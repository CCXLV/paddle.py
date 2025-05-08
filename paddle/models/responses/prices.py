from dataclasses import dataclass
from typing import Literal, Optional, List, Dict, Any, TYPE_CHECKING, TypedDict

from pydantic import BaseModel

from paddle.utils.constants import CURRENCY_CODE, COUNTRY_CODE
from paddle.models.responses.shared import ImportMeta, MetaWithPagination, Meta, BillingCycle

if TYPE_CHECKING:
    from paddle.models.responses.products import ProductData


# Typing
class BillingCycleType(TypedDict):
    frequency: int
    interval: Literal["day", "week", "month", "year"]


class UnitPriceType(TypedDict):
    amount: str
    currency_code: CURRENCY_CODE


class UnitPriceOverridesType(TypedDict):
    country_codes: List[COUNTRY_CODE]
    unit_price: UnitPriceType


class QuantityType(TypedDict):
    minimum: int
    maximum: int


# Models
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
    billing_cycle: Optional[BillingCycle] = None
    trial_period: Optional[BillingCycle] = None
    tax_mode: Literal["account_setting", "external", "internal"]
    unit_price: UnitPrice
    unit_price_overrides: List[UnitPriceOverrides]
    quantity: Quantity
    status: Literal["active", "archived"]
    custom_data: Optional[Dict[str, Any]] = None
    import_meta: Optional[ImportMeta] = None
    created_at: str
    updated_at: str


class PriceDataWithProduct(PriceData):
    product: Optional["ProductData"] = None


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


@dataclass
class PriceCreateResponse:
    """ "
    Response for the Price Create endpoint.
    """

    data: PriceData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = PriceData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class PriceGetResponse:
    """
    Response for the Price Get endpoint.
    """

    data: PriceDataWithProduct
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = PriceDataWithProduct(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class PriceUpdateResponse:
    """
    Response for the Price Update endpoint.
    """

    data: PriceData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = PriceData(**response["data"])
        self.meta = Meta(**response["meta"])
