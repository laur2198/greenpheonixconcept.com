from django.contrib import admin
from .models import Pachet


@admin.register(Pachet)
class PachetAdmin(admin.ModelAdmin):
    list_display = ["nume", "tier", "pret_lunar", "recomandat", "activ", "ordine"]
    list_filter = ["tier", "recomandat", "activ"]
    list_editable = ["ordine", "activ", "recomandat"]
    search_fields = ["nume"]
