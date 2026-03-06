from django.contrib import admin
from .models import Articol, Categorie, Tag


@admin.register(Articol)
class ArticolAdmin(admin.ModelAdmin):
    list_display = ["titlu", "categorie", "status", "data_publicare"]
    list_filter = ["status", "categorie"]
    search_fields = ["titlu", "continut"]
    prepopulated_fields = {"slug": ("titlu",)}
    list_editable = ["status"]
    filter_horizontal = ["taguri"]


admin.site.register(Categorie)
admin.site.register(Tag)
