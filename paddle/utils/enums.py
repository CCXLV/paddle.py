import enum

from typing import Any


class WebhookEvent(enum.Enum):
    """
    Enumeration of all possible Paddle webhook events.

    This enum represents the standardized event types that can be received
    from Paddle's webhook system.
    """

    # Transaction
    TRANSACTION_BILLED = "transaction.billed"
    TRANSACTION_CANCELED = "transaction.canceled"
    TRANSACTION_COMPLETED = "transaction.completed"
    TRANSACTION_CREATED = "transaction.created"
    TRANSACTION_PAID = "transaction.paid"
    TRANSACTION_PAST_DUE = "transaction.past_due"
    TRANSACTION_PAYMENT_FAILED = "transaction.payment_failed"
    TRANSACTION_READY = "transaction.ready"
    TRANSACTION_UPDATED = "transaction.updated"
    TRANSACTION_REVISED = "transaction.revised"

    # Subscription
    SUBSCRIPTION_ACTIVATED = "subscription.activated"
    SUBSCRIPTION_CANCELED = "subscription.canceled"
    SUBSCRIPTION_CREATED = "subscription.created"
    SUBSCRIPTION_IMPORTED = "subscription.imported"
    SUBSCRIPTION_PAST_DUE = "subscription.past_due"
    SUBSCRIPTION_PAUSED = "subscription.paused"
    SUBSCRIPTION_RESUMED = "subscription.resumed"
    SUBSCRIPTION_TRIALING = "subscription.trialing"
    SUBSCRIPTION_UPDATED = "subscription.updated"

    # Product
    PRODUCT_CREATED = "product.created"
    PRODUCT_IMPORTED = "product.imported"
    PRODUCT_UPDATED = "product.updated"

    # Price
    PRICE_CREATED = "price.created"
    PRICE_IMPORTED = "price.imported"
    PRICE_UPDATED = "price.updated"

    # Customer
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_IMPORTED = "customer.imported"
    CUSTOMER_UPDATED = "customer.updated"

    # Payment Method
    PAYMENT_METHOD_SAVED = "payment_method.saved"
    PAYMENT_METHOD_DELETED = "payment_method.deleted"

    # Address
    ADDRESS_CREATED = "address.created"
    ADDRESS_IMPORTED = "address.imported"
    ADDRESS_UPDATED = "address.updated"

    # Business
    BUSINESS_CREATED = "business.created"
    BUSINESS_IMPORTED = "business.imported"
    BUSINESS_UPDATED = "business.updated"

    # Adjustment
    ADJUSTMENT_CREATED = "adjustment.created"
    ADJUSTMENT_UPDATED = "adjustment.updated"

    # Payout
    PAYOUT_CREATED = "payout.created"
    PAYOUT_PAID = "payout.paid"

    # Discount
    DISCOUNT_CREATED = "discount.created"
    DISCOUNT_IMPORTED = "discount.imported"
    DISCOUNT_UPDATED = "discount.updated"

    # Report
    REPORT_CREATED = "report.created"
    REPORT_UPDATED = "report.updated"

    @classmethod
    def _missing_(cls, value: Any) -> None:
        """Handle invalid webhook event values."""
        raise value
