from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Tranzactie
from .bt_pay import BTPay


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
