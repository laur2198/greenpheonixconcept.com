from django.db import models


class Pachet(models.Model):
    """Modelul pentru pachetele de servicii afișate pe pagina de prețuri."""
    TIER_CHOICES = [
        ("starter", "Starter"),
        ("business", "Business"),
        ("pro", "Pro"),
    ]

    nume = models.CharField(max_length=50)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    pret_lunar = models.DecimalField(max_digits=8, decimal_places=2, help_text="Preț lunar în EUR")
    pret_setup = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Cost setup o singură dată, în EUR")
    descriere = models.TextField(help_text="1-2 propoziții scurte despre pachet")
    features = models.JSONField(default=list, help_text="Listă de string-uri — bullet points afișate pe card")
    recomandat = models.BooleanField(default=False, help_text="Cardul evidențiat cu border auriu")
    activ = models.BooleanField(default=True)
    ordine = models.PositiveIntegerField(default=0, help_text="Ordine afișare (crescător)")

    class Meta:
        verbose_name = "Pachet"
        verbose_name_plural = "Pachete"
        ordering = ["ordine"]

    def __str__(self):
        return f"{self.nume} — {self.pret_lunar}€/lună"

    def get_slug(self):
        """Returnează slug-ul tier-ului pentru URL-uri Stripe checkout."""
        return self.tier
