from django.contrib import admin
from .models import Testimonial, ClientLogo


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_nume", "client_firma", "rating", "rezultat_cheie", "featured", "activ", "ordine")
    list_editable = ("activ", "featured", "ordine")
    list_filter = ("activ", "featured", "rating")
    search_fields = ("client_nume", "client_firma", "text")


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("nume", "activ", "ordine")
    list_editable = ("activ", "ordine")
