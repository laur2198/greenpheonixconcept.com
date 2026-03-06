from django.urls import path
from . import views

app_name = "studii_de_caz"

urlpatterns = [
    path("", views.lista, name="list"),
    path("<slug:slug>/", views.detail, name="detail"),
]
