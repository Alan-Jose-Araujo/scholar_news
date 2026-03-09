
# HttpClientService

## Overview

`HttpClientService` is a robust HTTP client wrapper built on top of the `requests` library. It provides configurable headers, cookies, retry logic, proxy support, and user-agent rotation for making HTTP GET requests with resilience and flexibility.

## Features

- Customizable headers and cookies
- Automatic retry with exponential backoff
- User-Agent rotation (using `fake_useragent`)
- Proxy support
- Timeout configuration
- Cookie serialization

## Configuration

The service is configured via a `HttpClientConfig` dictionary with the following optional keys:

- `headers`: `Dict[str, str]` — Default headers for all requests
- `cookies`: `Dict[str, str]` — Default cookies for all requests
- `timeout`: `int` — Request timeout in seconds (default: 15)
- `max_retries`: `int` — Maximum number of retry attempts (default: 3)
- `initial_retry_delay_in_ms`: `int` — Initial delay before retrying (ms, default: 1500)
- `proxies`: `Optional[Dict[str, str]]` — Proxy settings

## Usage

### Initialization

```python
config = {
	"headers": {"User-Agent": "CustomAgent/1.0"},
	"timeout": 10,
	"max_retries": 5,
	"proxies": {"http": "http://proxy.example.com:8080"}
}
client = HttpClientService(config)
```

### Making a GET Request

```python
response = client.get(
	"https://example.com",
	headers={"Custom-Header": "value"},
	cookies={"sessionid": "abc123"},
	use_agent_rotation=True  # Optional: rotate User-Agent
)
html = response.text
```

## Methods

### `get(url, headers=None, cookies=None, **kwargs)`

Performs an HTTP GET request with optional headers and cookies. Supports retries and user-agent rotation.

- `url`: Target URL
- `headers`: Additional headers (merged with defaults)
- `cookies`: Additional cookies (merged with defaults)
- `use_agent_rotation`: If True, rotates the User-Agent header
- Returns: `requests.Response`

### `_serialize_cookies(cookies)`

Merges default and provided cookies, serializing them into a string for the `Cookie` header.