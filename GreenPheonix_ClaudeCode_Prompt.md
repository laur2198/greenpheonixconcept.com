# 🚀 GREEN PHEONIX CONCEPT — Claude Code Master Prompt
# Fișier complet pentru construirea site-ului Django de la zero
# Autor: Laurențiu Bogdan | greenpheonixconcept.com
# Data: Martie 2026

---

## 📋 INSTRUCȚIUNI PENTRU CLAUDE CODE

Acest fișier conține TOATE informațiile necesare pentru a construi site-ul
greenpheonixconcept.com în Django. Citește-l integral înainte de a scrie
orice linie de cod.

Lucrează în ordine: Setup → Models → Views → Templates → Static → Integrări.
La fiecare pas, rulează serverul și verifică că funcționează înainte de a continua.

---

## 1. STACK TEHNOLOGIC

- **Backend**: Django 5.x + Python 3.12
- **Baza de date**: PostgreSQL (producție) / SQLite (development local)
- **Frontend**: HTML5 + CSS3 + Vanilla JS (fără framework JS greu)
- **Deployment**: Gunicorn + Nginx (sau Railway/Render pentru început)
- **Email**: SMTP Gmail sau SendGrid
- **Plăți**: BT Pay (Banca Transilvania) — API REST
- **Static files**: WhiteNoise (development) → AWS S3 sau Cloudflare R2 (producție)
- **SEO**: django-meta + sitemap framework inclus în Django

---

## 2. STRUCTURA PROIECTULUI

```
greenpheonix/
├── manage.py
├── requirements.txt
├── .env                        # Nu se pune în git!
├── .env.example
├── .gitignore
├── README.md
│
├── config/                     # Setări proiect
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Setări comune
│   │   ├── development.py      # SQLite, DEBUG=True
│   │   └── production.py      # PostgreSQL, DEBUG=False
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                   # Home, Despre, pagini statice
│   │   ├── migrations/
│   │   ├── templates/core/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── sitemaps.py
│   │
│   ├── servicii/               # Pagini servicii + pachete
│   │   ├── migrations/
│   │   ├── templates/servicii/
│   │   ├── models.py           # Serviciu, Pachet, PretServiciu
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── studii_de_caz/          # Portfolio + rezultate
│   │   ├── migrations/
│   │   ├── templates/studii_de_caz/
│   │   ├── models.py           # StudiuDeCaz, MetricaStudiu
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── blog/                   # Articole, categorii, taguri
│   │   ├── migrations/
│   │   ├── templates/blog/
│   │   ├── models.py           # Articol, Categorie, Tag
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── contact/                # Formular contact + email
│   │   ├── templates/contact/
│   │   ├── forms.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── plati/                  # Integrare BT Pay
│       ├── migrations/
│       ├── templates/plati/
│       ├── models.py           # Tranzactie, Factura
│       ├── views.py
│       ├── urls.py
│       └── bt_pay.py           # Client API BT Pay
│
├── static/
│   ├── css/
│   │   ├── main.css            # Stiluri globale
│   │   ├── components.css      # Carduri, butoane, navbar
│   │   └── pages/             # CSS specific per pagină
│   ├── js/
│   │   ├── main.js
│   │   └── components/
│   ├── img/
│   │   ├── logo_gpc.svg
│   │   ├── hero_gpc.svg
│   │   └── og-default.jpg      # 1200x630px pentru Open Graph
│   └── video/
│       └── studiu_bpd.mp4
│
├── media/                      # Upload-uri utilizatori
│
└── templates/
    ├── base.html               # Template de bază cu SEO complet
    ├── includes/
    │   ├── navbar.html
    │   ├── footer.html
    │   ├── cookie_banner.html
    │   └── schema_markup.html
    ├── robots.txt
    └── sitemap_index.xml
```

---

## 3. REQUIREMENTS.TXT

```
Django==5.1.4
psycopg2-binary==2.9.9
python-decouple==3.8
whitenoise==6.7.0
Pillow==10.4.0
django-meta==2.4.0
gunicorn==23.0.0
requests==2.32.3
sendgrid==6.11.0
django-crispy-forms==2.3
crispy-bootstrap5==2024.2
django-storages==1.14.4
boto3==1.35.0
```

---

## 4. FIȘIER .ENV (template)

```env
# Django
SECRET_KEY=django-insecure-SCHIMBA-CU-O-CHEIE-PUTERNICA
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,greenpheonixconcept.com

# Database (development)
DATABASE_URL=sqlite:///db.sqlite3

# Database (production PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/greenpheonix_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=contact@greenpheonixconcept.com
EMAIL_HOST_PASSWORD=parola-aplicatie-gmail
DEFAULT_FROM_EMAIL=contact@greenpheonixconcept.com
CONTACT_RECIPIENT_EMAIL=contact@greenpheonixconcept.com

# BT Pay (Banca Transilvania)
BT_PAY_MERCHANT_ID=COMPLETEAZA_DE_LA_BT
BT_PAY_SECRET_KEY=COMPLETEAZA_DE_LA_BT
BT_PAY_TERMINAL_ID=COMPLETEAZA_DE_LA_BT
BT_PAY_ENVIRONMENT=sandbox   # sandbox sau production

# AWS S3 (opțional, pentru media files în producție)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

---

## 5. MODELS COMPLETE

### apps/studii_de_caz/models.py
```python
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
    featured = models.BooleanField(default=False,
        help_text="Afișat pe homepage")
    activ = models.BooleanField(default=True)
    creat_la = models.DateTimeField(auto_now_add=True)

    # Metrici cheie (afișate vizual pe pagina studiului)
    metrica_1_label = models.CharField(max_length=50, blank=True,
        help_text="Ex: Total Impressions")
    metrica_1_valoare = models.CharField(max_length=50, blank=True,
        help_text="Ex: 400K+")
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
```

### apps/blog/models.py
```python
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
        default="draft")
    data_publicare = models.DateTimeField(default=timezone.now)
    creat_la = models.DateTimeField(auto_now_add=True)
    actualizat_la = models.DateTimeField(auto_now=True)

    # SEO fields
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
```

### apps/plati/models.py
```python
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
        default="pending")
    creat_la = models.DateTimeField(auto_now_add=True)
    actualizat_la = models.DateTimeField(auto_now=True)
    raspuns_complet_bt = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Tranzacție"
        verbose_name_plural = "Tranzacții"
        ordering = ["-creat_la"]

    def __str__(self):
        return f"{self.id_tranzactie} | {self.suma} RON | {self.status}"
```

---

## 6. URLS COMPLETE (config/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("servicii/", include("apps.servicii.urls")),
    path("studii-de-caz/", include("apps.studii_de_caz.urls")),
    path("blog/", include("apps.blog.urls")),
    path("contact/", include("apps.contact.urls")),
    path("plati/", include("apps.plati.urls")),

    # SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 7. TEMPLATE BASE.HTML (SEO complet)

```html
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Title & Meta SEO -->
    <title>{% block title %}Green Pheonix Concept | Marketing Digital Brașov{% endblock %}</title>
    <meta name="description" content="{% block meta_description %}Agenție marketing digital Brașov. Campanii Meta Ads, Google Ads, web development. Rezultate măsurabile.{% endblock %}">
    <meta name="keywords" content="{% block meta_keywords %}marketing digital brasov, meta ads, google ads, web development{% endblock %}">
    <meta name="author" content="Laurențiu Bogdan — Green Pheonix Concept">
    <meta name="robots" content="index, follow">

    <!-- Canonical -->
    <link rel="canonical" href="{% block canonical %}{{ request.build_absolute_uri }}{% endblock %}">

    <!-- Open Graph -->
    <meta property="og:type" content="{% block og_type %}website{% endblock %}">
    <meta property="og:site_name" content="Green Pheonix Concept">
    <meta property="og:url" content="{{ request.build_absolute_uri }}">
    <meta property="og:title" content="{% block og_title %}Green Pheonix Concept — Marketing Digital{% endblock %}">
    <meta property="og:description" content="{% block og_description %}Sisteme digitale care convertesc. Brașov, România.{% endblock %}">
    <meta property="og:image" content="{% block og_image %}{% load static %}{% static "img/og-default.jpg" %}{% endblock %}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="ro_RO">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{% block twitter_title %}Green Pheonix Concept{% endblock %}">
    <meta name="twitter:description" content="{% block twitter_description %}Marketing digital Brașov.{% endblock %}">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{% load static %}{% static "img/logo_gpc.svg" %}">

    <!-- CSS -->
    {% load static %}
    <link rel="stylesheet" href="{% static "css/main.css" %}">
    {% block extra_css %}{% endblock %}

    <!-- Schema Markup -->
    {% include "includes/schema_markup.html" %}
    {% block extra_schema %}{% endblock %}
</head>
<body class="{% block body_class %}{% endblock %}">

    {% include "includes/navbar.html" %}
    {% include "includes/cookie_banner.html" %}

    <main>
        {% block content %}{% endblock %}
    </main>

    {% include "includes/footer.html" %}

    <!-- JS -->
    <script src="{% static "js/main.js" %}"></script>
    {% block extra_js %}{% endblock %}

    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BP0J2SJTP1"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag("js", new Date());
        gtag("config", "G-BP0J2SJTP1");
    </script>

    <!-- Meta Pixel -->
    <script>
        !function(f,b,e,v,n,t,s){/* Meta Pixel code */}(window, document,"script",
        "https://connect.facebook.net/en_US/fbevents.js");
        fbq("init", "1250834263629342");
        fbq("track", "PageView");
    </script>
</body>
</html>
```

---

## 8. VIEWS PRINCIPALE

### apps/core/views.py
```python
from django.shortcuts import render
from apps.studii_de_caz.models import StudiuDeCaz
from apps.blog.models import Articol

def home(request):
    studii_featured = StudiuDeCaz.objects.filter(
        featured=True, activ=True)[:3]
    articole_recente = Articol.objects.filter(
        status="publicat")[:3]
    context = {
        "studii_featured": studii_featured,
        "articole_recente": articole_recente,
        "page_title": "Agenție Marketing Digital Brașov | Green Pheonix Concept",
        "meta_description": "Campanii Meta Ads, Google Ads și web development. Rezultate măsurabile, prețuri transparente.",
    }
    return render(request, "core/home.html", context)

def despre(request):
    return render(request, "core/despre.html", {
        "page_title": "Despre Laurențiu Bogdan — Marketing Specialist Brașov",
        "meta_description": "Specialist marketing digital și web developer din Brașov. Certificat Google & Meta Ads. Fondator Green Pheonix Concept SRL.",
    })

def termeni(request):
    return render(request, "core/termeni.html")

def confidentialitate(request):
    return render(request, "core/confidentialitate.html")

def anulare(request):
    return render(request, "core/anulare.html")
```

### apps/contact/views.py
```python
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Email către tine
            send_mail(
                subject=f"[GPC] Solicitare nouă: {cd["serviciu_interes"]}",
                message=f"""
Nume: {cd["nume"]}
Email: {cd["email"]}
Telefon: {cd.get("telefon", "—")}
Serviciu: {cd["serviciu_interes"]}
Buget: {cd.get("buget", "—")}
Mesaj: {cd["mesaj"]}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
            # Email confirmare către client
            send_mail(
                subject="Mulțumim! Am primit solicitarea ta — Green Pheonix Concept",
                message=f"""Bună {cd["nume"]},

Mulțumim că ne-ai contactat! Am primit solicitarea ta și îți vom răspunde în maximum 24 de ore.

Dacă ai urgențe, ne poți scrie pe WhatsApp: +40 793 650 902

Cu drag,
Laurențiu Bogdan
Green Pheonix Concept SRL
greenpheonixconcept.com""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cd["email"]],
                fail_silently=True,
            )
            messages.success(request,
                "Mulțumim! Am primit solicitarea ta. Îți răspundem în 24h.")
            return redirect("contact:succes")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})

def succes(request):
    return render(request, "contact/succes.html")
```

### apps/contact/forms.py
```python
from django import forms

SERVICII_CHOICES = [
    ("", "— Selectează serviciul —"),
    ("meta_ads", "Meta Ads (Facebook & Instagram)"),
    ("google_ads", "Google Ads"),
    ("tiktok_ads", "TikTok Ads"),
    ("meta_google", "Meta Ads + Google Ads"),
    ("audit", "Audit campanii existente"),
    ("landing_page", "Landing Page"),
    ("site_prezentare", "Site de prezentare"),
    ("consultanta", "Consultanță / Strategie"),
    ("altceva", "Altceva"),
]

BUGET_CHOICES = [
    ("", "— Buget lunar estimat (opțional) —"),
    ("sub_500", "Sub 500 RON/lună"),
    ("500_1000", "500 – 1.000 RON/lună"),
    ("1000_2000", "1.000 – 2.000 RON/lună"),
    ("2000_5000", "2.000 – 5.000 RON/lună"),
    ("peste_5000", "Peste 5.000 RON/lună"),
]

class ContactForm(forms.Form):
    nume = forms.CharField(max_length=100, label="Nume complet",
        widget=forms.TextInput(attrs={"placeholder": "Nume Prenume"}))
    email = forms.EmailField(label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "email@firma.ro"}))
    telefon = forms.CharField(max_length=20, required=False, label="Telefon",
        widget=forms.TextInput(attrs={"placeholder": "+40 7XX XXX XXX"}))
    serviciu_interes = forms.ChoiceField(choices=SERVICII_CHOICES,
        label="Serviciu de interes")
    buget = forms.ChoiceField(choices=BUGET_CHOICES, required=False,
        label="Buget estimat")
    mesaj = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 5,
        "placeholder": "Descrie pe scurt afacerea ta și ce îți dorești să obții..."}),
        label="Mesaj")
    gdpr = forms.BooleanField(
        label="Sunt de acord cu Politica de Confidențialitate",
        error_messages={"required": "Trebuie să accepți politica de confidențialitate."})
```

---

## 9. INTEGRARE BT PAY (apps/plati/bt_pay.py)

```python
import requests
import hashlib
import hmac
import json
from django.conf import settings

class BTPay:
    """
    Client pentru API-ul BT Pay (Banca Transilvania).
    Documentație: https://btpay.ro/docs (solicită acces de la BT)

    IMPORTANT: Credențialele reale se obțin de la BT după aprobarea contului merchant.
    În modul sandbox, folosește credențialele de test furnizate de BT.
    """

    SANDBOX_URL = "https://sandbox.btpay.ro/api/v1"
    PRODUCTION_URL = "https://api.btpay.ro/api/v1"

    def __init__(self):
        self.merchant_id = settings.BT_PAY_MERCHANT_ID
        self.secret_key = settings.BT_PAY_SECRET_KEY
        self.terminal_id = settings.BT_PAY_TERMINAL_ID
        self.environment = settings.BT_PAY_ENVIRONMENT
        self.base_url = (self.SANDBOX_URL if self.environment == "sandbox"
                        else self.PRODUCTION_URL)

    def _generate_signature(self, data: dict) -> str:
        """Generează semnătura HMAC pentru request."""
        payload = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def initiate_payment(self, order_id: str, amount: float,
                        description: str, return_url: str,
                        client_email: str) -> dict:
        """
        Inițiază o plată nouă.
        Returnează URL-ul de redirect pentru client.
        """
        data = {
            "merchantId": self.merchant_id,
            "terminalId": self.terminal_id,
            "orderId": order_id,
            "amount": int(amount * 100),  # în bani (cenți)
            "currency": "RON",
            "description": description,
            "returnUrl": return_url,
            "email": client_email,
        }
        data["signature"] = self._generate_signature(data)

        response = requests.post(
            f"{self.base_url}/payments/initiate",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def verify_payment(self, order_id: str) -> dict:
        """Verifică statusul unei plăți."""
        data = {
            "merchantId": self.merchant_id,
            "orderId": order_id,
        }
        data["signature"] = self._generate_signature(data)

        response = requests.post(
            f"{self.base_url}/payments/status",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
```

### apps/plati/views.py
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import Tranzactie
from .bt_pay import BTPay
import uuid

def initiate_payment(request):
    if request.method == "POST":
        tranzactie = Tranzactie.objects.create(
            suma=request.POST.get("suma"),
            descriere_serviciu=request.POST.get("descriere"),
            nume_client=request.POST.get("nume"),
            email_client=request.POST.get("email"),
            telefon_client=request.POST.get("telefon", ""),
        )
        bt = BTPay()
        return_url = request.build_absolute_uri(
            reverse("plati:callback", kwargs={"pk": tranzactie.pk})
        )
        try:
            result = bt.initiate_payment(
                order_id=str(tranzactie.id_tranzactie),
                amount=float(tranzactie.suma),
                description=tranzactie.descriere_serviciu,
                return_url=return_url,
                client_email=tranzactie.email_client,
            )
            return redirect(result["paymentUrl"])
        except Exception as e:
            tranzactie.status = "failed"
            tranzactie.save()
            return render(request, "plati/eroare.html", {"error": str(e)})
    return render(request, "plati/checkout.html")

@csrf_exempt
def payment_callback(request, pk):
    tranzactie = get_object_or_404(Tranzactie, pk=pk)
    bt = BTPay()
    try:
        result = bt.verify_payment(str(tranzactie.id_tranzactie))
        tranzactie.bt_response_code = result.get("responseCode", "")
        tranzactie.bt_order_id = result.get("orderId", "")
        tranzactie.raspuns_complet_bt = result
        if result.get("status") == "SUCCESS":
            tranzactie.status = "completed"
        else:
            tranzactie.status = "failed"
        tranzactie.save()
    except Exception:
        tranzactie.status = "failed"
        tranzactie.save()

    if tranzactie.status == "completed":
        return render(request, "plati/succes.html", {"tranzactie": tranzactie})
    return render(request, "plati/eroare.html", {"tranzactie": tranzactie})
```

---

## 10. ADMIN DJANGO — configurare

```python
# apps/studii_de_caz/admin.py
from django.contrib import admin
from .models import StudiuDeCaz

@admin.register(StudiuDeCaz)
class StudiuDeCazAdmin(admin.ModelAdmin):
    list_display = ["client", "titlu", "industrie", "canal",
                    "data_proiect", "featured", "activ"]
    list_filter = ["industrie", "canal", "featured", "activ"]
    search_fields = ["titlu", "client"]
    list_editable = ["featured", "activ"]
    prepopulated_fields = {"slug": ("titlu",)}
    fieldsets = [
        ("Informații generale", {
            "fields": ["titlu", "slug", "client", "industrie", "canal",
                      "data_proiect", "featured", "activ"]
        }),
        ("Conținut", {
            "fields": ["descriere_scurta", "descriere_completa",
                      "obiectiv", "solutie", "rezultate"]
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

# apps/blog/admin.py
from django.contrib import admin
from .models import Articol, Categorie, Tag

@admin.register(Articol)
class ArticolAdmin(admin.ModelAdmin):
    list_display = ["titlu", "categorie", "status", "data_publicare"]
    list_filter = ["status", "categorie"]
    search_fields = ["titlu", "continut"]
    prepopulated_fields = {"slug": ("titlu",)}
    list_editable = ["status"]

admin.site.register(Categorie)
admin.site.register(Tag)
```

---

## 11. SCHEMA MARKUP (templates/includes/schema_markup.html)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Green Pheonix Concept SRL",
  "url": "https://greenpheonixconcept.com",
  "telephone": "+40793650902",
  "email": "contact@greenpheonixconcept.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Gura Calitei",
    "addressRegion": "VN",
    "addressCountry": "RO"
  },
  "founder": {
    "@type": "Person",
    "name": "Laurentiu Bogdan"
  },
  "description": "Agentie marketing digital si web development din Brasov. Meta Ads, Google Ads, TikTok Ads.",
  "areaServed": "Romania",
  "serviceType": ["Meta Ads", "Google Ads", "TikTok Ads", "Web Development"],
  "sameAs": [
    "https://www.facebook.com/greenpheonixconcept",
    "https://www.instagram.com/greenpheonixconcept"
  ]
}
</script>
```

---

## 12. ROBOTS.TXT (templates/robots.txt)

```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /plati/callback/
Disallow: /media/

Sitemap: https://greenpheonixconcept.com/sitemap.xml
```

---

## 13. SITEMAPS (apps/core/sitemaps.py)

```python
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.studii_de_caz.models import StudiuDeCaz
from apps.blog.models import Articol

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:despre", "core:contact",
                "servicii:ads", "servicii:web", "servicii:audit",
                "studii_de_caz:list", "blog:list"]

    def location(self, item):
        return reverse(item)

class StudiiDeCazSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return StudiuDeCaz.objects.filter(activ=True)

    def lastmod(self, obj):
        return obj.creat_la

class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Articol.objects.filter(status="publicat")

    def lastmod(self, obj):
        return obj.actualizat_la

sitemaps = {
    "static": StaticViewSitemap,
    "studii": StudiiDeCazSitemap,
    "blog": BlogSitemap,
}
```

---

## 14. CSS — DESIGN IDENTIC CU ORIGINALUL

### Paleta de culori și variabile CSS (static/css/main.css)
```css
:root {
  /* Culori principale — identice cu site-ul original */
  --color-dark: #0a0a0a;
  --color-dark-2: #111111;
  --color-dark-3: #1a1a1a;
  --color-accent: #00ff88;        /* Verde neon — accent principal */
  --color-accent-2: #00d4ff;      /* Albastru electric — accent secundar */
  --color-text: #e8e8e8;
  --color-text-muted: #888888;
  --color-border: #2a2a2a;
  --color-white: #ffffff;

  /* Tipografie */
  --font-mono: "JetBrains Mono", "Courier New", monospace;
  --font-sans: "Inter", system-ui, sans-serif;

  /* Spacing */
  --section-padding: 5rem 0;
  --container-max: 1200px;
  --border-radius: 4px;

  /* Ticker/bandă animată */
  --ticker-speed: 30s;
}

/* Reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--color-dark);
  color: var(--color-text);
  font-family: var(--font-sans);
  line-height: 1.6;
}

/* Container */
.container { max-width: var(--container-max); margin: 0 auto; padding: 0 1.5rem; }

/* Ticker animat (banda de servicii) */
.ticker-wrap { overflow: hidden; background: var(--color-dark-3);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border); }
.ticker { display: flex; animation: ticker-scroll var(--ticker-speed) linear infinite; }
.ticker-item { white-space: nowrap; padding: 0.75rem 2rem;
  font-family: var(--font-mono); font-size: 0.8rem;
  color: var(--color-text-muted); letter-spacing: 0.1em; }
@keyframes ticker-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* Hero */
.hero { min-height: 90vh; display: flex; align-items: center;
  padding: 6rem 0 4rem; position: relative; overflow: hidden; }
.hero__eyebrow { font-family: var(--font-mono); font-size: 0.75rem;
  color: var(--color-accent); letter-spacing: 0.2em; margin-bottom: 1.5rem; }
.hero__title { font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 800;
  line-height: 1.1; margin-bottom: 1.5rem; }
.hero__subtitle { font-size: 1.1rem; color: var(--color-text-muted);
  max-width: 600px; margin-bottom: 2.5rem; line-height: 1.7; }

/* Butoane */
.btn { display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.875rem 2rem; border-radius: var(--border-radius);
  font-weight: 600; font-size: 0.9rem; letter-spacing: 0.05em;
  text-decoration: none; transition: all 0.2s; cursor: pointer; border: none; }
.btn-primary { background: var(--color-accent); color: var(--color-dark); }
.btn-primary:hover { background: #00e57a; transform: translateY(-2px); }
.btn-outline { border: 1px solid var(--color-border); color: var(--color-text);
  background: transparent; }
.btn-outline:hover { border-color: var(--color-accent);
  color: var(--color-accent); }

/* Carduri servicii */
.card { background: var(--color-dark-2); border: 1px solid var(--color-border);
  border-radius: var(--border-radius); padding: 2rem;
  transition: border-color 0.2s, transform 0.2s; }
.card:hover { border-color: var(--color-accent); transform: translateY(-4px); }
.card__number { font-family: var(--font-mono); font-size: 0.75rem;
  color: var(--color-accent); margin-bottom: 1rem; }
.card__title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; }
.card__text { color: var(--color-text-muted); font-size: 0.95rem; line-height: 1.6; }

/* Metrici / cifre cheie */
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1px; background: var(--color-border); border: 1px solid var(--color-border); }
.metric-item { background: var(--color-dark-2); padding: 2rem 1.5rem; text-align: center; }
.metric-value { font-size: 2.5rem; font-weight: 800; color: var(--color-accent);
  font-family: var(--font-mono); line-height: 1; margin-bottom: 0.5rem; }
.metric-label { font-size: 0.8rem; color: var(--color-text-muted);
  letter-spacing: 0.1em; text-transform: uppercase; }

/* Grid responsive */
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }

/* Navbar */
.navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  background: rgba(10, 10, 10, 0.95); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border); padding: 1rem 0; }
.navbar__inner { display: flex; align-items: center;
  justify-content: space-between; }
.navbar__logo { font-family: var(--font-mono); font-weight: 700;
  color: var(--color-white); text-decoration: none; font-size: 1rem; }
.navbar__links { display: flex; gap: 2rem; list-style: none; }
.navbar__links a { color: var(--color-text-muted); text-decoration: none;
  font-size: 0.9rem; transition: color 0.2s; }
.navbar__links a:hover { color: var(--color-accent); }

/* Footer */
.footer { border-top: 1px solid var(--color-border); padding: 3rem 0 2rem;
  background: var(--color-dark-2); }

/* Responsive */
@media (max-width: 768px) {
  .hero__title { font-size: 2.2rem; }
  .navbar__links { display: none; }
  .grid-3 { grid-template-columns: 1fr; }
}
```

---

## 15. DATE REALE PENTRU POPULAREA DB (fixtures)

### Studii de caz existente (de introdus manual în admin):

**Studiu 1 — BPD Transport**
- Client: BPD Transport (bpdtransport.ro)
- Industrie: transport
- Canal: meta
- Obiectiv: Generare lead-uri pentru curse regulate România ↔ Italia
- Rezultate: 4.220 clicks | 400K+ impresii | 276K reach | 0.57 RON/click mediu | 12 campanii active
- Metrici: 400K+ Impresii | 4.220 Clicks | 0.57 RON Cost/Click | 12 Campanii
- Featured: Da

**Studiu 2 — CBS Express**
- Client: CBS Express
- Industrie: transport
- Canal: meta
- Obiectiv: Vizibilitate rute România ↔ Austria
- Rezultate: 490 clicks | 58K impresii | 43K reach | 0.96 RON/click mediu | 4 campanii
- Metrici: 58K+ Impresii | 490 Clicks | 0.96 RON Cost/Click | 4 Campanii
- Featured: Da

### Primul articol blog recomandat:
- Titlu: "Cum setezi corect Meta Pixel în 2026 — ghid pas cu pas"
- Categorie: Meta Ads
- Cuvinte cheie: cum setezi pixel facebook 2026, configurare meta pixel
- Status: publicat

---

## 16. COMENZI SETUP INIȚIAL

```bash
# 1. Crează proiectul
mkdir greenpheonix && cd greenpheonix
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Inițializare Django
django-admin startproject config .
python manage.py startapp core
# ... (repetă pentru fiecare app)

# 3. Migrații
python manage.py makemigrations
python manage.py migrate

# 4. Superuser pentru admin
python manage.py createsuperuser

# 5. Colectare fișiere statice
python manage.py collectstatic

# 6. Server development
python manage.py runserver
```

---

## 17. CHECKLIST FINAL ÎNAINTE DE GO-LIVE

- [ ] .env configurat cu toate credențialele reale
- [ ] DEBUG=False în producție
- [ ] ALLOWED_HOSTS include domeniul real
- [ ] PostgreSQL conectat și migrațiile rulate
- [ ] Fișierele statice colectate (collectstatic)
- [ ] SSL/HTTPS activ pe server
- [ ] robots.txt și sitemap.xml accesibile
- [ ] Google Analytics 4 ID actualizat în base.html
- [ ] Meta Pixel ID actualizat în base.html
- [ ] BT Pay credențiale de producție (nu sandbox)
- [ ] Email SMTP testat și funcțional
- [ ] Google Search Console verificat
- [ ] Toate paginile legale publicate (Termeni, GDPR, Anulare)
- [ ] Admin Django securizat (parolă puternică, URL /admin/ custom opțional)
- [ ] Backup automat baza de date configurat

---

## 18. INFORMAȚII COMPANIE (pentru conținut)

**Denumire**: GREEN PHEONIX CONCEPT SRL
**CUI**: RO45667331
**Nr. Reg. Comerțului**: J39/195/2022
**Sediul social**: Strada Principală Nr. 174, Gura Calitei, Județul Vrancea
**Website**: greenpheonixconcept.com
**Email**: greenpheonixconcept@gmail.com
**Telefon/WhatsApp**: +40 793 650 902
**Locație**: Brașov, România
**Fondator**: Laurențiu Bogdan
**An înființare**: 2022

**Servicii principale**:
- Meta Ads (Facebook & Instagram) — pachete 400–2.500 RON/lună
- Google Ads — pachete 400–2.500 RON/lună
- TikTok Ads — în Pachet Pro
- Creare site web — 1.500–4.000 RON
- Landing page — 500–900 RON
- Audit campanii — 300–500 RON
- Consultanță — 100–150 RON/oră

**Clienți reali**:
- BPD Transport (transport România-Italia)
- CBS Express (transport România-Austria)
- Reinert (brand FMCG — The Family Butchers Romania SRL)
- Martinel (brand FMCG — The Family Butchers Romania SRL)

**Cifre cheie (din campanii reale)**:
- 455.000+ impresii generate total
- 320.000+ utilizatori unici atinși
- 0.57 RON cost mediu/click (BPD Transport)
- Certificat Google Ads & Meta Ads

---

*Fișier generat de Claude | Versiune: 1.0 | Data: Martie 2026*
*Actualizează credențialele, CUI-ul și datele firmei înainte de utilizare.*
