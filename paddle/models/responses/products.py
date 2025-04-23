from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any, List

from pydantic import BaseModel

from paddle.utils.constants import CURRENCY_CODE, COUNTRY_CODE, TAX_CATEGORY


class Pagination(BaseModel):
    per_page: int
    next: str
    has_more: bool
    estimated_total: int


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


class ImportMeta(BaseModel):
    imported_from: Literal["paddle_classic"]


class PriceData(BaseModel):
    id: str
    product_id: str
    description: str
    type: Literal["custom", "standard"]
    tax_mode: Literal["account_setting", "external", "internal"]
    unit_price: UnitPrice
    quantity: Quantity
    status: Literal["active", "archived"]
    created_at: str
    updated_at: str
    billing_cycle: Optional[BillingCycle] = None
    trial_period: Optional[BillingCycle] = None
    unit_price_overrides: Optional[List[UnitPriceOverrides]] = None
    custom_data: Optional[Dict[str, Any]] = None


class Prices(BaseModel):
    data: Optional[List[PriceData]] = None


class ProductData(BaseModel):
    id: str
    name: str
    tax_category: TAX_CATEGORY
    type: str
    status: Literal["active", "archived"]
    created_at: str
    updated_at: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
    import_meta: Optional[ImportMeta] = None


class ProductDataWithPrices(ProductData):
    prices: Optional[Prices] = None


class ProductMeta(BaseModel):
    request_id: str


class ProductMetaWithPagination(ProductMeta):
    pagination: Pagination


@dataclass
class ProductListResponse:
    """
    Response for the Product List endpoint.
    """

    data: List[ProductDataWithPrices]
    meta: ProductMetaWithPagination

    def __init__(self, response: Dict[str, Any]):
        self.data = [ProductDataWithPrices(**item) for item in response["data"]]
        self.meta = ProductMetaWithPagination(**response["meta"])


@dataclass
class ProductCreateResponse:
    """
    Response for the Product Create endpoint.
    """

    data: ProductData
    meta: ProductMeta

    def __init__(self, response: Dict[str, Any]):
        self.data = ProductData(**response["data"])
        self.meta = ProductMeta(**response["meta"])


@dataclass
class ProductGetResponse:
    """
    Response for the Product Get endpoint.
    """

    data: ProductDataWithPrices
    meta: ProductMeta

    def __init__(self, response: Dict[str, Any]):
        self.data = ProductDataWithPrices(**response["data"])
        self.meta = ProductMeta(**response["meta"])
