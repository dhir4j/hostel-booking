from decimal import Decimal
from typing import Mapping

from app.payments.base import PaymentProvider


class StripeProvider(PaymentProvider):
    name = 'stripe'

    def create_intent(self, booking, amount: Decimal, currency: str, metadata: dict) -> dict:
        raise NotImplementedError('Stripe not enabled in v1')

    def verify_webhook(self, headers: Mapping[str, str], raw_body: bytes) -> dict:
        raise NotImplementedError('Stripe not enabled in v1')

    def fetch_payment_status(self, provider_ref: str) -> dict:
        raise NotImplementedError('Stripe not enabled in v1')

    def refund(self, provider_ref: str, amount: Decimal | None = None) -> dict:
        raise NotImplementedError('Stripe not enabled in v1')
