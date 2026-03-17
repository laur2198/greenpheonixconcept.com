from django.shortcuts import render
from .models import Pachet


def pachete(request):
    """Pagina cu pachetele de servicii și prețuri."""
    pachete_active = Pachet.objects.filter(activ=True)
    return render(request, "servicii/pachete.html", {
        "pachete": pachete_active,
        "page_title": "Pachete & Prețuri | Green Pheonix Concept",
        "meta_description": "Pachete clare de marketing digital. Starter 300€, Business 600€, Pro 1200€. Prețuri corecte, rezultate măsurabile.",
    })


def ads(request):
    return render(request, "servicii/ads.html", {
        "page_title": "Servicii Meta Ads & Google Ads Brașov | Green Pheonix Concept",
        "meta_description": "Campanii Meta Ads (Facebook & Instagram) și Google Ads gestionate profesional. Pachete de la 400 RON/lună.",
    })


def web(request):
    return render(request, "servicii/web.html", {
        "page_title": "Web Development Brașov — Site-uri și Landing Pages | Green Pheonix Concept",
        "meta_description": "Creare site-uri de prezentare și landing page-uri optimizate pentru conversii. De la 500 RON.",
    })


def audit(request):
    return render(request, "servicii/audit.html", {
        "page_title": "Audit Campanii Publicitare | Green Pheonix Concept",
        "meta_description": "Audit profesional al campaniilor Meta Ads și Google Ads. Identificăm ce nu funcționează și cum îmbunătățim rezultatele.",
    })
