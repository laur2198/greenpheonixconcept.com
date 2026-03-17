import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Tranzactie, Abonament, Plata, RaportClient, LivrabilClient, PromoTrial, ContractSemnat
from .bt_pay import BTPay
from apps.servicii.models import Pachet
from . import stripe_service


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
    return render(request, "plati/checkout.html", {
        "page_title": "Plată Online | Green Pheonix Concept",
    })


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


# --- Views Stripe ---

# Mapare tier pachet → Stripe Price ID din settings
STRIPE_PRICE_MAP = {
    "starter": settings.STRIPE_PRICE_ID_STARTER,
    "business": settings.STRIPE_PRICE_ID_BUSINESS,
    "pro": settings.STRIPE_PRICE_ID_PRO,
}


@login_required
def checkout(request, pachet_slug):
    """Inițiază o sesiune de Checkout Stripe pentru pachetul selectat."""
    pachet = get_object_or_404(Pachet, tier=pachet_slug, activ=True)
    price_id = STRIPE_PRICE_MAP.get(pachet.tier, "")

    if not price_id:
        messages.error(request, "Acest pachet nu este disponibil momentan pentru plată online.")
        return redirect("servicii:pachete")

    # Creare sau obținere customer Stripe
    abonament_activ = Abonament.objects.filter(
        user=request.user, status__in=["activ", "trial"]
    ).first()

    if abonament_activ and abonament_activ.stripe_customer_id:
        customer_id = abonament_activ.stripe_customer_id
    else:
        customer = stripe_service.creeaza_customer(
            email=request.user.email,
            nume=request.user.get_full_name() or request.user.email,
        )
        customer_id = customer.id

    success_url = request.build_absolute_uri(reverse("plati:portal_client")) + "?plata=succes"
    cancel_url = request.build_absolute_uri(reverse("servicii:pachete"))

    session = stripe_service.creeaza_abonament(
        customer_id=customer_id,
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return redirect(session.url)


@csrf_exempt
def webhook(request):
    """
    Endpoint webhook Stripe — procesează evenimentele de plată.
    Returnează întotdeauna HTTP 200 (chiar și la erori) pentru a evita retriele.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "invoice.paid":
        _proceseaza_factura_platita(data)

    elif event_type == "invoice.payment_failed":
        _proceseaza_plata_esuata(data)

    elif event_type == "customer.subscription.deleted":
        _proceseaza_abonament_sters(data)

    elif event_type == "customer.subscription.updated":
        _proceseaza_abonament_actualizat(data)

    elif event_type == "customer.subscription.created":
        _creeaza_cont_client(data)

    elif event_type == "checkout.session.completed":
        _proceseaza_trial_platit(data)

    return HttpResponse(status=200)


def _proceseaza_factura_platita(invoice):
    """Înregistrează plata reușită și activează abonamentul."""
    subscription_id = invoice.get("subscription")
    if not subscription_id:
        return
    abonament = Abonament.objects.filter(stripe_subscription_id=subscription_id).first()
    if abonament:
        abonament.status = "activ"
        abonament.save()
        Plata.objects.create(
            abonament=abonament,
            stripe_payment_intent_id=invoice.get("payment_intent", ""),
            suma=invoice.get("amount_paid", 0) / 100,
            valuta=invoice.get("currency", "eur"),
            status="reusit",
            data_plata=timezone.now(),
            factura_url=invoice.get("hosted_invoice_url", ""),
        )


def _proceseaza_plata_esuata(invoice):
    """Suspendă abonamentul la plată eșuată."""
    subscription_id = invoice.get("subscription")
    if not subscription_id:
        return
    Abonament.objects.filter(stripe_subscription_id=subscription_id).update(status="suspendat")


def _proceseaza_abonament_sters(subscription):
    """Marchează abonamentul ca anulat."""
    Abonament.objects.filter(stripe_subscription_id=subscription["id"]).update(status="anulat")


def _proceseaza_abonament_actualizat(subscription):
    """Actualizează data următoarei plăți."""
    import datetime
    next_billing = subscription.get("current_period_end")
    if next_billing:
        next_billing_dt = timezone.datetime.fromtimestamp(next_billing, tz=timezone.utc)
        Abonament.objects.filter(stripe_subscription_id=subscription["id"]).update(
            data_urmatoarei_plati=next_billing_dt
        )


def _creeaza_cont_client(subscription):
    """
    Crează automat un cont de utilizator la primul abonament Stripe.
    Trimite email cu link de setare parolă.
    """
    customer_id = subscription.get("customer")
    if not customer_id:
        return

    try:
        customer = stripe.Customer.retrieve(customer_id)
        email = customer.get("email", "")
        if not email:
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email, "is_active": True},
        )

        if created:
            user.set_unusable_password()
            user.save()

            # Trimite email cu link setare parolă
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"/reset/{uid}/{token}/"
            send_mail(
                subject="Contul tău Green Pheonix Concept a fost creat",
                message=(
                    f"Salut,\n\nContul tău a fost creat automat.\n"
                    f"Setează parola accesând: {reset_url}\n\n"
                    f"Green Pheonix Concept"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

        # Creare abonament local
        pachet = _gaseste_pachet_din_subscription(subscription)
        if pachet:
            import datetime
            start_ts = subscription.get("current_period_start")
            data_start = timezone.datetime.fromtimestamp(start_ts, tz=timezone.utc) if start_ts else timezone.now()
            Abonament.objects.get_or_create(
                stripe_subscription_id=subscription["id"],
                defaults={
                    "user": user,
                    "pachet": pachet,
                    "stripe_customer_id": customer_id,
                    "status": "activ",
                    "data_start": data_start,
                },
            )
    except Exception:
        pass  # Nu blocăm webhook-ul la erori interne


def _proceseaza_trial_platit(session):
    """Activează PromoTrial după plată confirmată prin Stripe Checkout."""
    trial_id = session.get("metadata", {}).get("trial_id")
    if not trial_id:
        return
    try:
        trial = PromoTrial.objects.get(pk=int(trial_id))
    except (PromoTrial.DoesNotExist, ValueError):
        return

    trial.status = "activ"
    trial.data_start = timezone.now()
    trial.data_expirare = timezone.now() + timezone.timedelta(days=7)
    trial.save()

    # Trimite email de confirmare
    send_mail(
        subject="✅ Plata confirmată — Trial 7 Zile Green Pheonix",
        message=(
            f"Salut {trial.nume_client},\n\n"
            f"Plata ta de 50€ a fost confirmată!\n\n"
            f"Trial-ul tău de 7 zile este acum activ.\n"
            f"Data expirare: {trial.data_expirare.strftime('%d.%m.%Y')}\n\n"
            f"Accesează portalul tău: https://greenpheonixconcept.com/plati/portal/trial/\n\n"
            f"Ne vom contacta în curând pentru a demara auditul și strategia.\n\n"
            f"Cu respect,\nLaurențiu — Green Pheonix Concept"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[trial.email_client],
        fail_silently=True,
    )


def _gaseste_pachet_din_subscription(subscription):
    """Mapează Stripe Price ID la un Pachet local."""
    items = subscription.get("items", {}).get("data", [])
    if not items:
        return None
    price_id = items[0].get("price", {}).get("id", "")
    for tier, pid in STRIPE_PRICE_MAP.items():
        if pid == price_id:
            return Pachet.objects.filter(tier=tier, activ=True).first()
    return None


@login_required
@require_POST
def anuleaza_abonament(request):
    """Anulează abonamentul activ al clientului la sfârșitul perioadei."""
    abonament = Abonament.objects.filter(
        user=request.user, status="activ"
    ).first()

    if not abonament:
        messages.error(request, "Nu ai niciun abonament activ de anulat.")
        return redirect("plati:portal_client")

    stripe_service.anuleaza_abonament(abonament.stripe_subscription_id)
    abonament.status = "anulat"
    abonament.save()
    messages.success(request, "Abonamentul tău a fost anulat. Vei mai avea acces până la sfârșitul perioadei curente.")
    return redirect("plati:portal_client")


def contract_view(request, pachet_slug):
    """Afișează contractul de prestări servicii pentru pachetul ales."""
    pachet = get_object_or_404(Pachet, tier=pachet_slug, activ=True)
    return render(request, "plati/contract.html", {
        "pachet": pachet,
        "page_title": f"Contract de Servicii — {pachet.nume} | Green Pheonix Concept",
    })


def semneaza_contract(request, pachet_slug):
    """Procesează semnarea contractului, trimite emailuri, redirecționează la plată."""
    if request.method != "POST":
        return redirect("plati:contract", pachet_slug=pachet_slug)

    pachet = get_object_or_404(Pachet, tier=pachet_slug, activ=True)

    nume = request.POST.get("client_nume", "").strip()
    email = request.POST.get("client_email", "").strip()
    telefon = request.POST.get("client_telefon", "").strip()
    firma = request.POST.get("client_firma", "").strip()
    cui = request.POST.get("client_cui", "").strip()
    adresa = request.POST.get("client_adresa", "").strip()
    semnatura = request.POST.get("semnatura_text", "").strip()
    accept = request.POST.get("accept_termeni")

    if not nume or not email or not semnatura or not accept:
        messages.error(request, "Completează toate câmpurile obligatorii și acceptă termenii.")
        return redirect("plati:contract", pachet_slug=pachet_slug)

    # IP client
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")

    # Snapshot pachet la momentul semnării
    snapshot = {
        "nume": pachet.nume,
        "tier": pachet.tier,
        "pret_lunar": str(pachet.pret_lunar),
        "pret_setup": str(pachet.pret_setup) if pachet.pret_setup else "0",
        "descriere": pachet.descriere,
    }

    contract = ContractSemnat.objects.create(
        pachet=pachet,
        client_nume_complet=nume,
        client_email=email,
        client_telefon=telefon,
        client_firma=firma,
        client_cui=cui,
        client_adresa=adresa,
        semnatura_text=semnatura,
        ip_semnare=ip,
        pachet_snapshot=snapshot,
        status="semnat",
    )

    # --- EMAIL CATRE CLIENT ---
    numar = contract.numar_contract()
    mesaj_client = f"""Bună ziua, {nume},

Confirmăm că ai semnat electronic Contractul de Prestări Servicii cu Green Pheonix Concept.

📋 DETALII CONTRACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Număr contract: {numar}
Data semnării: {contract.data_semnare.strftime('%d.%m.%Y, %H:%M')}
Pachet ales: {pachet.nume} ({pachet.get_tier_display()})
Valoare lunară: {pachet.pret_lunar}€/lună
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✍️ SEMNĂTURA ELECTRONICĂ
Semnătură înregistrată: {semnatura}
IP înregistrat: {ip}

Această semnătură electronică simplă este valabilă conform Regulamentului eIDAS (Art. 3(10)).

PASUL URMĂTOR: Urmează plata pentru activarea abonamentului. Vei fi redirecționat automat.

Cu respect,
Laurențiu Știrbu
Green Pheonix Concept SRL
📧 contact@greenpheonixconcept.com
📱 +40 793 650 902
"""
    send_mail(
        subject=f"[{numar}] Contract Semnat — {pachet.nume} | Green Pheonix Concept",
        message=mesaj_client,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )

    # --- EMAIL CATRE ADMIN ---
    mesaj_admin = f"""NOU CONTRACT SEMNAT

Număr: {numar}
Client: {nume} ({email})
Telefon: {telefon or '—'}
Firmă: {firma or '—'} | CUI: {cui or '—'}
Adresă: {adresa or '—'}
Pachet: {pachet.nume} — {pachet.pret_lunar}€/lună
Semnătură: {semnatura}
IP: {ip}
Data: {contract.data_semnare.strftime('%d.%m.%Y %H:%M')}

Urmează plata Stripe.
"""
    send_mail(
        subject=f"[ADMIN] Contract nou: {numar} — {nume}",
        message=mesaj_admin,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=True,
    )

    # Redirecționare către Stripe checkout (cu contract_id în sesiune)
    request.session["contract_id"] = contract.pk
    if request.user.is_authenticated:
        return redirect("plati:checkout", pachet_slug=pachet_slug)
    else:
        # Redirecționare cu email prefilled pentru login/register
        return redirect(f"/login/?next=/plati/stripe/checkout/{pachet_slug}/&email={email}")


def promo_trial(request):
    """Landing page Pachet Promo 7 Zile — 50€ one-time."""
    return render(request, "plati/promo_trial.html", {
        "page_title": "Testează 7 Zile — 50€ | Green Pheonix Concept",
        "meta_description": "Testează serviciile noastre timp de 7 zile pentru 50€. Audit, strategie și primii pași implementați.",
    })


def checkout_trial(request):
    """Inițiază Stripe Payment Intent pentru Promo Trial 7 Zile."""
    if request.method != "POST":
        return redirect("plati:promo_trial")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    nume = request.POST.get("nume", "").strip()
    email = request.POST.get("email", "").strip()
    telefon = request.POST.get("telefon", "").strip()
    nisa = request.POST.get("nisa", "").strip()
    pachet_dorit = request.POST.get("pachet_dorit", "nedecis")

    if not nume or not email:
        messages.error(request, "Completează numele și emailul.")
        return redirect("plati:promo_trial")

    # Crează înregistrarea trial
    trial = PromoTrial.objects.create(
        user=request.user if request.user.is_authenticated else None,
        nume_client=nume,
        email_client=email,
        telefon_client=telefon,
        nisa_client=nisa,
        pachet_dorit_dupa_trial=pachet_dorit,
        status="pending",
    )

    success_url = request.build_absolute_uri(
        reverse("plati:portal_trial") + f"?trial_id={trial.pk}"
    )
    cancel_url = request.build_absolute_uri(reverse("plati:promo_trial"))

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            customer_email=email,
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "unit_amount": 5000,  # 50€ în cenți
                    "product_data": {
                        "name": "Pachet Promo 7 Zile — Green Pheonix Concept",
                        "description": "Acces 7 zile: audit, strategie și primii pași implementați.",
                    },
                },
                "quantity": 1,
            }],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"trial_id": str(trial.pk)},
        )
        trial.stripe_payment_intent_id = session.id
        trial.save()
        return redirect(session.url)
    except Exception as e:
        trial.status = "pending"
        trial.save()
        messages.error(request, f"Eroare la procesarea plății: {str(e)}")
        return redirect("plati:promo_trial")


def portal_trial(request):
    """Portal pentru clienții cu Promo Trial activ."""
    trial_id = request.GET.get("trial_id")
    trial = None

    if trial_id:
        trial = PromoTrial.objects.filter(pk=trial_id).first()

    if not trial and request.user.is_authenticated:
        trial = PromoTrial.objects.filter(
            user=request.user
        ).order_by("-creat_la").first()

    return render(request, "plati/portal_trial.html", {
        "trial": trial,
        "page_title": "Portal Trial | Green Pheonix Concept",
    })


@login_required
def portal_client(request):
    """Pagina portal client — afișează abonamentul, plățile, rapoartele și livrabilele."""
    abonament = Abonament.objects.filter(
        user=request.user
    ).order_by("-creat_la").first()

    plati = []
    rapoarte = []
    livrabile = []
    categorie_filtru = request.GET.get("categorie", "toate")

    if abonament:
        plati = abonament.plati.all()
        rapoarte = abonament.rapoarte.all()
        livrabile_qs = abonament.livrabile.all()
        if categorie_filtru != "toate":
            livrabile_qs = livrabile_qs.filter(categorie=categorie_filtru)
        livrabile = livrabile_qs

    return render(request, "plati/portal_client.html", {
        "abonament": abonament,
        "plati": plati,
        "rapoarte": rapoarte,
        "livrabile": livrabile,
        "categorie_filtru": categorie_filtru,
        "page_title": "Portalul meu | Green Pheonix Concept",
    })
