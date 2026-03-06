from django.shortcuts import render


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
