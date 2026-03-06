from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("despre/", views.despre, name="despre"),
    path("termeni/", views.termeni, name="termeni"),
    path("confidentialitate/", views.confidentialitate, name="confidentialitate"),
    path("anulare/", views.anulare, name="anulare"),
]
