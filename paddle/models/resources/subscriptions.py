"""
Paddle Subscriptions API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Dict, Any, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.subscriptions import (
    SubscriptionListResponse,
    SubscriptionGetResponse,
    SubscriptionPreviewUpdateResponse,
    DiscountType,
    BillingDetailsType,
    SubscriptionUpdateResponse,
)

from paddle.utils.decorators import validate_params
from paddle.utils.helpers import filter_none_kwargs

from paddle.exceptions import PaddleAPIError, create_paddle_error


class SubscriptionBase(ResourceBase):
    """Base resource for Paddle Subscriptions API endpoints."""

    def __init__(self, client: Union[Client, AsyncClient]):
        self._client = client

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list products."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to get a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _preview_update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to preview an update to a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get_transaction_to_update_payment_method(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to get a transaction to update a payment method."""
        raise NotImplementedError("Subclasses must implement this method")

    def _preview_charge(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to list transactions for a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _charge(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to charge a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _activate(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to activate a trialing subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _pause(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to pause a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _resume(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to resume a paused subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    def _cancel(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to cancel a subscription."""
        raise NotImplementedError("Subclasses must implement this method")

    @validate_params
    def list(
        self,
        *,
        address_id: Optional[List[str]] = None,
        after: Optional[str] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        customer_id: Optional[List[str]] = None,
        id: Optional[List[str]] = None,
        order_by: Optional[Literal["id[ASC]", "id[DESC]"]] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        price_id: Optional[List[str]] = None,
        scheduled_change_action: Optional[List[Literal["cancel", "pause", "resume"]]] = None,
        status: Optional[
            List[Literal["active", "canceled", "past_due", "paused", "trialing"]]
        ] = None,
    ) -> SubscriptionListResponse:
        try:
            kwargs = filter_none_kwargs(
                address_id=",".join(address_id) if address_id else None,
                after=after,
                collection_mode=collection_mode,
                customer_id=",".join(customer_id) if customer_id else None,
                id=",".join(id) if id else None,
                order_by=order_by,
                per_page=per_page,
                price_id=",".join(price_id) if price_id else None,
                scheduled_change_action=(
                    ",".join(scheduled_change_action) if scheduled_change_action else None
                ),
                status=",".join(status) if status else None,
            )
            response = self._list(**kwargs)

            return SubscriptionListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get(
        self,
        subscription_id: str,
        *,
        include: Optional[
            List[Literal["next_transaction", "recurring_transaction_details"]]
        ] = None,
    ) -> SubscriptionGetResponse:
        try:
            kwargs = filter_none_kwargs(
                include=",".join(include) if include else None,
            )
            response = self._get(subscription_id, **kwargs)

            return SubscriptionGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def preview_update(
        self,
        subscription_id: str,
        *,
        customer_id: Optional[str] = None,
        address_id: Optional[str] = None,
        business_id: Optional[str] = None,
        currency_code: Optional[str] = None,
        next_billed_at: Optional[str] = None,
        discount: Optional[DiscountType] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        billing_details: Optional[BillingDetailsType] = None,
        scheduled_change: None = None,
        items: Optional[List[Dict[str, Any]]] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        proration_billing_mode: Optional[
            Literal[
                "prorated_immediately",
                "prorated_next_billing_period",
                "full_immediately",
                "full_next_billing_period",
                "do_not_bill",
            ]
        ] = None,
        on_payment_failure: Optional[Literal["prevent_change", "apply_change"]] = None,
    ) -> SubscriptionPreviewUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                customer_id=customer_id,
                address_id=address_id,
                business_id=business_id,
                currency_code=currency_code,
                next_billed_at=next_billed_at,
                discount=discount,
                collection_mode=collection_mode,
                billing_details=billing_details,
                scheduled_change=scheduled_change,
                items=items,
                custom_data=custom_data,
                proration_billing_mode=proration_billing_mode,
                on_payment_failure=on_payment_failure,
            )
            response = self._preview_update(subscription_id, **kwargs)

            return SubscriptionPreviewUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def update(
        self,
        subscription_id: str,
        *,
        customer_id: Optional[str] = None,
        address_id: Optional[str] = None,
        business_id: Optional[str] = None,
        currency_code: Optional[str] = None,
        next_billed_at: Optional[str] = None,
        discount: Optional[DiscountType] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        billing_details: Optional[BillingDetailsType] = None,
        scheduled_change: None = None,
        items: Optional[List[Dict[str, Any]]] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        proration_billing_mode: Optional[
            Literal[
                "prorated_immediately",
                "prorated_next_billing_period",
                "full_immediately",
                "full_next_billing_period",
                "do_not_bill",
            ]
        ] = None,
        on_payment_failure: Optional[Literal["prevent_change", "apply_change"]] = None,
    ) -> SubscriptionUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                customer_id=customer_id,
                address_id=address_id,
                business_id=business_id,
                currency_code=currency_code,
                next_billed_at=next_billed_at,
                discount=discount,
                collection_mode=collection_mode,
                billing_details=billing_details,
                scheduled_change=scheduled_change,
                items=items,
                custom_data=custom_data,
                proration_billing_mode=proration_billing_mode,
                on_payment_failure=on_payment_failure,
            )
            response = self._update(subscription_id, **kwargs)

            return SubscriptionUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get_transaction_to_update_payment_method(
        self,
        subscription_id: str,
    ) -> SubscriptionGetResponse:
        try:
            response = self._get_transaction_to_update_payment_method(subscription_id)

            return SubscriptionUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def cancel(
        self,
        subscription_id: str,
        *,
        effective_from: Optional[Literal["next_billing_period", "immediately"]] = None,
    ) -> SubscriptionUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                effective_from=effective_from,
            )
            response = self._cancel(subscription_id, **kwargs)

            return SubscriptionUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    # TODO: Add remaining endpoints


class Subscription(SubscriptionBase):
    """Paddle Subscriptions API endpoints."""

    def __init__(self, client: Union[Client, AsyncClient]):
        super().__init__(client)

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list subscriptions."""
        return self._client._request(
            method="GET",
            path="/subscriptions",
            params=kwargs,
        )

    def _get(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a subscription."""
        return self._client._request(
            method="GET",
            path=f"/subscriptions/{subscription_id}",
            params=kwargs,
        )

    def _preview_update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to preview an update to a subscription."""
        return self._client._request(
            method="PATCH",
            path=f"/subscriptions/{subscription_id}/preview",
            json=kwargs,
        )

    def _update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a subscription."""
        return self._client._request(
            method="PATCH",
            path=f"/subscriptions/{subscription_id}",
            json=kwargs,
        )

    def _get_transaction_to_update_payment_method(self, subscription_id: str) -> Dict[str, Any]:
        """Internal method to get a transaction to update a payment method."""
        return self._client._request(
            method="GET",
            path=f"/subscriptions/{subscription_id}/update-payment-method-transaction",
        )

    def _cancel(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to cancel a subscription."""
        return self._client._request(
            method="POST",
            path=f"/subscriptions/{subscription_id}/cancel",
            json=kwargs,
        )


class AsyncSubscription(SubscriptionBase):
    """Async Paddle Subscriptions API endpoints."""

    def __init__(self, client: AsyncClient):
        super().__init__(client)

    async def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list subscriptions."""
        return await self._client._request(
            method="GET",
            path="/subscriptions",
            params=kwargs,
        )

    async def _get(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a subscription."""
        return await self._client._request(
            method="GET",
            path=f"/subscriptions/{subscription_id}",
            params=kwargs,
        )

    async def _preview_update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to preview an update to a subscription."""
        return await self._client._request(
            method="PATCH",
            path=f"/subscriptions/{subscription_id}/preview",
            json=kwargs,
        )

    async def _update(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a subscription."""
        return await self._client._request(
            method="PATCH",
            path=f"/subscriptions/{subscription_id}",
            json=kwargs,
        )

    async def _get_transaction_to_update_payment_method(
        self, subscription_id: str
    ) -> Dict[str, Any]:
        """Internal method to get a transaction to update a payment method."""
        return await self._client._request(
            method="GET",
            path=f"/subscriptions/{subscription_id}/update-payment-method-transaction",
        )

    async def _cancel(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to cancel a subscription."""
        return await self._client._request(
            method="POST",
            path=f"/subscriptions/{subscription_id}/cancel",
            json=kwargs,
        )

    @validate_params
    async def list(
        self,
        *,
        address_id: Optional[List[str]] = None,
        after: Optional[str] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        customer_id: Optional[List[str]] = None,
        id: Optional[List[str]] = None,
        order_by: Optional[Literal["id[ASC]", "id[DESC]"]] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        price_id: Optional[List[str]] = None,
        scheduled_change_action: Optional[List[Literal["cancel", "pause", "resume"]]] = None,
        status: Optional[
            List[Literal["active", "canceled", "past_due", "paused", "trialing"]]
        ] = None,
    ) -> SubscriptionListResponse:
        try:
            kwargs = filter_none_kwargs(
                address_id=",".join(address_id) if address_id else None,
                after=after,
                collection_mode=collection_mode,
                customer_id=",".join(customer_id) if customer_id else None,
                id=",".join(id) if id else None,
                order_by=order_by,
                per_page=per_page,
                price_id=",".join(price_id) if price_id else None,
                scheduled_change_action=(
                    ",".join(scheduled_change_action) if scheduled_change_action else None
                ),
                status=",".join(status) if status else None,
            )
            response = await self._list(**kwargs)

            return SubscriptionListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get(
        self,
        subscription_id: str,
        *,
        include: Optional[
            List[Literal["next_transaction", "recurring_transaction_details"]]
        ] = None,
    ) -> SubscriptionGetResponse:
        try:
            kwargs = filter_none_kwargs(
                include=",".join(include) if include else None,
            )
            response = await self._get(subscription_id, **kwargs)

            return SubscriptionGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def preview_update(
        self,
        subscription_id: str,
        *,
        customer_id: Optional[str] = None,
        address_id: Optional[str] = None,
        business_id: Optional[str] = None,
        currency_code: Optional[str] = None,
        next_billed_at: Optional[str] = None,
        discount: Optional[DiscountType] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        billing_details: Optional[BillingDetailsType] = None,
        scheduled_change: None = None,
        items: Optional[List[Dict[str, Any]]] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        proration_billing_mode: Optional[
            Literal[
                "prorated_immediately",
                "prorated_next_billing_period",
                "full_immediately",
                "full_next_billing_period",
                "do_not_bill",
            ]
        ] = None,
        on_payment_failure: Optional[Literal["prevent_change", "apply_change"]] = None,
    ) -> SubscriptionPreviewUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                customer_id=customer_id,
                address_id=address_id,
                business_id=business_id,
                currency_code=currency_code,
                next_billed_at=next_billed_at,
                discount=discount,
                collection_mode=collection_mode,
                billing_details=billing_details,
                scheduled_change=scheduled_change,
                items=items,
                custom_data=custom_data,
                proration_billing_mode=proration_billing_mode,
                on_payment_failure=on_payment_failure,
            )
            response = await self._preview_update(subscription_id, **kwargs)

            return SubscriptionPreviewUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def update(
        self,
        subscription_id: str,
        *,
        customer_id: Optional[str] = None,
        address_id: Optional[str] = None,
        business_id: Optional[str] = None,
        currency_code: Optional[str] = None,
        next_billed_at: Optional[str] = None,
        discount: Optional[DiscountType] = None,
        collection_mode: Optional[Literal["automatic", "manual"]] = None,
        billing_details: Optional[BillingDetailsType] = None,
        scheduled_change: None = None,
        items: Optional[List[Dict[str, Any]]] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        proration_billing_mode: Optional[
            Literal[
                "prorated_immediately",
                "prorated_next_billing_period",
                "full_immediately",
                "full_next_billing_period",
                "do_not_bill",
            ]
        ] = None,
        on_payment_failure: Optional[Literal["prevent_change", "apply_change"]] = None,
    ) -> SubscriptionUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                customer_id=customer_id,
                address_id=address_id,
                business_id=business_id,
                currency_code=currency_code,
                next_billed_at=next_billed_at,
                discount=discount,
                collection_mode=collection_mode,
                billing_details=billing_details,
                scheduled_change=scheduled_change,
                items=items,
                custom_data=custom_data,
                proration_billing_mode=proration_billing_mode,
                on_payment_failure=on_payment_failure,
            )
            response = await self._update(subscription_id, **kwargs)

            return SubscriptionUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get_transaction_to_update_payment_method(
        self,
        subscription_id: str,
    ) -> SubscriptionGetResponse:
        try:
            response = await self._get_transaction_to_update_payment_method(subscription_id)

            return SubscriptionGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def cancel(
        self,
        subscription_id: str,
        *,
        effective_from: Optional[Literal["next_billing_period", "immediately"]] = None,
    ) -> SubscriptionUpdateResponse:
        try:
            kwargs = filter_none_kwargs(
                effective_from=effective_from,
            )
            response = await self._cancel(subscription_id, **kwargs)

            return SubscriptionUpdateResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    # TODO: Add remaining endpoints
