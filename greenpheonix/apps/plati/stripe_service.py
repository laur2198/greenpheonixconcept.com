"""
Servicii pentru integrarea cu Stripe API.
Toate funcțiile de comunicare cu Stripe sunt centralizate aici.
"""
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def creeaza_customer(email, nume):
    """Creează un customer nou în Stripe și returnează obiectul Customer."""
    customer = stripe.Customer.create(
        email=email,
        name=nume,
    )
    return customer


def creeaza_abonament(customer_id, price_id, success_url, cancel_url):
    """
    Creează o sesiune de Checkout pentru abonament.
    Returnează sesiunea Stripe — folosim Checkout hosted, nu Billing direct.
    """
    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def anuleaza_abonament(subscription_id):
    """Anulează abonamentul la sfârșitul perioadei curente (cancel_at_period_end=True)."""
    subscription = stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True,
    )
    return subscription


def obtine_facturi(customer_id):
    """Returnează lista de facturi pentru un customer Stripe."""
    invoices = stripe.Invoice.list(customer=customer_id, limit=20)
    return invoices.data


def creeaza_portal_session(customer_id, return_url):
    """Creează o sesiune de Customer Portal Stripe pentru self-service."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return session
