from dataclasses import dataclass
from typing import Optional, Literal, TypedDict, Dict, Any, List

from pydantic import BaseModel

from paddle.models.responses.shared import (
    BillingCycle,
    ImportMeta,
    MetaWithPagination,
    Meta,
    BillingCycleType,
    DateRange,
)
from paddle.models.responses.prices import PriceData
from paddle.models.responses.products import ProductData


# Typing
class DiscountType(TypedDict):
    id: str
    effective_from: Literal["next_billing_period", "immediately"]


class BillingDetailsType(TypedDict):
    enable_checkout: bool
    purchase_order_number: str
    additional_information: Optional[str] = None
    payment_terms: BillingCycleType


# Models
class Discount(BaseModel):
    id: str
    ends_at: Optional[str] = None
    starts_at: Optional[str] = None


class BillingDetails(BaseModel):
    payment_terms: BillingCycle
    enable_checkout: bool
    purchase_order_number: str
    additional_information: Optional[str] = None


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


class SubscriptionBase(BaseModel):
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
    collection_mode: Literal["automatic", "manual"]
    billing_details: Optional[BillingDetails] = None
    current_billing_period: Optional[DateRange] = None
    billing_cycle: BillingCycle
    scheduled_change: Optional[ScheduledChange] = None
    management_urls: ManagedUrls
    items: List[Item]
    custom_data: Optional[Dict[str, Any]] = None
    import_meta: Optional[ImportMeta] = None


class SubscriptionData(SubscriptionBase):
    id: str


class SubscriptionDataForPaymentMethodUpdate(BaseModel):
    id: str
    status: Literal["draft", "ready", "billed", "paid", "completed", "canceled", "past_due"]
    customer_id: Optional[str] = None
    address_id: Optional[str] = None
    business_id: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
    currency_code: Optional[str] = None
    origin: Literal[
        "api",
        "subscription_charge",
        "subscription_payment_method_change",
        "subscription_recurring",
        "subscription_update",
        "web",
    ]
    subscription_id: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    billing_details: Optional[BillingDetails] = None
    billing_period: Optional[DateRange] = None


class BaseTotal(BaseModel):
    subtotal: str
    tax: str
    total: str


class Total(BaseTotal):
    discount: str


class TransactionTotal(Total):
    credit: str
    credit_to_balance: str
    balance: str
    grand_total: str
    fee: Optional[str] = None
    earnings: Optional[str] = None
    currency_code: str


class AdjustmentTotal(Total):
    earnings: str
    currency_code: str


class TaxRatesUsed(BaseModel):
    tax_rate: str
    totals: Total


class Proration(BaseModel):
    rate: str
    billing_period: DateRange


class LineItem(BaseModel):
    price_id: Optional[str] = None
    quantity: int
    tax_rate: str
    unit_totals: Total
    totals: Total
    product: ProductData
    proration: Optional[Proration] = None


class NextTransactionDetails(BaseModel):
    tax_rates_used: List[TaxRatesUsed]
    totals: TransactionTotal
    line_items: List[LineItem]


class AdjustmentItem(BaseModel):
    item_id: str
    type: Literal["full", "partial", "tax", "proration"]
    amount: Optional[str] = None
    proration: Optional[Proration] = None
    totals: BaseTotal


class Adjustment(BaseModel):
    transaction_id: str
    items: List[AdjustmentItem]
    totals: AdjustmentTotal


class NextTransaction(BaseModel):
    billing_period: DateRange
    details: NextTransactionDetails
    adjustments: List[Adjustment]


class TransactionDetailsTotals(Total):
    credit: str
    credit_to_balance: str
    balance: str
    grand_total: str
    fee: Optional[str] = None
    earnings: Optional[str] = None
    currency_code: str


class RecurringTransactionDetails(BaseModel):
    tax_rates_used: List[TaxRatesUsed]
    totals: TransactionDetailsTotals
    line_items: List[LineItem]


class SubscriptionDataWithTransactions(SubscriptionData):
    next_transaction: Optional[NextTransaction] = None
    recurring_transaction_details: Optional[RecurringTransactionDetails] = None


class Credit(BaseModel):
    amount: str
    currency_code: str


class Result(Credit):
    action: Literal["credit", "charge"]


class UpdateSummary(BaseModel):
    credit: Credit
    charge: Credit
    results: Result


class PreviewUpdateData(SubscriptionBase):
    next_transaction: Optional[NextTransaction] = None
    recurring_transaction_details: Optional[RecurringTransactionDetails] = None
    immediate_transaction: Optional[NextTransaction] = None
    update_summary: Optional[UpdateSummary] = None


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


@dataclass
class SubscriptionGetResponse:
    """
    Response for the Subscription Get endpoint.
    """

    data: SubscriptionDataWithTransactions
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = SubscriptionDataWithTransactions(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class SubscriptionPreviewUpdateResponse:
    """
    Response for the Subscription Preview Update endpoint.
    """

    data: PreviewUpdateData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = PreviewUpdateData(**response["data"])
        self.meta = Meta(**response["meta"])


@dataclass
class SubscriptionUpdateResponse:
    """
    Response for the Subscription Update endpoint.
    """

    data: SubscriptionData
    meta: Meta

    def __init__(self, response: Dict[str, Any]):
        self.data = SubscriptionData(**response["data"])
        self.meta = Meta(**response["meta"])
