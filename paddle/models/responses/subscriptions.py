from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any, List

from pydantic import BaseModel

from paddle.models.responses.shared import BillingCycle, ImportMeta, MetaWithPagination
from paddle.models.responses.prices import PriceData
from paddle.models.responses.products import ProductData


class Discount(BaseModel):
    id: str
    ends_at: Optional[str] = None
    starts_at: Optional[str] = None


class BillingDetails(BaseModel):
    payment_terms: BillingCycle
    enable_checkout: bool
    purchase_order_number: str
    additional_information: Optional[str] = None


class DateRange(BaseModel):
    starts_at: str
    ends_at: str


class ScheduledChange(BaseModel):
    action: Literal["cancel", "pause", "resume"]
    effective_at: str
    resume_at: Optional[str] = None


class ManagedUrls(BaseModel):
    update_payment_method: Optional[str] = None
    cancel: str


class Item(BaseModel):
    status: Literal["active", "inactive", "trialing"]
    quantity: int
    recurring: bool
    created_at: str
    updated_at: str
    previously_billed_at: Optional[str] = None
    next_billed_at: Optional[str] = None
    trial_dates: Optional[DateRange] = None
    price: PriceData
    product: ProductData


class SubscriptionData(BaseModel):
    id: str
    status: Literal["active", "canceled", "past_due", "paused", "trialing"]
    customer_id: str
    address_id: str
    business_id: Optional[str] = None
    currency_code: str
    created_at: str
    updated_at: str
    started_at: Optional[str] = None
    first_billed_at: Optional[str] = None
    next_billed_at: Optional[str] = None
    paused_at: Optional[str] = None
    canceled_at: Optional[str] = None
    discount: Optional[Discount] = None
    collection_mode = Literal["automatic", "manual"]
    billing_details: Optional[BillingDetails] = None
    current_billing_period: Optional[DateRange] = None
    billing_cycle: BillingCycle
    scheduled_change: Optional[ScheduledChange] = None
    management_urls: ManagedUrls
    items: List[Item]
    custom_data: Optional[Dict[str, Any]] = None
    import_meta: Optional[ImportMeta] = None


class Total(BaseModel):
    subtotal: str
    discount: str
    tax: str
    total: str


class TransactionTotal(Total):
    credit: str
    credit_to_balance: str
    balance: str
    grand_total: str
    fee: Optional[str] = None
    earnings: Optional[str] = None
    currency_code: str


class TaxRatesUsed(BaseModel):
    tax_rate: str
    totals: Total


# TODO: Finish this
class NextTransactionDetails(BaseModel):
    tax_rates_used: List[TaxRatesUsed]
    totals: TransactionTotal


# TODO: Finish this
class NextTransaction(BaseModel):
    billing_period: DateRange
    details: NextTransactionDetails


# TODO: Finish this
class SubscriptionDataWithTransactions(SubscriptionData):
    next_transaction: Optional[NextTransaction] = None


@dataclass
class SubscriptionListResponse:
    """
    Response for the Subscription List endpoint.
    """

    data: List[SubscriptionData]
    meta: MetaWithPagination

    def __init__(self, response: Dict[str, Any]):
        self.data = [SubscriptionData(**item) for item in response["data"]]
        self.meta = MetaWithPagination(**response["meta"])
