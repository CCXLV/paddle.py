from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any, List

from pydantic import BaseModel

from paddle.models.responses.shared import ImportMeta, MetaWithPagination, Meta


class CustomerData(BaseModel):
    id: str
    name: Optional[str] = None
    email: str
    marketing_consent: bool
    status: Literal["active", "archived"]
    custom_data: Optional[Dict[str, Any]] = None
    locale: str
    created_at: str
    updated_at: str
    import_meta: Optional[ImportMeta] = None


@dataclass
class CustomerListResponse:
    """
    Response for the Customer List endpoint.
    """

    data: List[CustomerData]
    meta: MetaWithPagination

    def __init__(self, response: Dict[str, Any]):
        self.data = [CustomerData(**item) for item in response["data"]]
        self.meta = MetaWithPagination(**response["meta"])


@dataclass
class CustomerCreateResponse:
    """
    Response for the Customer Create endpoint.
    """

    data: CustomerData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = CustomerData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class CustomerGetResponse:
    """
    Response for the Customer Get endpoint.
    """

    data: CustomerData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = CustomerData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class CustomerUpdateResponse:
    """
    Response for the Customer Update endpoint.
    """

    data: CustomerData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = CustomerData(**response["data"])
        self.meta = Meta(**response["meta"])
