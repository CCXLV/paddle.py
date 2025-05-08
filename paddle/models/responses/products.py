from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any, List, TYPE_CHECKING

from pydantic import BaseModel

from paddle.utils.constants import TAX_CATEGORY
from paddle.models.responses.shared import (
    ImportMeta,
    Meta,
    MetaWithPagination,
)

if TYPE_CHECKING:
    from paddle.models.responses.prices import PriceData


class ProductData(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: str
    tax_category: TAX_CATEGORY
    image_url: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
    status: Literal["active", "archived"]
    import_meta: Optional[ImportMeta] = None
    created_at: str
    updated_at: str


class ProductDataWithPrices(ProductData):
    prices: Optional[List["PriceData"]] = None


@dataclass
class ProductListResponse:
    """
    Response for the Product List endpoint.
    """

    data: List[ProductDataWithPrices]
    meta: MetaWithPagination

    def __init__(self, response: Dict[str, Any]):
        self.data = [ProductDataWithPrices(**item) for item in response["data"]]
        self.meta = MetaWithPagination(**response["meta"])


@dataclass
class ProductCreateResponse:
    """
    Response for the Product Create, Update endpoint.
    """

    data: ProductData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = ProductData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class ProductGetResponse:
    """
    Response for the Product Get endpoint.
    """

    data: ProductDataWithPrices
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = ProductDataWithPrices(**response["data"])
        self.meta = Meta(**response["meta"])
