from datetime import datetime
from typing import Dict, Any

class PaymentService:
    """
    Service to handle payments via local providers (Fedapay, Kkapay) and Stripe.
    """
    
    def __init__(self):
        # API Keys would be loaded from env
        pass

    async def create_checkout_session(self, 
                                      provider: str, 
                                      amount: int, 
                                      currency: str = "XOF", 
                                      user_email: str = "") -> Dict[str, Any]:
        """
        Create a payment session for the specified provider.
        """
        if provider == "fedapay":
            return self._init_fedapay(amount, currency, user_email)
        elif provider == "kkapay":
            return self._init_kkapay(amount, currency, user_email)
        elif provider == "stripe":
            return self._init_stripe(amount, currency, user_email)
        else:
            raise ValueError(f"Provider {provider} not supported.")

    def _init_fedapay(self, amount, currency, email):
        # Fedapay implementation stub
        return {
            "checkout_url": f"https://checkout.fedapay.com/m/stub-{amount}",
            "transaction_id": "fed_12345",
            "provider": "fedapay"
        }

    def _init_kkapay(self, amount, currency, email):
        # Kkapay implementation stub
        return {
            "checkout_url": f"https://kkapay.bj/pay/stub-{amount}",
            "transaction_id": "kka_67890",
            "provider": "kkapay"
        }

    def _init_stripe(self, amount, currency, email):
        # Stripe implementation stub
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/stub-{amount}",
            "transaction_id": "st_54321",
            "provider": "stripe"
        }

    def generate_ohada_invoice(self, transaction_data: Dict[str, Any]) -> str:
        """
        Generate a text/HTML stub for an OHADA compliant invoice.
        """
        return f"""
        FACTURE N° {transaction_data.get('transaction_id')}
        Conformité OHADA
        Montant: {transaction_data.get('amount')} {transaction_data.get('currency')}
        Date: {transaction_data.get('date')}
        """
