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
            send_mail(
                subject=f"[GPC] Solicitare noua: {cd['serviciu_interes']}",
                message=f"Nume: {cd['nume']}\nEmail: {cd['email']}\nTelefon: {cd.get('telefon', '')}\nServiciu: {cd['serviciu_interes']}\nBuget: {cd.get('buget', '')}\nMesaj: {cd['mesaj']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
            send_mail(
                subject="Multumim! Am primit solicitarea ta - Green Pheonix Concept",
                message=f"Buna {cd['nume']},\n\nMultumim ca ne-ai contactat! Iti vom raspunde in maximum 24 de ore.\n\nWhatsApp: +40 793 650 902\n\nCu drag,\nLaurentiu Bogdan\nGreen Pheonix Concept SRL",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cd["email"]],
                fail_silently=True,
            )
            messages.success(request, "Multumim! Am primit solicitarea ta. Iti raspundem in 24h.")
            return redirect("contact:succes")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {
        "form": form,
        "page_title": "Contact | Green Pheonix Concept",
        "meta_description": "Contacteaza-ne pentru o oferta personalizata de marketing digital sau web development.",
    })


def succes(request):
    return render(request, "contact/succes.html", {
        "page_title": "Mesaj trimis cu succes | Green Pheonix Concept",
    })
