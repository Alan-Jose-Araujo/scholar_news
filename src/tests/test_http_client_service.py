from unittest.mock import Mock

import pytest

from scholar_news.services.HttpClientService import HttpClientService


def test_configures_proxies_and_retries() -> None:
    client = HttpClientService(
        proxies={"https": "http://proxy.example:8080"},
        retries=4,
        backoff_factor=0.5,
    )

    assert client.session.proxies["https"] == "http://proxy.example:8080"
    adapter = client.session.get_adapter("https://example.com")
    assert adapter.max_retries.total == 4
    assert adapter.max_retries.backoff_factor == 0.5
    assert adapter.max_retries.status_forcelist == frozenset(
        {429, 500, 502, 503, 504}
    )

    client.close()


def test_request_uses_default_timeout_and_forwards_arguments() -> None:
    client = HttpClientService(timeout=5.0)
    response = Mock()
    client.session.request = Mock(return_value=response)

    result = client.request("GET", "https://example.com", params={"page": 2})

    assert result is response
    client.session.request.assert_called_once_with(
        "GET",
        "https://example.com",
        params={"page": 2},
        timeout=5.0,
    )
    client.close()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"retries": -1}, "retries"),
        ({"backoff_factor": -0.1}, "backoff_factor"),
    ],
)
def test_rejects_negative_retry_settings(
    kwargs: dict[str, int | float], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        HttpClientService(**kwargs)
