from django.urls import path
from . import views

app_name = "plati"

urlpatterns = [
    path("", views.initiate_payment, name="checkout"),
    path("callback/<int:pk>/", views.payment_callback, name="callback"),
]
