import json
import time
import hmac
import hashlib

from pydantic import BaseModel

from paddle.utils.decorators import validate_params
from paddle.utils.enums import WebhookEvent


class WebhookSignatureData(BaseModel):
    event_type: WebhookEvent


class Webhooks:
    def __init__(self):
        pass

    @validate_params
    def verify_signature(
        self,
        *,
        signature: str,
        secret: str,
        request_body: str,
    ) -> WebhookSignatureData:
        """Verify a webhook signature.

        Args:
            signature: The signature string from the webhook request
            secret: The webhook secret key
            request_body_raw: The raw request body

        Returns:
            WebhookSignatureData: A validated webhook signature data object

        Raises:
            ValueError: If the signature is invalid or expired
        """
        signature_parts = signature.split(";")
        if len(signature_parts) != 2:
            raise ValueError("Invalid signature")

        timestamp = signature_parts[0].split("=")[1]
        signature = signature_parts[1].split("=")[1]

        if not timestamp or not signature:
            raise ValueError("Invalid signature")

        try:
            timestamp = int(timestamp)
        except ValueError as e:
            raise ValueError("Invalid timestamp") from e

        if abs(time.time() - timestamp) > 5:
            raise ValueError("Signature expired")

        signed_payload = f"{timestamp}:{request_body}"
        computed_hash = hmac.new(
            secret.encode(), signed_payload.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed_hash, signature):
            raise ValueError("Invalid signature")

        request_body_json = json.loads(request_body)

        return WebhookSignatureData(event_type=WebhookEvent(request_body_json["event_type"]))
