"""
Paddle Prices API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Any, Dict, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.price import PriceListResponse

from paddle.utils.helpers import filter_none_kwargs


class PriceBase(ResourceBase):
    """
    Paddle Prices API endpoints.
    """

    def __init__(self, client: Union[Client, AsyncClient]):
        super().__init__(client)

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

    def create(self):
        pass

    def get(self):
        pass

    def update(self):
        pass
