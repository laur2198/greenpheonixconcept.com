import requests
import hashlib
import hmac
import json
from django.conf import settings


class BTPay:
    """
    Client pentru API-ul BT Pay (Banca Transilvania).
    Credentialele reale se obtin de la BT dupa aprobarea contului merchant.
    In modul sandbox, foloseste credentialele de test furnizate de BT.
    """

    SANDBOX_URL = "https://sandbox.btpay.ro/api/v1"
    PRODUCTION_URL = "https://api.btpay.ro/api/v1"

    def __init__(self):
        self.merchant_id = settings.BT_PAY_MERCHANT_ID
        self.secret_key = settings.BT_PAY_SECRET_KEY
        self.terminal_id = settings.BT_PAY_TERMINAL_ID
        self.environment = settings.BT_PAY_ENVIRONMENT
        self.base_url = (self.SANDBOX_URL if self.environment == "sandbox"
                        else self.PRODUCTION_URL)

    def _generate_signature(self, data: dict) -> str:
        payload = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def initiate_payment(self, order_id: str, amount: float,
                        description: str, return_url: str,
                        client_email: str) -> dict:
        data = {
            "merchantId": self.merchant_id,
            "terminalId": self.terminal_id,
            "orderId": order_id,
            "amount": int(amount * 100),
            "currency": "RON",
            "description": description,
            "returnUrl": return_url,
            "email": client_email,
        }
        data["signature"] = self._generate_signature(data)
        response = requests.post(
            f"{self.base_url}/payments/initiate",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def verify_payment(self, order_id: str) -> dict:
        data = {
            "merchantId": self.merchant_id,
            "orderId": order_id,
        }
        data["signature"] = self._generate_signature(data)
        response = requests.post(
            f"{self.base_url}/payments/status",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
