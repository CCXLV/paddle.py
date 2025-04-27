from dataclasses import dataclass
from typing import Literal, Optional, List, Dict, Any

from pydantic import BaseModel

from paddle.utils.constants import CURRENCY_CODE, COUNTRY_CODE
from paddle.models.responses.shared import ImportMeta, MetaWithPagination
from paddle.models.responses import ProductData


class BillingCycle(BaseModel):
    frequency: int
    interval: Literal["day", "week", "month", "year"]


class UnitPrice(BaseModel):
    amount: str
    currency_code: CURRENCY_CODE


class UnitPriceOverrides(BaseModel):
    country_codes: List[COUNTRY_CODE]
    unit_price: UnitPrice


class Quantity(BaseModel):
    minimum: int
    maximum: int


class PriceData(BaseModel):
    id: str
    product_id: str
    description: str
    type: Literal["custom", "standard"]
    name: Optional[str] = None
    tax_mode: Literal["account_setting", "external", "internal"]
    billing_cycle: Optional[BillingCycle] = None
    trial_period: Optional[BillingCycle] = None
    unit_price: UnitPrice
    unit_price_overrides: List[UnitPriceOverrides]
    quantity: Quantity
    status: Literal["active", "archived"]
    custom_data: Optional[Dict[str, Any]] = None
    import_meta: Optional[ImportMeta] = None
    created_at: str
    updated_at: str


class PriceDataWithProduct(PriceData):
    product: ProductData


@dataclass
class PriceListResponse:
    """
    Response for the Price List endpoint.
    """

    data: List[PriceDataWithProduct]
    meta: MetaWithPagination

    def __init__(self, response: Dict[str, Any]):
        self.data = [PriceDataWithProduct(**item) for item in response["data"]]
        self.meta = MetaWithPagination(**response["meta"])


# TODO: Add GET, CREATE, UPDATE responses