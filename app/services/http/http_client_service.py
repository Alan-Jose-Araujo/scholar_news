# http_client_service.py
# @description A HTTP client implementation using the fetch API.
# @author Alan José <alanjsdelima@gmail.com>

import requests
import time
from fake_useragent import UserAgent
from typing import TypedDict, Optional, Dict

class HttpClientConfig(TypedDict, total=False):
    headers: Dict[str, str]
    cookies: Dict[str, str]
    timeout: int
    max_retries: int
    initial_retry_delay_in_ms: int
    proxies: Optional[Dict[str, str]]

class HttpClientService:

    _default_headers: Dict[str, str]

    _default_cookies: Dict[str, str]

    _timeout: int

    _max_retries: int

    _initial_retry_delay_in_ms: int

    _proxies: Optional[Dict[str, str]]

    _last_url: Optional[str]

    def __init__(self, config: HttpClientConfig):
        self._default_headers = config.get('headers', {
            "User-Agent": (UserAgent()).chrome,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        self._default_cookies = config.get('cookies', {})
        self._timeout = config.get('timeout', 15)
        self._max_retries = config.get('max_retries', 3)
        self._initial_retry_delay_in_ms = config.get('initial_retry_delay_in_ms', 1500)
        self._proxies = config.get('proxies', {})
        self._last_url = None

    def _serialize_cookies(self, cookies: Dict[str, str]) -> str:
        merged_cookies: Dict[str, str] = self._default_cookies | cookies
        cookies_string: str = ";".join(f"{key}={value}" for key, value in merged_cookies.items()) # Resulting in the pattern "Key=Value; Key=Value..."
        return cookies_string
    
    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        attempt: int = kwargs.get("attempt", 1)
        use_agent_rotation: bool = kwargs.get("use_agent_rotation", False)

        fetch_headers: Dict[str, str] = {
            **self._default_headers,
            "Referer": self._last_url or url,
            "Cookie": self._serialize_cookies(cookies),
            **headers,
        }
        fetch_cookies: Dict[str, str] = {
            **self._default_cookies,
            **cookies,
        }
        if use_agent_rotation:
            fetch_headers["User-Agent"] = (UserAgent()).random

        try:
            with requests.get(
                url=url,
                headers=fetch_headers,
                cookies=fetch_cookies,
                timeout=self._timeout,
                allow_redirects=True,
                proxies=self._proxies if self._proxies else {}
            ) as response:
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                self._last_url = url
                return response
        except requests.RequestException as exception:
            can_retry: bool = attempt <= self._max_retries
            if can_retry:
                delay: int = self._initial_retry_delay_in_ms * (2 ** (attempt - 1))
                print(f"[Attempt {attempt}] Fail to fetch {url}: {exception}. Attempting again in {delay}ms...")
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                return self.get(url, headers, cookies, attempt=attempt+1, use_agent_rotation=use_agent_rotation)
            else:
                print(f"[Request error on fetch] {url}: {exception}")
                raise