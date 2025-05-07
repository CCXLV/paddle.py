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


class CustomerCreditBalance(BaseModel):
    available: str
    reserved: str
    used: str


class CustomerCreditBalanceData(BaseModel):
    customer_id: str
    currency_code: str
    balance: CustomerCreditBalance


class CustomerAuthTokenData(BaseModel):
    customer_auth_token: str
    expires_at: str


class CustomerPortalGeneral(BaseModel):
    overview: str


class CustomerPortalSubscription(BaseModel):
    id: str
    cancel_subscription: str
    update_subscription_payment_method: str


class CustomerPortalUrls(BaseModel):
    general: CustomerPortalGeneral
    subscriptions: List[CustomerPortalSubscription]


class CustomerPortalSessionData(BaseModel):
    id: str
    customer_id: str
    urls: CustomerPortalUrls
    created_at: str


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


@dataclass
class CustomerCreditBalanceResponse:
    """
    Response for the Customer Credit Balance endpoint.
    """

    data: List[CustomerCreditBalanceData]
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = [CustomerCreditBalanceData(**item) for item in response["data"]]
        self.meta = Meta(**response["meta"])


@dataclass
class CustomerAuthTokenResponse:
    """
    Response for the Customer Auth Token endpoint.
    """

    data: CustomerAuthTokenData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = CustomerAuthTokenData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class CustomerPortalSessionResponse:
    """
    Response for the Customer Portal Session endpoint.
    """

    data: CustomerPortalSessionData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = CustomerPortalSessionData(**response["data"])
        self.meta = Meta(**response["meta"])
