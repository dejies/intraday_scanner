"""
Generic HTTP client.

Provides a reusable HTTP client with:

- GET
- POST
- Configurable timeout
- Retry support
- Automatic JSON parsing
- File download
- Header management
- Consistent logging
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import requests

from src.core.exceptions import ConnectionError
from src.services.base_service import BaseService
from src.core.exceptions import ConnectionError

class HttpClient(BaseService):
    """
    Generic HTTP client.

    Can be reused for any REST API.
    """

    def __init__(
            self,
            base_url: str,
            timeout: int = 30,
            retry_count: int = 3,
            retry_delay: float = 0.5,
            headers: dict[str, str] | None = None,
    ) -> None:

        super().__init__()

        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        self.retry_count = retry_count

        self.retry_delay = retry_delay

        self.session = requests.Session()

        if headers:
            self.session.headers.update(headers)

    # ------------------------------------------------------------------
    # Header Management
    # ------------------------------------------------------------------

    def set_headers(
            self,
            headers: dict[str, str],
    ) -> None:
        """
        Replace all request headers.
        """

        self.session.headers.clear()

        self.session.headers.update(headers)

    # ------------------------------------------------------------------

    def add_header(
            self,
            key: str,
            value: str,
    ) -> None:
        """
        Add or replace a single header.
        """

        self.session.headers[key] = value

    # ------------------------------------------------------------------

    def remove_header(
            self,
            key: str,
    ) -> None:
        """
        Remove a request header.
        """

        self.session.headers.pop(
            key,
            None,
        )

    # ------------------------------------------------------------------

    @property
    def headers(
            self,
    ) -> dict[str, str]:
        """
        Current request headers.
        """

        return dict(
            self.session.headers
        )

    # ------------------------------------------------------------------
    # URL Builder
    # ------------------------------------------------------------------

    def _build_url(
            self,
            path: str = "",
    ) -> str:
        """
        Build request URL safely.
        """

        base = self.base_url.rstrip("/")

        if not path:
            return base

        return f"{base}/{path.lstrip('/')}"

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------

    def get(
            self,
            endpoint: str,
            params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute HTTP GET.
        """

        return self._request(
            method="GET",
            url=self._build_url(endpoint),
            params=params,
        )

    # ------------------------------------------------------------------
    # POST
    # ------------------------------------------------------------------

    def post(
            self,
            endpoint: str,
            payload: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute HTTP POST.
        """

        return self._request(
            method="POST",
            url=self._build_url(endpoint),
            json=payload,
        )

    # ------------------------------------------------------------------
    # PUT
    # ------------------------------------------------------------------

    def put(
            self,
            endpoint: str,
            payload: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute HTTP PUT.
        """

        return self._request(
            method="PUT",
            url=self._build_url(endpoint),
            json=payload,
        )

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete(
            self,
            endpoint: str,
    ) -> Any:
        """
        Execute HTTP DELETE.
        """

        return self._request(
            method="DELETE",
            url=self._build_url(endpoint),
        )

    # ------------------------------------------------------------------
    # Core Request
    # ------------------------------------------------------------------

    def _request(
            self,
            method: str,
            url: str,
            **kwargs,
    ) -> Any:
        """
        Execute an HTTP request with retries.
        """

        last_exception = None

        for attempt in range(
                1,
                self.retry_count + 1,
        ):

            try:

                self.logger.debug(
                    "%s %s",
                    method,
                    url,
                )

                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs,
                )

                response.raise_for_status()

                if not response.content:
                    return None

                content_type = response.headers.get(
                    "Content-Type",
                    "",
                )

                if "application/json" in content_type:

                    return response.json()

                return response.text

            except requests.RequestException as exc:

                last_exception = exc

                self.logger.warning(
                    "Attempt %d/%d failed: %s",
                    attempt,
                    self.retry_count,
                    exc,
                )

                if attempt < self.retry_count:

                    time.sleep(
                        self.retry_delay,
                    )

        raise ConnectionError(
            f"HTTP request failed: {last_exception}"
        )

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------

    def download(
            self,
            endpoint: str,
            destination: str | Path,
    ) -> None:
        """
        Download a file.
        """

        url = self._build_url(endpoint)

        destination = Path(destination)

        self.logger.info(
            "Downloading %s",
            url,
        )

        response = self.session.get(
            url,
            timeout=self.timeout,
            stream=True,
        )

        response.raise_for_status()

        with destination.open("wb") as file:

            for chunk in response.iter_content(
                    chunk_size=8192,
            ):

                if chunk:

                    file.write(chunk)

        self.logger.info(
            "Saved %s",
            destination,
        )