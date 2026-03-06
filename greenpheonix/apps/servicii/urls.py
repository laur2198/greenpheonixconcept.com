from django.urls import path
from . import views

app_name = "servicii"

urlpatterns = [
    path("ads/", views.ads, name="ads"),
    path("web/", views.web, name="web"),
    path("audit/", views.audit, name="audit"),
]
