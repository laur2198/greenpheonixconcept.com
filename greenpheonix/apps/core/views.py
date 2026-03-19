from django.shortcuts import render
from apps.studii_de_caz.models import StudiuDeCaz
from apps.blog.models import Articol
from apps.servicii.models import Pachet
from .models import Testimonial, ClientLogo


def home(request):
    studii_featured = StudiuDeCaz.objects.filter(featured=True, activ=True)[:3]
    articole_recente = Articol.objects.filter(status="publicat")[:3]
    pachete = Pachet.objects.filter(activ=True)[:3]
    testimoniale = Testimonial.objects.filter(activ=True, featured=True)[:6]
    toate_testimonialele = Testimonial.objects.filter(activ=True) if not testimoniale else None
    if not testimoniale:
        testimoniale = Testimonial.objects.filter(activ=True)[:6]
    logo_uri = ClientLogo.objects.filter(activ=True)[:8]
    context = {
        "studii_featured": studii_featured,
        "articole_recente": articole_recente,
        "pachete": pachete,
        "testimoniale": testimoniale,
        "logo_uri": logo_uri,
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
    return render(request, "core/termeni.html", {
        "page_title": "Termeni și Condiții | Green Pheonix Concept",
    })


def confidentialitate(request):
    return render(request, "core/confidentialitate.html", {
        "page_title": "Politica de Confidențialitate | Green Pheonix Concept",
    })


def anulare(request):
    return render(request, "core/anulare.html", {
        "page_title": "Politica de Anulare și Rambursare | Green Pheonix Concept",
    })


def landing_transport(request):
    studiu_transport = StudiuDeCaz.objects.filter(
        industrie="transport", activ=True
    ).order_by("-featured", "-data_proiect").first()
    return render(request, "core/landing_transport.html", {
        "studiu": studiu_transport,
        "page_title": "Marketing Transport & Logistică | Green Pheonix Concept",
        "meta_description": "Sistem complet pentru firme de transport persoane și colete. Umplem mașinile prin Meta Ads + landing pages optimizate. Rezervări direct pe WhatsApp.",
    })


def custom_404(request, exception):
    return render(request, "404.html", {
        "page_title": "Pagina nu există | Green Pheonix Concept",
    }, status=404)
