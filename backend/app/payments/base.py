import hashlib
import hmac
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import ClassVar, Mapping


class PaymentProvider(ABC):
    name: ClassVar[str]

    @abstractmethod
    def create_intent(self, booking, amount: Decimal, currency: str, metadata: dict) -> dict:
        """Returns {provider_ref, client_secret (optional), status='pending', raw}"""

    @abstractmethod
    def verify_webhook(self, headers: Mapping[str, str], raw_body: bytes) -> dict:
        """Verifies HMAC signature. Returns {provider_ref, status, amount, currency, raw}.
        Raises ValueError on bad signature."""

    @abstractmethod
    def fetch_payment_status(self, provider_ref: str) -> dict:
        """Returns {provider_ref, status}"""

    @abstractmethod
    def refund(self, provider_ref: str, amount: Decimal | None = None) -> dict:
        """Returns {status, provider_ref, amount}"""
