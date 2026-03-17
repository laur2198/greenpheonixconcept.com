from django.contrib import admin
from .models import Tranzactie, Abonament, Plata, RaportClient, LivrabilClient, PromoTrial, ContractSemnat


@admin.register(Tranzactie)
class TranzactieAdmin(admin.ModelAdmin):
    list_display = ["id_tranzactie", "nume_client", "email_client", "suma", "status", "creat_la"]
    list_filter = ["status", "moneda"]
    search_fields = ["id_tranzactie", "email_client", "nume_client"]
    readonly_fields = ["id_tranzactie", "creat_la", "actualizat_la", "raspuns_complet_bt"]


class PlataInline(admin.TabularInline):
    model = Plata
    extra = 0
    readonly_fields = ["stripe_payment_intent_id", "suma", "valuta", "status", "data_plata", "factura_url"]
    can_delete = False


class RaportClientInline(admin.TabularInline):
    model = RaportClient
    extra = 1
    fields = ["titlu", "luna", "fisier"]


class LivrabilClientInline(admin.TabularInline):
    model = LivrabilClient
    extra = 1
    fields = ["titlu", "categorie", "fisier", "descriere"]


@admin.register(Abonament)
class AbonamentAdmin(admin.ModelAdmin):
    list_display = ["user", "pachet", "status", "data_start", "data_urmatoarei_plati"]
    list_filter = ["status", "pachet"]
    search_fields = ["user__email", "stripe_customer_id"]
    inlines = [PlataInline, RaportClientInline, LivrabilClientInline]


@admin.register(PromoTrial)
class PromoTrialAdmin(admin.ModelAdmin):
    list_display = [
        "email_client", "nume_client", "status", "suma", "data_start",
        "data_expirare", "convertit_la_pachet", "creat_la"
    ]
    list_filter = ["status", "convertit_la_pachet", "pachet_dorit_dupa_trial"]
    search_fields = ["email_client", "nume_client", "stripe_payment_intent_id"]
    readonly_fields = ["stripe_payment_intent_id", "creat_la", "data_start", "data_expirare"]
    fieldsets = (
        ("Date client", {
            "fields": ("user", "nume_client", "email_client", "telefon_client", "nisa_client")
        }),
        ("Trial", {
            "fields": ("status", "data_start", "data_expirare", "pachet_dorit_dupa_trial", "convertit_la_pachet")
        }),
        ("Plată Stripe", {
            "fields": ("stripe_payment_intent_id", "suma", "valuta")
        }),
        ("Note interne", {
            "fields": ("nota_interna",)
        }),
        ("Sistem", {
            "fields": ("creat_la",),
            "classes": ("collapse",),
        }),
    )


@admin.register(ContractSemnat)
class ContractSemnatAdmin(admin.ModelAdmin):
    list_display = ["numar_contract", "client_email", "client_nume_complet", "pachet", "status", "data_semnare"]
    list_filter = ["status", "pachet", "data_semnare"]
    search_fields = ["client_email", "client_nume_complet", "client_firma", "id_contract"]
    readonly_fields = ["id_contract", "data_semnare", "ip_semnare", "pachet_snapshot"]
    fieldsets = (
        ("Contract", {
            "fields": ("id_contract", "pachet", "status", "stripe_session_id")
        }),
        ("Date client", {
            "fields": ("client_nume_complet", "client_email", "client_telefon", "client_firma", "client_cui", "client_adresa")
        }),
        ("Semnătură electronică", {
            "fields": ("semnatura_text", "ip_semnare", "data_semnare")
        }),
        ("Snapshot pachet", {
            "fields": ("pachet_snapshot",),
            "classes": ("collapse",),
        }),
    )
