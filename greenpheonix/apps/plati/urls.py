from django.urls import path
from . import views

app_name = "plati"

urlpatterns = [
    # BT Pay (existent)
    path("", views.initiate_payment, name="checkout"),
    path("callback/<int:pk>/", views.payment_callback, name="callback"),
    # Contract digital — înainte de plată
    path("contract/<slug:pachet_slug>/", views.contract_view, name="contract"),
    path("contract/<slug:pachet_slug>/semneaza/", views.semneaza_contract, name="semneaza_contract"),
    # Stripe abonamente
    path("stripe/checkout/<slug:pachet_slug>/", views.checkout, name="checkout_stripe"),
    path("stripe/webhook/", views.webhook, name="stripe_webhook"),
    path("anuleaza/", views.anuleaza_abonament, name="anuleaza_abonament"),
    path("portal/", views.portal_client, name="portal_client"),
]
