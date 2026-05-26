from django.db import models


class Testimonial(models.Model):
    RATING_CHOICES = [(i, f"{i} stele") for i in range(1, 6)]

    client_nume = models.CharField(max_length=100, help_text="Numele clientului")
    client_firma = models.CharField(max_length=150, blank=True, help_text="Firma / Brand (opțional)")
    client_industrie = models.CharField(max_length=100, blank=True, help_text="Ex: Transport, eCommerce")
    client_foto = models.ImageField(upload_to="testimoniale/", blank=True, null=True)
    text = models.TextField(help_text="Citatul clientului")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    rezultat_cheie = models.CharField(
        max_length=100, blank=True,
        help_text="Ex: +230% rezervări | 4.8x ROAS — apare ca highlight"
    )
    activ = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Afișat în prima secțiune pe homepage")
    ordine = models.PositiveIntegerField(default=0)
    creat_la = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimoniale"
        ordering = ["ordine", "-creat_la"]

    def __str__(self):
        return f"{self.client_nume} ({self.client_firma or self.client_industrie or '—'})"


class ClientLogo(models.Model):
    nume = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="clienti/logos/", blank=True, null=True)
    url_site = models.URLField(blank=True, help_text="Link către site-ul clientului (opțional)")
    ordine = models.PositiveIntegerField(default=0)
    activ = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Logo client"
        verbose_name_plural = "Logo-uri clienți"
        ordering = ["ordine"]

    def __str__(self):
        return self.nume
