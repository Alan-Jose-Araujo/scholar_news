# http_client_service_test.py
# This file holds the http client service unitary tests.

import pytest
import requests
from unittest.mock import patch, MagicMock
from app.services.http.http_client_service import HttpClientService, HttpClientConfig

class TestHttpClientService:

    def test_init_with_default_config(self):
        config = HttpClientConfig()
        service = HttpClientService(config)
        assert isinstance(service._default_headers, dict)
        assert isinstance(service._default_cookies, dict)
        assert isinstance(service._timeout, int)
        assert isinstance(service._max_retries, int)
        assert isinstance(service._initial_retry_delay_in_ms, int)

    def test_serialize_cookies_merges_and_serializes(self):
        config = HttpClientConfig(cookies={"a": "1"})
        service = HttpClientService(config)
        cookies = {"b": "2"}
        result = service._serialize_cookies(cookies)
        assert "a=1" in result and "b=2" in result
        assert ";" in result

    @patch("app.services.http.http_client_service.requests.get")
    def test_get_successful_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.status_code = 200
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response
        service = HttpClientService(HttpClientConfig())
        response = service.get("http://test.com")
        assert response.status_code == 200
        assert service._last_url == "http://test.com"

    @patch("app.services.http.http_client_service.requests.get")
    def test_get_retries_and_raises(self, mock_get):
        mock_get.side_effect = requests.RequestException("fail")
        service = HttpClientService(HttpClientConfig(max_retries=2, initial_retry_delay_in_ms=1))
        with pytest.raises(requests.RequestException):
            service.get("http://fail.com")

    @patch("app.services.http.http_client_service.requests.get")
    def test_get_with_custom_headers_and_cookies(self, mock_get):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.status_code = 200
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response
        service = HttpClientService(HttpClientConfig())
        response = service.get(
            "http://test.com",
            headers={"X-Test": "1"},
            cookies={"session": "abc"}
        )
        assert response.status_code == 200
        called_kwargs = mock_get.call_args[1]
        assert "X-Test" in called_kwargs["headers"]
        assert called_kwargs["cookies"]["session"] == "abc"

    @patch("app.services.http.http_client_service.UserAgent")
    @patch("app.services.http.http_client_service.requests.get")
    def test_get_with_user_agent_rotation(self, mock_get, mock_useragent):
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.status_code = 200
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response
        mock_useragent.return_value.random = "rotated-agent"
        service = HttpClientService(HttpClientConfig())
        service.get("http://test.com", use_agent_rotation=True)
        called_kwargs = mock_get.call_args[1]
        assert called_kwargs["headers"]["User-Agent"] == "rotated-agent"