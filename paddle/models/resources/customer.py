"""
Paddle Customers API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Any, Dict, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient
from paddle.exceptions import PaddleAPIError, create_paddle_error

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.customer import (
    CustomerListResponse,
    CustomerCreateResponse,
    CustomerGetResponse,
    CustomerUpdateResponse,
    CustomerCreditBalanceResponse,
    CustomerAuthTokenResponse,
    CustomerPortalSessionResponse,
)

from paddle.utils.decorators import validate_params
from paddle.utils.helpers import filter_none_kwargs


class CustomerBase(ResourceBase):
    """
    Paddle Customers API endpoints.
    """

    def __init__(self, client: Union[Client, AsyncClient]):
        self._client = client

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list customers."""
        raise NotImplementedError("Subclasses must implement this method")

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a customer."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to get a customer."""
        raise NotImplementedError("Subclasses must implement this method")

    def _update(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a customer."""
        raise NotImplementedError("Subclasses must implement this method")

    def _list_credit_balances(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list credit balances."""
        raise NotImplementedError("Subclasses must implement this method")

    def _generate_auth_token(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to generate an authorization token for a customer."""
        raise NotImplementedError("Subclasses must implement this method")

    def _create_portal_session(
        self, customer_id: str, subscription_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Internal method to create a portal session for a customer."""
        raise NotImplementedError("Subclasses must implement this method")

    @validate_params
    def list(
        self,
        *,
        after: Optional[str] = None,
        email: Optional[List[str]] = None,
        id: Optional[List[str]] = None,
        order_by: Optional[
            Literal[
                "id[ASC]",
                "id[DESC]",
                "created_at[ASC]",
                "created_at[DESC]",
                "updated_at[ASC]",
                "updated_at[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        search: Optional[str] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
    ) -> CustomerListResponse:
        # TODO: Add docstring

        params = filter_none_kwargs(
            after=after,
            email=",".join(email) if email else None,
            id=",".join(id) if id else None,
            order_by=order_by,
            per_page=per_page,
            search=search,
            status=",".join(status) if status else None,
        )
        response = self._list(**params)

        return CustomerListResponse(response)

    @validate_params
    def create(
        self,
        *,
        email: str,
        name: Optional[str] = None,
        custom_data: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
    ) -> CustomerCreateResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                email=email,
                name=name,
                custom_data=custom_data,
                locale=locale,
            )
            response = self._create(**params)

            return CustomerCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get(
        self,
        customer_id: str,
    ) -> CustomerGetResponse:
        # TODO: Add docstring

        try:
            response = self._get(customer_id)

            return CustomerGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def update(
        self,
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[Literal["active", "archived"]] = None,
        custom_data: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
    ) -> CustomerUpdateResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                name=name,
                email=email,
                status=status,
                custom_data=custom_data,
                locale=locale,
            )
            response = self._update(customer_id, **params)

            return CustomerUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def list_credit_balances(
        self,
        customer_id: str,
        *,
        currency_code: Optional[List[str]] = None,
    ) -> CustomerCreditBalanceResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                currency_code=",".join(currency_code) if currency_code else None,
            )
            response = self._list_credit_balances(customer_id, **params)

            return CustomerCreditBalanceResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def generate_auth_token(
        self,
        customer_id: str,
    ) -> CustomerAuthTokenResponse:
        # TODO: Add docstring

        try:
            response = self._generate_auth_token(customer_id)

            return CustomerAuthTokenResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def create_portal_session(
        self,
        customer_id: str,
        *,
        subscription_ids: Optional[List[str]] = None,
    ) -> CustomerPortalSessionResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                subscription_ids=subscription_ids,
            )
            response = self._create_portal_session(customer_id, **params)

            return CustomerPortalSessionResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e


class Customer(CustomerBase):
    """
    Paddle Customers API endpoints.
    """

    def __init__(self, client: Client):
        super().__init__(client)

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list customers."""
        return self._client._request(
            method="GET",
            path="/customers",
            params=kwargs,
        )

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a customer."""
        return self._client._request(
            method="POST",
            path="/customers",
            json=kwargs,
        )

    def _get(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to get a customer."""
        return self._client._request(
            method="GET",
            path=f"/customers/{customer_id}",
        )

    def _update(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a customer."""
        return self._client._request(
            method="PATCH",
            path=f"/customers/{customer_id}",
            json=kwargs,
        )

    def _list_credit_balances(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list credit balances."""
        return self._client._request(
            method="GET",
            path=f"/customers/{customer_id}/credit-balances",
            params=kwargs,
        )

    def _generate_auth_token(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to generate an authorization token for a customer."""
        return self._client._request(
            method="POST",
            path=f"/customers/{customer_id}/auth-token",
        )

    def _create_portal_session(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a portal session for a customer."""
        return self._client._request(
            method="POST",
            path=f"/customers/{customer_id}/portal-sessions",
            json=kwargs,
        )


class AsyncCustomer(CustomerBase):
    """
    Paddle Customers API endpoints.
    """

    def __init__(self, client: AsyncClient):
        super().__init__(client)

    async def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list customers."""
        return await self._client._request(
            method="GET",
            path="/customers",
            params=kwargs,
        )

    async def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a customer."""
        return await self._client._request(
            method="POST",
            path="/customers",
            json=kwargs,
        )

    async def _get(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to get a customer."""
        return await self._client._request(
            method="GET",
            path=f"/customers/{customer_id}",
        )

    async def _update(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a customer."""
        return await self._client._request(
            method="PATCH",
            path=f"/customers/{customer_id}",
            json=kwargs,
        )

    async def _list_credit_balances(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list credit balances."""
        return await self._client._request(
            method="GET",
            path=f"/customers/{customer_id}/credit-balances",
            params=kwargs,
        )

    async def _generate_auth_token(self, customer_id: str) -> Dict[str, Any]:
        """Internal method to generate an authorization token for a customer."""
        return await self._client._request(
            method="POST",
            path=f"/customers/{customer_id}/auth-token",
        )

    async def _create_portal_session(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a portal session for a customer."""
        return await self._client._request(
            method="POST",
            path=f"/customers/{customer_id}/portal-sessions",
            json=kwargs,
        )

    @validate_params
    async def list(
        self,
        *,
        after: Optional[str] = None,
        email: Optional[List[str]] = None,
        id: Optional[List[str]] = None,
        order_by: Optional[
            Literal[
                "id[ASC]",
                "id[DESC]",
                "created_at[ASC]",
                "created_at[DESC]",
                "updated_at[ASC]",
                "updated_at[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        search: Optional[str] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
    ) -> CustomerListResponse:
        # TODO: Add docstring

        params = filter_none_kwargs(
            after=after,
            email=",".join(email) if email else None,
            id=",".join(id) if id else None,
            order_by=order_by,
            per_page=per_page,
            search=search,
            status=",".join(status) if status else None,
        )
        response = await self._list(**params)

        return CustomerListResponse(response)

    @validate_params
    async def create(
        self,
        *,
        email: str,
        name: Optional[str] = None,
        custom_data: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
    ) -> CustomerCreateResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                email=email,
                name=name,
                custom_data=custom_data,
                locale=locale,
            )
            response = await self._create(**params)

            return CustomerCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get(
        self,
        customer_id: str,
    ) -> CustomerGetResponse:
        # TODO: Add docstring

        try:
            response = await self._get(customer_id)

            return CustomerGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def update(
        self,
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[Literal["active", "archived"]] = None,
        custom_data: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
    ) -> CustomerUpdateResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                name=name,
                email=email,
                status=status,
                custom_data=custom_data,
                locale=locale,
            )
            response = await self._update(customer_id, **params)

            return CustomerUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def list_credit_balances(
        self,
        customer_id: str,
        *,
        currency_code: Optional[List[str]] = None,
    ) -> CustomerCreditBalanceResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                currency_code=",".join(currency_code) if currency_code else None,
            )
            response = await self._list_credit_balances(customer_id, **params)

            return CustomerCreditBalanceResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def generate_auth_token(
        self,
        customer_id: str,
    ) -> CustomerAuthTokenResponse:
        # TODO: Add docstring

        try:
            response = await self._generate_auth_token(customer_id)

            return CustomerAuthTokenResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def create_portal_session(
        self,
        customer_id: str,
        *,
        subscription_ids: Optional[List[str]] = None,
    ) -> CustomerPortalSessionResponse:
        # TODO: Add docstring

        try:
            params = filter_none_kwargs(
                subscription_ids=subscription_ids,
            )
            response = await self._create_portal_session(customer_id, **params)

            return CustomerPortalSessionResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e
