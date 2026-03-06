from django.contrib import admin
from .models import Tranzactie


@admin.register(Tranzactie)
class TranzactieAdmin(admin.ModelAdmin):
    list_display = ["id_tranzactie", "nume_client", "email_client", "suma", "status", "creat_la"]
    list_filter = ["status", "moneda"]
    search_fields = ["id_tranzactie", "email_client", "nume_client"]
    readonly_fields = ["id_tranzactie", "creat_la", "actualizat_la", "raspuns_complet_bt"]
