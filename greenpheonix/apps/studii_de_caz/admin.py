from django.contrib import admin
from .models import StudiuDeCaz


@admin.register(StudiuDeCaz)
class StudiuDeCazAdmin(admin.ModelAdmin):
    list_display = ["titlu", "client", "nisa", "featured", "activ", "creat_la"]
    list_filter = ["featured", "activ", "industrie", "canal"]
    search_fields = ["titlu", "client"]
    list_editable = ["featured", "activ"]
    prepopulated_fields = {"slug": ("titlu",)}
    fieldsets = [
        ("Info generale", {
            "fields": ["titlu", "slug", "client", "industrie", "canal", "nisa", "perioada", "data_proiect", "featured", "activ"]
        }),
        ("Conținut", {
            "fields": ["descriere_scurta", "descriere_completa", "problema", "obiectiv", "solutie", "rezultate"]
        }),
        ("Metrici cheie", {
            "fields": [
                ("metrica_1_label", "metrica_1_valoare"),
                ("metrica_2_label", "metrica_2_valoare"),
                ("metrica_3_label", "metrica_3_valoare"),
                ("metrica_4_label", "metrica_4_valoare"),
            ]
        }),
        ("Media", {
            "fields": ["imagine_cover", "logo_client", "imagine_rezultate"]
        }),
    ]
