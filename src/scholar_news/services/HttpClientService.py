"""HTTP client service with proxy support and retry backoff."""

from collections.abc import Mapping
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3.util.retry import Retry


class HttpClientService:
    """Reusable HTTP client with configurable proxies and retries."""

    def __init__(
        self,
        proxies: Mapping[str, str] | None = None,
        retries: int = 3,
        backoff_factor: float = 0.3,
        timeout: float | tuple[float, float] = 10.0,
    ) -> None:
        if retries < 0:
            raise ValueError("retries must be non-negative")
        if backoff_factor < 0:
            raise ValueError("backoff_factor must be non-negative")

        self.timeout = timeout
        self.session = requests.Session()
        if proxies:
            self.session.proxies.update(proxies)

        retry_policy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=frozenset({429, 500, 502, 503, 504}),
            allowed_methods=frozenset(
                {"DELETE", "GET", "HEAD", "OPTIONS", "PUT", "TRACE"}
            ),
        )
        adapter = HTTPAdapter(max_retries=retry_policy)
        self.session.mount("https://", adapter)

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        """Send an HTTP request and return its response."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, url, **kwargs)

    def close(self) -> None:
        """Close the underlying session and its connections."""
        self.session.close()

    def __enter__(self) -> "HttpClientService":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
