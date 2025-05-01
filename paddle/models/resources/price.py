"""
Paddle Prices API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Any, Dict, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.price import (
    PriceListResponse,
    PriceCreateResponse,
    UnitPrice,
    BillingCycle,
    UnitPriceOverrides,
    Quantity,
)

from paddle.utils.decorators import validate_params
from paddle.utils.helpers import filter_none_kwargs


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
        # TODO: Add docstrings

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
        response = self._list(**params)

        return PriceListResponse(response)

    @validate_params
    def create(
        self,
        *,
        description: str,
        product_id: str,
        unit_price: Union[UnitPrice, Dict[str, str]],
        type: Optional[str] = None,
        billing_cycle: Optional[Union[BillingCycle, Dict[str, str]]] = None,
        trial_period: Optional[Union[BillingCycle, Dict[str, str]]] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverrides]] = None,
        quantity: Optional[Quantity] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ):
        # TODO: Add docstrings

        kwargs = filter_none_kwargs(
            description=description,
            product_id=product_id,
            unit_price=unit_price,
            type=type,
            billing_cycle=billing_cycle,
            trial_period=trial_period,
            tax_mode=tax_mode,
            unit_price_overrides=unit_price_overrides,
            quantity=quantity,
            custom_data=custom_data,
        )
        response = self._create(**kwargs)

        return PriceCreateResponse(response)

    def get(self):
        # TODO
        pass

    def update(self):
        # TODO
        pass


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
        # TODO: Add docstrings

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

    @validate_params
    async def create(
        self,
        *,
        description: str,
        product_id: str,
        unit_price: Union[UnitPrice, Dict[str, str]],
        type: Optional[str] = None,
        billing_cycle: Optional[Union[BillingCycle, Dict[str, str]]] = None,
        trial_period: Optional[Union[BillingCycle, Dict[str, str]]] = None,
        tax_mode: Optional[Literal["account_setting", "external", "internal"]] = None,
        unit_price_overrides: Optional[List[UnitPriceOverrides]] = None,
        quantity: Optional[Quantity] = None,
        custom_data: Optional[Dict[str, str]] = None,
    ):
        # TODO: Add docstrings

        kwargs = filter_none_kwargs(
            description=description,
            product_id=product_id,
            unit_price=unit_price,
            type=type,
            billing_cycle=billing_cycle,
            trial_period=trial_period,
            tax_mode=tax_mode,
            unit_price_overrides=unit_price_overrides,
            quantity=quantity,
            custom_data=custom_data,
        )
        response = await self._create(**kwargs)

        return PriceCreateResponse(response)
