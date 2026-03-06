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
