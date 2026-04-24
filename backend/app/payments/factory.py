from flask import current_app

from app.payments.base import PaymentProvider
from app.payments.mock import MockProvider
from app.payments.razorpay_provider import RazorpayProvider
from app.payments.stripe_provider import StripeProvider

_REGISTRY: dict[str, type[PaymentProvider]] = {
    MockProvider.name: MockProvider,
    StripeProvider.name: StripeProvider,
    RazorpayProvider.name: RazorpayProvider,
}


def get_provider(name: str | None = None) -> PaymentProvider:
    if name is None:
        name = current_app.config.get('PAYMENT_PROVIDER', 'mock')
    provider_class = _REGISTRY.get(name)
    if not provider_class:
        raise ValueError(f'Unknown payment provider: {name}')
    return provider_class()
