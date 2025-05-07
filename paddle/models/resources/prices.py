"""
Paddle Prices API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Any, Dict, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.prices import (
    PriceListResponse,
    PriceCreateResponse,
    PriceGetResponse,
    PriceUpdateResponse,
    UnitPriceType,
    BillingCycleType,
    UnitPriceOverridesType,
    QuantityType,
)

from paddle.utils.decorators import validate_params
from paddle.utils.helpers import filter_none_kwargs

from paddle.exceptions import PaddleAPIError, create_paddle_error


class PriceBase(ResourceBase):
    """
    Paddle Prices API endpoints.
    """

    def __init__(self, client: Union[Client, AsyncClient]):
        self._client = client

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list products."""
        raise NotImplementedError("Subclasses must implement this method")

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        raise NotImplementedError("Subclasses must implement this method")

    @validate_params
    def list(
        self,
        *,
        after: Optional[str] = None,
        id: Optional[List[str]] = None,
        include: Optional[List[Literal["product"]]] = None,
        order_by: Optional[
            Literal[
                "billing_cycle.frequency[ASC]",
                "billing_cycle.frequency[DESC]",
                "billing_cycle.interval[ASC]",
                "billing_cycle.interval[DESC]",
                "id[ASC]",
                "id[DESC]",
                "product_id[ASC]",
                "product_id[DESC]",
                "quantity.maximum[ASC]",
                "quantity.maximum[DESC]",
                "quantity.minimum[ASC]",
                "quantity.minimum[DESC]",
                "status[ASC]",
                "status[DESC]",
                "tax_mode[ASC]",
                "tax_mode[DESC]",
                "unit_price.amount[ASC]",
                "unit_price.amount[DESC]",
                "unit_price.currency_code[ASC]",
                "unit_price.currency_code[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        product_id: Optional[List[str]] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
        recurring: Optional[bool] = None,
        type: Optional[Literal["custom", "standard"]] = None,
    ) -> PriceListResponse:
        """
        List prices.

        Parameters
        ----------

            after: Optional[str] = None
                Return entities after the specified Paddle ID when working with paginated endpoints.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            include: Optional[List[Literal["product"]]] = None
                Include related entities in the response.

            order_by: Optional[
                Literal[
                    "billing_cycle.frequency[ASC]",
                    "billing_cycle.frequency[DESC]",
                    ...
                ]
            ] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            product_id: Optional[List[str]] = None
                The IDs of the products to list.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return entities that match the specified status. Use a comma-separated list to specify multiple status values.

            recurring: Optional[bool] = None
                Return entities that match the specified recurring status.

            type: Optional[Literal["custom", "standard"]] = None
                Return entities that match the specified type.

        Returns
        -------

            A list of prices.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            prices = client.prices.list()
            print(prices)

        """

        try:
            kwargs = filter_none_kwargs(
                after=after,
                id=",".join(id) if id else None,
                include=",".join(include) if include else None,
                order_by=order_by,
                per_page=per_page,
                product_id=",".join(product_id) if product_id else None,
                status=",".join(status) if status else None,
                recurring=recurring,
                type=type,
            )
            response = self._list(**kwargs)

            return PriceListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def create(
        self,
        *,
        description: str,
        product_id: str,
        unit_price: Union[UnitPriceType, Dict[str, str]],
        type: Optional[str] = None,
        name: Optional[str] = None,
        billing_cycle: Optional[BillingCycleType] = None,
        trial_period: Optional[BillingCycleType] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None,
        quantity: Optional[QuantityType] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ) -> PriceCreateResponse:
        """
        Create a price.

        Parameters
        ----------

            description: str
               Internal description for this price, not shown to customers. Typically notes for your team.

            product_id: str
                Paddle ID for the product that this price is for, prefixed with `pro_`.

            unit_price: Union[UnitPriceType, Dict[str, str]]
                Base price. This price applies to all customers, except for customers located in countries where you have unit_price_overrides.

            type: Optional[str] = None
                The type of the price.

            name: Optional[str] = None
                Name of this price, shown to customers at checkout and on invoices.

            billing_cycle: Optional[BillingCycleType] = None
                How often this price should be charged.

            trial_period: Optional[BillingCycleType] = None
                Trial period for the product related to this price. The billing cycle begins once the trial period is over. null for no trial period. Requires billing_cycle. If omitted, defaults to null.

            tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None
                How tax is calculated for this price.

            unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None
                Limits on how many times the related product can be purchased at this price.

            quantity: Optional[QuantityType] = None
                The quantity of the price.

            custom_data: Optional[Dict[str, str]] = None
                Arbitrary data you can store with this price.

        Returns
        -------

            A price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            price = client.prices.create(
                description="My Price",
                product_id="prod_1234567890",
                unit_price=100,
                type="standard",
            )
            print(price)
        """

        try:
            kwargs = filter_none_kwargs(
                description=description,
                product_id=product_id,
                unit_price=unit_price,
                type=type,
                name=name,
                billing_cycle=billing_cycle,
                trial_period=trial_period,
                tax_mode=tax_mode,
                unit_price_overrides=unit_price_overrides,
                quantity=quantity,
                custom_data=custom_data,
            )
            response = self._create(**kwargs)

            return PriceCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get(
        self,
        price_id: str,
        *,
        include: Optional[List[Literal["product"]]] = None,
    ) -> PriceGetResponse:
        """
        Get a price.

        Parameters
        ----------

            price_id: str
                The ID of the price to get.

            include: Optional[List[Literal["product"]]] = None
                Include related entities in the response.

        Returns
        -------

            A price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            price = client.prices.get(price_id="pri_1234567890")
            print(price)
        """

        try:
            kwargs = filter_none_kwargs(include=",".join(include) if include else None)
            response = self._get(price_id, **kwargs)

            return PriceGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def update(
        self,
        price_id: str,
        *,
        description: Optional[str] = None,
        type: Optional[str] = None,
        name: Optional[str] = None,
        billing_cycle: Optional[BillingCycleType] = None,
        trial_period: Optional[BillingCycleType] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None,
        quantity: Optional[QuantityType] = None,
        status: Optional[Literal["active", "archived"]] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ) -> PriceUpdateResponse:
        """
        Update a price.

        Parameters
        ----------

            price_id: str
                The ID of the price to update.

            description: Optional[str] = None
                Internal description for this price, not shown to customers. Typically notes for your team.

            type: Optional[str] = None
                The type of the price.

            name: Optional[str] = None
                Name of this price, shown to customers at checkout and on invoices.

            billing_cycle: Optional[BillingCycleType] = None
                How often this price should be charged.

            trial_period: Optional[BillingCycleType] = None
                Trial period for the product related to this price. The billing cycle begins once the trial period is over. null for no trial period. Requires billing_cycle. If omitted, defaults to null.

            tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None
                How tax is calculated for this price.

            unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None
                Limits on how many times the related product can be purchased at this price.

            quantity: Optional[QuantityType] = None
                The quantity of the price.

            status: Optional[Literal["active", "archived"]] = None
                The status of the price.

            custom_data: Optional[Dict[str, str]] = None
                Arbitrary data you can store with this price.

        Returns
        -------

            Updated price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            from paddle import Client

            client = Client(api_key="your_api_key")
            price = client.prices.update(
                price_id="pri_1234567890",
                description="My Updated Price",
            )
            print(price)
        """

        try:
            kwargs = filter_none_kwargs(
                description=description,
                type=type,
                name=name,
                billing_cycle=billing_cycle,
                trial_period=trial_period,
                tax_mode=tax_mode,
                unit_price_overrides=unit_price_overrides,
                quantity=quantity,
                status=status,
                custom_data=custom_data,
            )
            response = self._update(price_id, **kwargs)

            return PriceUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e


class Price(PriceBase):
    """Resource for Paddle Prices API endpoints."""

    def __init__(self, client: Client):
        super().__init__(client)

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list prices."""
        return self._client._request(
            method="GET",
            path="/prices",
            params=kwargs,
        )

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a price."""
        return self._client._request(
            method="POST",
            path="/prices",
            json=kwargs,
        )

    def _get(self, price_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a price."""
        return self._client._request(
            method="GET",
            path=f"/prices/{price_id}",
            params=kwargs,
        )

    def _update(self, price_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a price."""
        return self._client._request(
            method="PATCH",
            path=f"/prices/{price_id}",
            json=kwargs,
        )


class AsyncPrice(PriceBase):
    """Resource for Paddle Prices API endpoints."""

    def __init__(self, client: AsyncClient):
        super().__init__(client)

    async def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list prices."""
        return await self._client._request(
            method="GET",
            path="/prices",
            params=kwargs,
        )

    async def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a price."""
        return await self._client._request(
            method="POST",
            path="/prices",
            json=kwargs,
        )

    async def _get(self, price_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a price."""
        return await self._client._request(
            method="GET",
            path=f"/prices/{price_id}",
            params=kwargs,
        )

    async def _update(self, price_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a price."""
        return await self._client._request(
            method="PATCH",
            path=f"/prices/{price_id}",
            json=kwargs,
        )

    @validate_params
    async def list(
        self,
        *,
        after: Optional[str] = None,
        id: Optional[List[str]] = None,
        include: Optional[List[Literal["product"]]] = None,
        order_by: Optional[
            Literal[
                "billing_cycle.frequency[ASC]",
                "billing_cycle.frequency[DESC]",
                "billing_cycle.interval[ASC]",
                "billing_cycle.interval[DESC]",
                "id[ASC]",
                "id[DESC]",
                "product_id[ASC]",
                "product_id[DESC]",
                "quantity.maximum[ASC]",
                "quantity.maximum[DESC]",
                "quantity.minimum[ASC]",
                "quantity.minimum[DESC]",
                "status[ASC]",
                "status[DESC]",
                "tax_mode[ASC]",
                "tax_mode[DESC]",
                "unit_price.amount[ASC]",
                "unit_price.amount[DESC]",
                "unit_price.currency_code[ASC]",
                "unit_price.currency_code[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        product_id: Optional[List[str]] = None,
        status: Optional[List[Literal["active", "archived"]]] = None,
        recurring: Optional[bool] = None,
        type: Optional[Literal["custom", "standard"]] = None,
    ) -> PriceListResponse:
        """|coroutine|

        List prices.

        Parameters
        ----------

            after: Optional[str] = None
                Return entities after the specified Paddle ID when working with paginated endpoints.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            include: Optional[List[Literal["product"]]] = None
                Include related entities in the response.

            order_by: Optional[
                Literal[
                    "billing_cycle.frequency[ASC]",
                    "billing_cycle.frequency[DESC]",
                    ...
                ]
            ] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            product_id: Optional[List[str]] = None
                The IDs of the products to list.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return entities that match the specified status. Use a comma-separated list to specify multiple status values.

            recurring: Optional[bool] = None
                Return entities that match the specified recurring status.

            type: Optional[Literal["custom", "standard"]] = None
                Return entities that match the specified type.

        Returns
        -------

            A list of prices.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    prices = await client.prices.list()
                    print(prices)

            asyncio.run(main())

        """

        try:
            params = filter_none_kwargs(
                after=after,
                id=",".join(id) if id else None,
                include=",".join(include) if include else None,
                order_by=order_by,
                per_page=per_page,
                product_id=",".join(product_id) if product_id else None,
                status=",".join(status) if status else None,
                recurring=recurring,
                type=type,
            )
            response = await self._list(**params)

            return PriceListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def create(
        self,
        *,
        description: str,
        product_id: str,
        unit_price: Union[UnitPriceType, Dict[str, str]],
        type: Optional[str] = None,
        name: Optional[str] = None,
        billing_cycle: Optional[BillingCycleType] = None,
        trial_period: Optional[BillingCycleType] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None,
        quantity: Optional[QuantityType] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ) -> PriceCreateResponse:
        """|coroutine|

        Create a price.

        Parameters
        ----------

            description: str
               Internal description for this price, not shown to customers. Typically notes for your team.

            product_id: str
                Paddle ID for the product that this price is for, prefixed with `pro_`.

            unit_price: Union[UnitPriceType, Dict[str, str]]
                Base price. This price applies to all customers, except for customers located in countries where you have unit_price_overrides.

            type: Optional[str] = None
                The type of the price.

            name: Optional[str] = None
                Name of this price, shown to customers at checkout and on invoices.

            billing_cycle: Optional[BillingCycleType] = None
                How often this price should be charged.

            trial_period: Optional[BillingCycleType] = None
                Trial period for the product related to this price. The billing cycle begins once the trial period is over. null for no trial period. Requires billing_cycle. If omitted, defaults to null.

            tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None
                How tax is calculated for this price.

            unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None
                Limits on how many times the related product can be purchased at this price.

            quantity: Optional[QuantityType] = None
                The quantity of the price.

            custom_data: Optional[Dict[str, str]] = None
                Arbitrary data you can store with this price.

        Returns
        -------

           A price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    price = await client.prices.create(
                        description="My Price",
                        product_id="prod_1234567890",
                        unit_price=100,
                        type="standard",
                    )
                    print(price)

            asyncio.run(main())
        """

        try:
            kwargs = filter_none_kwargs(
                description=description,
                product_id=product_id,
                unit_price=unit_price,
                type=type,
                name=name,
                billing_cycle=billing_cycle,
                trial_period=trial_period,
                tax_mode=tax_mode,
                unit_price_overrides=unit_price_overrides,
                quantity=quantity,
                custom_data=custom_data,
            )
            response = await self._create(**kwargs)

            return PriceCreateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get(
        self,
        price_id: str,
        *,
        include: Optional[List[Literal["product"]]] = None,
    ) -> PriceGetResponse:
        """
        Get a price.

        Parameters
        ----------

            price_id: str
                The ID of the price to get.

            include: Optional[List[Literal["product"]]] = None
                Include related entities in the response.

        Returns
        -------

            A price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    price = await client.prices.get(price_id="pri_1234567890")
                    print(price)

            asyncio.run(main())
        """

        try:
            kwargs = filter_none_kwargs(include=",".join(include) if include else None)
            response = await self._get(price_id, **kwargs)

            return PriceGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def update(
        self,
        price_id: str,
        *,
        description: Optional[str] = None,
        type: Optional[str] = None,
        name: Optional[str] = None,
        billing_cycle: Optional[BillingCycleType] = None,
        trial_period: Optional[BillingCycleType] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None,
        quantity: Optional[QuantityType] = None,
        status: Optional[Literal["active", "archived"]] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ) -> PriceUpdateResponse:
        """
        Update a price.

        Parameters
        ----------

            price_id: str
                The ID of the price to update.

            description: Optional[str] = None
                Internal description for this price, not shown to customers. Typically notes for your team.

            type: Optional[str] = None
                The type of the price.

            name: Optional[str] = None
                Name of this price, shown to customers at checkout and on invoices.

            billing_cycle: Optional[BillingCycleType] = None
                How often this price should be charged.

            trial_period: Optional[BillingCycleType] = None
                Trial period for the product related to this price. The billing cycle begins once the trial period is over. null for no trial period. Requires billing_cycle. If omitted, defaults to null.

            tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None
                How tax is calculated for this price.

            unit_price_overrides: Optional[List[UnitPriceOverridesType]] = None
                Limits on how many times the related product can be purchased at this price.

            quantity: Optional[QuantityType] = None
                The quantity of the price.

            status: Optional[Literal["active", "archived"]] = None
                The status of the price.

            custom_data: Optional[Dict[str, str]] = None
                Arbitrary data you can store with this price.

        Returns
        -------

            Updated price.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the price is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    price = await client.prices.update(
                        price_id="pri_1234567890",
                        description="My Updated Price",
                    )
                    print(price)

            asyncio.run(main())
        """

        try:
            kwargs = filter_none_kwargs(
                description=description,
                type=type,
                name=name,
                billing_cycle=billing_cycle,
                trial_period=trial_period,
                tax_mode=tax_mode,
                unit_price_overrides=unit_price_overrides,
                quantity=quantity,
                status=status,
                custom_data=custom_data,
            )
            response = await self._update(price_id, **kwargs)

            return PriceUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e
