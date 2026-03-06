from django.db import models
import uuid


class Tranzactie(models.Model):
    STATUS_CHOICES = [
        ("pending", "În așteptare"),
        ("completed", "Finalizată"),
        ("failed", "Eșuată"),
        ("refunded", "Rambursată"),
    ]

    id_tranzactie = models.UUIDField(default=uuid.uuid4, unique=True)
    bt_order_id = models.CharField(max_length=100, blank=True)
    bt_response_code = models.CharField(max_length=20, blank=True)
    suma = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default="RON")
    descriere_serviciu = models.CharField(max_length=200)
    nume_client = models.CharField(max_length=100)
    email_client = models.EmailField()
    telefon_client = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    creat_la = models.DateTimeField(auto_now_add=True)
    actualizat_la = models.DateTimeField(auto_now=True)
    raspuns_complet_bt = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Tranzacție"
        verbose_name_plural = "Tranzacții"
        ordering = ["-creat_la"]

    def __str__(self):
        return f"{self.id_tranzactie} | {self.suma} RON | {self.status}"
