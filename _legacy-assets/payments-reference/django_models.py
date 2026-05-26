from django.db import models
from django.contrib.auth.models import User
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


class Abonament(models.Model):
    """Abonamentul activ al unui client la un pachet de servicii."""
    STATUS_CHOICES = [
        ("activ", "Activ"),
        ("anulat", "Anulat"),
        ("suspendat", "Suspendat"),
        ("trial", "Trial"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="abonamente")
    pachet = models.ForeignKey("servicii.Pachet", on_delete=models.PROTECT, related_name="abonamente")
    stripe_subscription_id = models.CharField(max_length=200, blank=True)
    stripe_customer_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="trial")
    data_start = models.DateTimeField()
    data_urmatoarei_plati = models.DateTimeField(null=True, blank=True)
    creat_la = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonament"
        verbose_name_plural = "Abonamente"
        ordering = ["-creat_la"]

    def __str__(self):
        return f"{self.user.email} — {self.pachet.nume} ({self.status})"


class Plata(models.Model):
    """O plată individuală asociată unui abonament."""
    STATUS_CHOICES = [
        ("reusit", "Reușit"),
        ("esuat", "Eșuat"),
        ("pending", "În așteptare"),
    ]

    abonament = models.ForeignKey(Abonament, on_delete=models.CASCADE, related_name="plati")
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    suma = models.DecimalField(max_digits=8, decimal_places=2)
    valuta = models.CharField(max_length=3, default="eur")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    data_plata = models.DateTimeField()
    factura_url = models.URLField(blank=True, help_text="Link factură din Stripe")

    class Meta:
        verbose_name = "Plată"
        verbose_name_plural = "Plăți"
        ordering = ["-data_plata"]

    def __str__(self):
        return f"{self.abonament.user.email} — {self.suma}€ ({self.status})"


class RaportClient(models.Model):
    """Raport lunar de performanță uploadat de admin pentru un client."""
    abonament = models.ForeignKey(Abonament, on_delete=models.CASCADE, related_name="rapoarte")
    titlu = models.CharField(max_length=200, help_text="Ex: Raport Mai 2026")
    luna = models.DateField(help_text="Prima zi a lunii de raportare")
    fisier = models.FileField(upload_to="rapoarte/")
    creat_la = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Raport client"
        verbose_name_plural = "Rapoarte clienți"
        ordering = ["-luna"]

    def __str__(self):
        return f"{self.titlu} — {self.abonament.user.email}"


class LivrabilClient(models.Model):
    """Fișier livrat clientului — reclame, documente, etc."""
    CATEGORIE_CHOICES = [
        ("reclame", "Reclame"),
        ("rapoarte", "Rapoarte"),
        ("documente", "Documente"),
        ("altele", "Altele"),
    ]

    abonament = models.ForeignKey(Abonament, on_delete=models.CASCADE, related_name="livrabile")
    titlu = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="altele")
    fisier = models.FileField(upload_to="livrabile/")
    descriere = models.TextField(blank=True)
    creat_la = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Livrabil client"
        verbose_name_plural = "Livrabile clienți"
        ordering = ["-creat_la"]

    def __str__(self):
        return f"{self.titlu} — {self.abonament.user.email}"


class ContractSemnat(models.Model):
    """Contract de prestări servicii semnat electronic de client înainte de plată."""
    STATUS_CHOICES = [
        ("semnat", "Semnat"),
        ("platit", "Plătit"),
        ("anulat", "Anulat"),
    ]

    id_contract = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    pachet = models.ForeignKey(
        "servicii.Pachet", on_delete=models.PROTECT, related_name="contracte"
    )

    # Date client
    client_nume_complet = models.CharField(max_length=150)
    client_email = models.EmailField()
    client_telefon = models.CharField(max_length=20, blank=True)
    client_firma = models.CharField(max_length=200, blank=True, help_text="Numele firmei (opțional PFA/SRL)")
    client_cui = models.CharField(max_length=20, blank=True, help_text="CUI / CNP (opțional)")
    client_adresa = models.TextField(blank=True)

    # Semnătură electronică simplă (eIDAS Art. 3(10))
    semnatura_text = models.CharField(max_length=150, help_text="Numele tastat de client ca semnătură")
    ip_semnare = models.GenericIPAddressField(null=True, blank=True)
    data_semnare = models.DateTimeField(auto_now_add=True)

    # Conținut contract salvat la momentul semnării (snapshot)
    pachet_snapshot = models.JSONField(default=dict, help_text="Datele pachetului la momentul semnării")

    # Plată
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="semnat")
    stripe_session_id = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Contract Semnat"
        verbose_name_plural = "Contracte Semnate"
        ordering = ["-data_semnare"]

    def __str__(self):
        return f"#{str(self.id_contract)[:8].upper()} — {self.client_email} — {self.pachet.nume}"

    def numar_contract(self):
        return f"GPC-{self.data_semnare.year}-{str(self.id_contract)[:6].upper()}"


class PromoTrial(models.Model):
    """Pachet Promo 7 Zile — 50€ one-time, acces la servicii de testare."""
    STATUS_CHOICES = [
        ("pending", "În așteptare plată"),
        ("activ", "Activ"),
        ("expirat", "Expirat"),
        ("convertit", "Convertit la pachet"),
        ("refundat", "Rambursat"),
    ]
    PACHET_DORIT_CHOICES = [
        ("starter", "Starter"),
        ("business", "Business"),
        ("pro", "Pro"),
        ("nedecis", "Încă nedecis"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="promo_trials"
    )
    nume_client = models.CharField(max_length=100)
    email_client = models.EmailField()
    telefon_client = models.CharField(max_length=20, blank=True)
    nisa_client = models.CharField(max_length=200, blank=True, help_text="Domeniu/industrie client")
    pachet_dorit_dupa_trial = models.CharField(
        max_length=20, choices=PACHET_DORIT_CHOICES, default="nedecis"
    )
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    suma = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    valuta = models.CharField(max_length=3, default="eur")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    data_start = models.DateTimeField(null=True, blank=True)
    data_expirare = models.DateTimeField(null=True, blank=True)
    convertit_la_pachet = models.BooleanField(default=False)
    nota_interna = models.TextField(blank=True, help_text="Note interne (nu se afișează clientului)")
    creat_la = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promo Trial 7 Zile"
        verbose_name_plural = "Promo Trials"
        ordering = ["-creat_la"]

    def __str__(self):
        return f"{self.email_client} — Trial 7 zile ({self.status})"

    def este_activ(self):
        from django.utils import timezone
        if self.status != "activ" or not self.data_expirare:
            return False
        return timezone.now() < self.data_expirare

    def zile_ramase(self):
        from django.utils import timezone
        if not self.data_expirare:
            return 0
        delta = self.data_expirare - timezone.now()
        return max(0, delta.days)
