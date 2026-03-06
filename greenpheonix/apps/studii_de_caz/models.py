from django.db import models
from django.utils.text import slugify


class StudiuDeCaz(models.Model):
    INDUSTRIE_CHOICES = [
        ("transport", "Transport & Logistică"),
        ("fmcg", "FMCG / Alimentar"),
        ("retail", "Retail"),
        ("servicii", "Servicii"),
        ("alt", "Altele"),
    ]
    CANAL_CHOICES = [
        ("meta", "Meta Ads"),
        ("google", "Google Ads"),
        ("tiktok", "TikTok Ads"),
        ("web", "Web Development"),
        ("mix", "Mix canale"),
    ]

    titlu = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    client = models.CharField(max_length=100)
    industrie = models.CharField(max_length=50, choices=INDUSTRIE_CHOICES)
    canal = models.CharField(max_length=50, choices=CANAL_CHOICES)
    descriere_scurta = models.CharField(max_length=300,
        help_text="Apare în card pe pagina de listing")
    descriere_completa = models.TextField()
    obiectiv = models.TextField(help_text="Ce și-a propus clientul")
    solutie = models.TextField(help_text="Ce am implementat")
    rezultate = models.TextField(help_text="Cifre și rezultate concrete")
    imagine_cover = models.ImageField(upload_to="studii/covers/", blank=True)
    imagine_rezultate = models.ImageField(upload_to="studii/results/", blank=True)
    data_proiect = models.DateField()
    featured = models.BooleanField(default=False, help_text="Afișat pe homepage")
    activ = models.BooleanField(default=True)
    creat_la = models.DateTimeField(auto_now_add=True)

    metrica_1_label = models.CharField(max_length=50, blank=True, help_text="Ex: Total Impressions")
    metrica_1_valoare = models.CharField(max_length=50, blank=True, help_text="Ex: 400K+")
    metrica_2_label = models.CharField(max_length=50, blank=True)
    metrica_2_valoare = models.CharField(max_length=50, blank=True)
    metrica_3_label = models.CharField(max_length=50, blank=True)
    metrica_3_valoare = models.CharField(max_length=50, blank=True)
    metrica_4_label = models.CharField(max_length=50, blank=True)
    metrica_4_valoare = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Studiu de caz"
        verbose_name_plural = "Studii de caz"
        ordering = ["-featured", "-data_proiect"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titlu)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} — {self.titlu}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("studii_de_caz:detail", kwargs={"slug": self.slug})

    def get_metrici(self):
        metrici = []
        for i in range(1, 5):
            label = getattr(self, f"metrica_{i}_label")
            valoare = getattr(self, f"metrica_{i}_valoare")
            if label and valoare:
                metrici.append({"label": label, "valoare": valoare})
        return metrici
