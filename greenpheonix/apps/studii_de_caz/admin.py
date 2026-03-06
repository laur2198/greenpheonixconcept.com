from django.contrib import admin
from .models import StudiuDeCaz


@admin.register(StudiuDeCaz)
class StudiuDeCazAdmin(admin.ModelAdmin):
    list_display = ["client", "titlu", "industrie", "canal", "data_proiect", "featured", "activ"]
    list_filter = ["industrie", "canal", "featured", "activ"]
    search_fields = ["titlu", "client"]
    list_editable = ["featured", "activ"]
    prepopulated_fields = {"slug": ("titlu",)}
    fieldsets = [
        ("Informatii generale", {
            "fields": ["titlu", "slug", "client", "industrie", "canal", "data_proiect", "featured", "activ"]
        }),
        ("Continut", {
            "fields": ["descriere_scurta", "descriere_completa", "obiectiv", "solutie", "rezultate"]
        }),
        ("Metrici cheie", {
            "fields": [
                ("metrica_1_label", "metrica_1_valoare"),
                ("metrica_2_label", "metrica_2_valoare"),
                ("metrica_3_label", "metrica_3_valoare"),
                ("metrica_4_label", "metrica_4_valoare"),
            ]
        }),
        ("Imagini", {
            "fields": ["imagine_cover", "imagine_rezultate"]
        }),
    ]
