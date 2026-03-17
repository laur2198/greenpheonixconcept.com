from django.shortcuts import render, get_object_or_404
from .models import StudiuDeCaz


def lista(request):
    studii = StudiuDeCaz.objects.filter(activ=True)
    return render(request, "studii_de_caz/lista.html", {
        "studii": studii,
        "page_title": "Studii de Caz — Rezultate Reale | Green Pheonix Concept",
        "meta_description": "Campanii Meta Ads și Google Ads cu rezultate măsurabile. Clienți reali, cifre reale.",
    })


def detail(request, slug):
    studiu = get_object_or_404(StudiuDeCaz, slug=slug, activ=True)
    return render(request, "studii_de_caz/detail.html", {
        "studiu": studiu,
        "page_title": f"{studiu.client} — {studiu.titlu} | Green Pheonix Concept",
        "meta_description": studiu.descriere_scurta,
    })


def featured(request):
    """Returnează primele studii cu featured=True — folosit pe homepage."""
    studii_featured = StudiuDeCaz.objects.filter(activ=True, featured=True)[:3]
    return studii_featured
