from django.urls import path
from . import views

app_name = "servicii"

urlpatterns = [
    path("pachete/", views.pachete, name="pachete"),
    path("ads/", views.ads, name="ads"),
    path("web/", views.web, name="web"),
    path("audit/", views.audit, name="audit"),
]
