"""
Paddle Customers API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Any, Dict, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient
from paddle.exceptions import PaddleAPIError, create_paddle_error

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.customers import (
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
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        search: Optional[str] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
    ) -> CustomerListResponse:
        """
        List customers.

        Parameters
        ----------

            after: Optional[str] = None
                Return only the IDs greater than the specified ID.

            email: Optional[List[str]] = None
                Return only the IDs specified.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            order_by: Optional[
                Literal[
                    "id[ASC]",
                    "id[DESC]",
                ]
            ] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            search: Optional[str] = None
                Return only the entities that match the specified search query.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return only the entities that match the specified status.

        Returns
        -------

            A list of customers.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            customers = client.customers.list()
            print(customers)

        """

        kwargs = filter_none_kwargs(
            after=after,
            email=",".join(email) if email else None,
            id=",".join(id) if id else None,
            order_by=order_by,
            per_page=per_page,
            search=search,
            status=",".join(status) if status else None,
        )
        response = self._list(**kwargs)

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
        """
        Create a customer.

        Parameters
        ----------

            email: str
                The email address of the customer.

            name: Optional[str] = None
                The name of the customer.

            custom_data: Optional[Dict[str, str]] = None
                Custom data for the customer.

            locale: Optional[str] = None
                The locale of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleBadRequestError: If the request is invalid.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            customer = client.customers.create(email="test@example.com")
            print(customer)

        """

        try:
            kwargs = filter_none_kwargs(
                email=email,
                name=name,
                custom_data=custom_data,
                locale=locale,
            )
            response = self._create(**kwargs)

            return CustomerCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get(
        self,
        customer_id: str,
    ) -> CustomerGetResponse:
        """
        Get a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            customer = client.customers.get("ctm_1234567890")
            print(customer)

        """

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
        """
        Update a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            name: Optional[str] = None
                The name of the customer.

            email: Optional[str] = None
                The email address of the customer.

            status: Optional[Literal["active", "archived"]] = None
                The status of the customer.

            custom_data: Optional[Dict[str, str]] = None
                Custom data for the customer.

            locale: Optional[str] = None
                The locale of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleBadRequestError: If the request is invalid.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            customer = client.customers.update(customer_id="ctm_1234567890", name="John Doe")
            print(customer)

        """

        try:
            kwargs = filter_none_kwargs(
                name=name,
                email=email,
                status=status,
                custom_data=custom_data,
                locale=locale,
            )
            response = self._update(customer_id, **kwargs)

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
        """
        List credit balances for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            currency_code: Optional[List[str]] = None
                The currency code of the credit balance.

        Returns
        -------

            A list of credit balances.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            credit_balances = client.customers.list_credit_balances(customer_id="ctm_1234567890")
            print(credit_balances)

        """

        try:
            kwargs = filter_none_kwargs(
                currency_code=",".join(currency_code) if currency_code else None,
            )
            response = self._list_credit_balances(customer_id, **kwargs)

            return CustomerCreditBalanceResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def generate_auth_token(
        self,
        customer_id: str,
    ) -> CustomerAuthTokenResponse:
        """
        Generate an authorization token for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

        Returns
        -------

            An authorization token.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            auth_token = client.customers.generate_auth_token(customer_id="ctm_1234567890")
            print(auth_token)

        """

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
        """
        Create a portal session for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            subscription_ids: Optional[List[str]] = None
                The IDs of the subscriptions to include in the portal session.

        Returns
        -------

            A portal session.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            portal_session = client.customers.create_portal_session(
                customer_id="ctm_1234567890",
                subscription_ids=["sub_1234567890"],
            )
            print(portal_session)

        """

        try:
            kwargs = filter_none_kwargs(
                subscription_ids=subscription_ids,
            )
            response = self._create_portal_session(customer_id, **kwargs)

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
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        search: Optional[str] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
    ) -> CustomerListResponse:
        """
        List customers.

        Parameters
        ----------

            after: Optional[str] = None
                Return only the IDs greater than the specified ID.

            email: Optional[List[str]] = None
                Return only the IDs specified.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            order_by: Optional[
                Literal[
                    "id[ASC]",
                    "id[DESC]",
                ]
            ] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            search: Optional[str] = None
                Return only the entities that match the specified search query.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return only the entities that match the specified status.

        Returns
        -------

            A list of customers.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    customers = await client.customers.list()
                    print(customers)

            asyncio.run(main())
        """

        kwargs = filter_none_kwargs(
            after=after,
            email=",".join(email) if email else None,
            id=",".join(id) if id else None,
            order_by=order_by,
            per_page=per_page,
            search=search,
            status=",".join(status) if status else None,
        )
        response = await self._list(**kwargs)

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
        """|coroutine|

        Create a customer.

        Parameters
        ----------

            email: str
                The email address of the customer.

            name: Optional[str] = None
                The name of the customer.

            custom_data: Optional[Dict[str, str]] = None
                Custom data for the customer.

            locale: Optional[str] = None
                The locale of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleBadRequestError: If the request is invalid.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    customer = await client.customers.create(email="test@example.com")
                print(customer)

            asyncio.run(main())

        """

        try:
            kwargs = filter_none_kwargs(
                email=email,
                name=name,
                custom_data=custom_data,
                locale=locale,
            )
            response = await self._create(**kwargs)

            return CustomerCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get(
        self,
        customer_id: str,
    ) -> CustomerGetResponse:
        """|coroutine|

        Get a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    customer = await client.customers.get("ctm_1234567890")
                    print(customer)

            asyncio.run(main())

        """

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
        """|coroutine|

        Update a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            name: Optional[str] = None
                The name of the customer.

            email: Optional[str] = None
                The email address of the customer.

            status: Optional[Literal["active", "archived"]] = None
                The status of the customer.

            custom_data: Optional[Dict[str, str]] = None
                Custom data for the customer.

            locale: Optional[str] = None
                The locale of the customer.

        Returns
        -------

            A customer.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleBadRequestError: If the request is invalid.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    customer = await client.customers.update(customer_id="ctm_1234567890", name="John Doe")
                    print(customer)

            asyncio.run(main())

        """

        try:
            kwargs = filter_none_kwargs(
                name=name,
                email=email,
                status=status,
                custom_data=custom_data,
                locale=locale,
            )
            response = await self._update(customer_id, **kwargs)

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
        """|coroutine|

        List credit balances for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            currency_code: Optional[List[str]] = None
                The currency code of the credit balance.

        Returns
        -------

            A list of credit balances.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    credit_balances = await client.customers.list_credit_balances(customer_id="ctm_1234567890")
                    print(credit_balances)

            asyncio.run(main())

        """
        try:
            kwargs = filter_none_kwargs(
                currency_code=",".join(currency_code) if currency_code else None,
            )
            response = await self._list_credit_balances(customer_id, **kwargs)

            return CustomerCreditBalanceResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def generate_auth_token(
        self,
        customer_id: str,
    ) -> CustomerAuthTokenResponse:
        """|coroutine|

        Generate an authorization token for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

        Returns
        -------

            An authorization token.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    auth_token = await client.customers.generate_auth_token(customer_id="ctm_1234567890")
                    print(auth_token)

            asyncio.run(main())

        """

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
        """|coroutine|

        Create a portal session for a customer.

        Parameters
        ----------

            customer_id: str
                The ID of the customer.

            subscription_ids: Optional[List[str]] = None
                The IDs of the subscriptions to include in the portal session.

        Returns
        -------

            A portal session.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the customer is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    portal_session = await client.customers.create_portal_session(
                        customer_id="ctm_1234567890",
                        subscription_ids=["sub_1234567890"],
                    )
                    print(portal_session)

            asyncio.run(main())

        """

        try:
            kwargs = filter_none_kwargs(
                subscription_ids=subscription_ids,
            )
            response = await self._create_portal_session(customer_id, **kwargs)

            return CustomerPortalSessionResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e
