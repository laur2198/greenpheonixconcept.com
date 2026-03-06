from django.shortcuts import render, get_object_or_404
from .models import Articol, Categorie


def lista(request):
    articole = Articol.objects.filter(status="publicat")
    categorii = Categorie.objects.all()
    categorie_slug = request.GET.get("categorie")
    if categorie_slug:
        articole = articole.filter(categorie__slug=categorie_slug)
    return render(request, "blog/lista.html", {
        "articole": articole,
        "categorii": categorii,
        "page_title": "Blog Marketing Digital | Green Pheonix Concept",
        "meta_description": "Articole despre Meta Ads, Google Ads, web development și strategii de marketing digital.",
    })


def detail(request, slug):
    articol = get_object_or_404(Articol, slug=slug, status="publicat")
    return render(request, "blog/detail.html", {
        "articol": articol,
        "page_title": articol.meta_title or articol.titlu,
        "meta_description": articol.meta_description or articol.rezumat,
    })
