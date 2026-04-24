import hashlib
import hmac as hmac_module
import json
import uuid
from decimal import Decimal

from flask import current_app

from app.payments.base import PaymentProvider


class MockProvider(PaymentProvider):
    name = 'mock'

    def create_intent(self, booking, amount: Decimal, currency: str, metadata: dict) -> dict:
        provider_ref = f"mock_{uuid.uuid4().hex}"
        return {
            'provider_ref': provider_ref,
            'client_secret': f"mock_secret_{provider_ref}",
            'status': 'pending',
            'raw': {'booking_id': metadata.get('booking_id')},
        }

    def verify_webhook(self, headers, raw_body: bytes) -> dict:
        secret = current_app.config.get('WEBHOOK_SECRET', '')
        expected = hmac_module.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
        provided = headers.get('X-Mock-Signature', '')
        if not hmac_module.compare_digest(expected, provided):
            raise ValueError('Invalid mock webhook signature')
        try:
            event = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise ValueError('Invalid webhook body') from exc
        required = {'provider_ref', 'status'}
        if not required.issubset(event.keys()):
            raise ValueError(f'Missing fields: {required - event.keys()}')
        return {
            'provider_ref': event['provider_ref'],
            'status': event['status'],  # 'success' or 'failed'
            'amount': Decimal(str(event.get('amount', '0'))),
            'currency': event.get('currency', 'INR'),
            'raw': event,
        }

    def fetch_payment_status(self, provider_ref: str) -> dict:
        return {'provider_ref': provider_ref, 'status': 'success'}

    def refund(self, provider_ref: str, amount: Decimal | None = None) -> dict:
        return {'status': 'refunded', 'provider_ref': provider_ref, 'amount': amount}
