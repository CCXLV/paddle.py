import time

import httpx

from typing import Dict, Any, Optional, Type, TypeVar, Union

from .environment import Environment

from .exceptions import create_paddle_error
from .utils import is_retryable_status_code, get_retry_delay

T = TypeVar("T")


class BaseClient:
    """Base client for Paddle API interactions."""

    def __init__(
        self,
        *,
        api_key: str,
        environment: Union[Environment.PRODUCTION, Environment.SANDBOX] = Environment.SANDBOX,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = environment.base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return headers

    def _build_url(self, path: str) -> str:
        """Build full URL for API endpoint."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _create_resource(self, resource_class: Type[T]) -> T:
        """
        Create a resource instance.

        Parameters:
            resource_class: The resource class to instantiate

        Returns:
            An instance of the resource class

        Raises:
            PaddleAPIError: If the resource class is not found
        """
        return resource_class(self)

    def _add_extension(self, extension_class: Type[T]) -> T:
        """
        Add an extension to the client.

        Parameters:
            extension_class: The extension class to add

        Returns:
            An instance of the extension class
        """
        return extension_class()


class Client(BaseClient):
    """
    Synchronous client for Paddle API.

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
        *,
        api_key: str,
        environment: Union[Environment.PRODUCTION, Environment.SANDBOX] = Environment.SANDBOX,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        super().__init__(
            api_key=api_key, environment=environment, timeout=timeout, max_retries=max_retries
        )
        self._client = httpx.Client(
            timeout=self.timeout,
            headers=self._get_headers(),
        )

        # Initialize extensions
        self._init_extensions()

        # Initialize resources
        self._init_resources()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the HTTP client."""
        self._client.close()

    def _init_extensions(self):
        from .extensions import Webhooks

        self.webhooks = self._add_extension(Webhooks)

    def _init_resources(self):
        """Initialize resources."""
        from .models.resources import Product
        from .models.resources import Price
        from .models.resources import Customer
        from .models.resources import Subscription

        self.products = self._create_resource(Product)
        self.prices = self._create_resource(Price)
        self.customers = self._create_resource(Customer)
        self.subscriptions = self._create_resource(Subscription)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retry_on_error: bool = True,
    ) -> Dict[str, Any]:
        """
        Make a synchronous HTTP request.

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
                response = self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )

                if response.is_success:
                    return response.json()

                # Handle error response
                if retry_on_error and retries < self.max_retries:
                    status_code = response.status_code

                    if is_retryable_status_code(status_code):
                        retry_delay = get_retry_delay(
                            status_code, response.headers.get("Retry-After")
                        )
                        time.sleep(retry_delay)
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
                    time.sleep(1.0)  # Simple exponential backoff
                    retries += 1
                    continue
                raise create_paddle_error(500, str(e)) from e
