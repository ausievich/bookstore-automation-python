"""HTTP client wrapper around httpx."""

from typing import Any

import httpx


class HttpClient:
    """Thin httpx wrapper that carries base URL and optional auth token."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._token: str | None = None
        self._client = httpx.Client(base_url=self._base_url, timeout=15.0)

    def set_auth_token(self, token: str | None) -> None:
        self._token = token

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        return self._client.get(path, params=params, headers=self._headers())

    def post(self, path: str, json: Any = None) -> httpx.Response:
        return self._client.post(path, json=json, headers=self._headers())

    def put(self, path: str, json: Any = None) -> httpx.Response:
        return self._client.put(path, json=json, headers=self._headers())

    def patch(self, path: str, json: Any = None) -> httpx.Response:
        return self._client.patch(path, json=json, headers=self._headers())

    def delete(self, path: str) -> httpx.Response:
        return self._client.delete(path, headers=self._headers())

    def close(self) -> None:
        self._client.close()
