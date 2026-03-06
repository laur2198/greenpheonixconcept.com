from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Categorie(models.Model):
    nume = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descriere = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categorii"

    def __str__(self):
        return self.nume


class Tag(models.Model):
    nume = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.nume


class Articol(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("publicat", "Publicat")]

    titlu = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL,
        null=True, related_name="articole")
    taguri = models.ManyToManyField(Tag, blank=True)
    rezumat = models.CharField(max_length=300,
        help_text="Apare în listing și meta description")
    continut = models.TextField()
    imagine_cover = models.ImageField(upload_to="blog/covers/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    data_publicare = models.DateTimeField(default=timezone.now)
    creat_la = models.DateTimeField(auto_now_add=True)
    actualizat_la = models.DateTimeField(auto_now=True)

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name_plural = "Articole"
        ordering = ["-data_publicare"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titlu)
        if not self.meta_title:
            self.meta_title = self.titlu[:70]
        if not self.meta_description:
            self.meta_description = self.rezumat[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titlu

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:detail", kwargs={"slug": self.slug})
