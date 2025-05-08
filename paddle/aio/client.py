import httpx
import asyncio

from typing import Dict, Any, Optional, Union

from paddle.client import BaseClient
from paddle.environment import Environment
from paddle.exceptions import create_paddle_error
from paddle.utils import is_retryable_status_code, get_retry_delay


class AsyncClient(BaseClient):
    """
    Asynchronous client for Paddle API.

    Args:
        api_key: The API key for the Paddle API
        environment: The environment to use for the Paddle API
        timeout: The timeout for the Paddle API
        max_retries: The maximum number of retries for the Paddle API

    Raises:
        PaddleAPIError: If the API key is invalid
    """

    def __init__(
        self,
        api_key: str,
        environment: Union[Environment.PRODUCTION, Environment.SANDBOX] = Environment.SANDBOX,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        super().__init__(
            api_key=api_key, environment=environment, timeout=timeout, max_retries=max_retries
        )
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers=self._get_headers(),
        )
        # Initialize extensions
        self._init_extensions()

        # Initialize resources
        self._init_resources()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the HTTP client."""
        await self._client.aclose()

    def _init_extensions(self):
        from paddle.extensions import Webhooks

        self.webhooks = self._add_extension(Webhooks)

    def _init_resources(self):
        """Initialize resources."""
        from paddle.models.resources import AsyncProduct
        from paddle.models.resources import AsyncPrice
        from paddle.models.resources import AsyncCustomer
        from paddle.models.resources import AsyncSubscription

        self.products = self._create_resource(AsyncProduct)
        self.prices = self._create_resource(AsyncPrice)
        self.customers = self._create_resource(AsyncCustomer)
        self.subscriptions = self._create_resource(AsyncSubscription)

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retry_on_error: bool = True,
    ) -> Dict[str, Any]:
        """
        Make an asynchronous HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            json: JSON body for POST/PUT requests
            retry_on_error: Whether to retry on retryable errors

        Returns:
            JSON response from the API

        Raises:
            PaddleAPIError: If the API request fails
        """
        url = self._build_url(path)
        retries = 0

        while True:
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )

                if response.is_success:
                    try:
                        return response.json()
                    except ValueError as e:  # httpx uses ValueError for JSON decode errors
                        raise create_paddle_error(
                            status_code=response.status_code,
                            message="Invalid JSON response",
                        ) from e

                # Handle error response
                if retry_on_error and retries < self.max_retries:
                    status_code = response.status_code

                    if is_retryable_status_code(status_code):
                        retry_delay = get_retry_delay(
                            status_code, response.headers.get("Retry-After")
                        )
                        await asyncio.sleep(retry_delay)
                        retries += 1
                        continue

                # If we get here, either we're not retrying or we've exhausted retries
                raise create_paddle_error(
                    status_code=response.status_code,
                    message=response.text,
                )

            except httpx.RequestError as e:
                # Handle network errors
                if retry_on_error and retries < self.max_retries:
                    await asyncio.sleep(1.0)  # Simple exponential backoff
                    retries += 1
                    continue
                raise create_paddle_error(500, str(e)) from e
