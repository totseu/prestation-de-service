from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from .forms import ClientRegistrationForm, PrestataireRegisterForm

from django.contrib.auth.decorators import login_required

BACKEND = 'django.contrib.auth.backends.ModelBackend'


def choix_inscription(request):

    form_client = ClientRegistrationForm()
    form_prestataire = PrestataireRegisterForm()

    if request.method == "POST":

        role = request.POST.get("role")
        print("ROLE :", role)

        if role == "client":

            form_client = ClientRegistrationForm(request.POST)

            if form_client.is_valid():
                user = form_client.save()
                login(request, user, backend=BACKEND)
                return redirect("dashboard_client")
            else:
                print(form_client.errors)

        elif role == "prestataire":

            form_prestataire = PrestataireRegisterForm(
                request.POST,
                request.FILES
            )

            if form_prestataire.is_valid():
                user = form_prestataire.save()
                login(request, user, backend=BACKEND)
                return redirect("dashboard_prestataire")
            else:
                print(form_prestataire.errors)

    return render(
        request,
        "accounts/choix_inscription.html",
        {
            "form_client": form_client,
            "form_prestataire": form_prestataire,
        }
    )


def connexion(request):

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        user = form.get_user()
        login(request, user, backend=BACKEND)

        if user.role == "prestataire":
            return redirect("dashboard_prestataire")

        return redirect("dashboard_client")

    return render(
        request,
        "accounts/connexion.html",
        {"form": form}
    )



from django.contrib.auth.decorators import login_required
from orders.models import Order
from services.models import Service
from payments.models import Payment
from django.contrib import messages
from django.db import models
from reviews.models import Review

@login_required
def dashboard_client(request):
    user = request.user
    panel = request.GET.get("panel", "overview")

    # Réservations du client
    reservations = Order.objects.filter(
        client=user
    ).select_related('service', 'service__prestataire')

    # Stats
    reservations_actives = reservations.filter(
        statut__in=['planifie', 'en_cours']
    ).count()

    # Historique — réservations terminées ou annulées
    historique = Order.objects.filter(
        client=user,
        statut__in=['termine', 'annule']
    ).select_related('service', 'service__prestataire')

    # Total dépensé
    total = Payment.objects.filter(
        client=user,
        statut='paye'
    ).aggregate(
        total=models.Sum('montant_total')
    )['total'] or 0

    # Catalogue des services disponibles
    prestataires = Service.objects.filter(
        disponible=True
    ).select_related('prestataire')

    # Facture en attente (première réservation en cours non payée)
    facture_order = reservations.filter(
        statut='en_cours'
    ).exclude(
        payment__statut='paye'
    ).first()

    facture = None
    if facture_order:
        frais = int(facture_order.montant * 5 / 100)
        facture = {
            "service": facture_order.service.titre,
            "prestataire": facture_order.service.prestataire.prenom,
            "duree": str(facture_order.date_livraison) if factura_order.date_livraison else "-",
            "sous_total": facture_order.montant,
            "frais_plateforme": frais,
            "total": facture_order.montant + frais,
        }
    else:
        facture = {
            "service": "-", "prestataire": "-", "duree": "-",
            "sous_total": 0, "frais_plateforme": 0, "total": 0,
        }

    # Traitement POST
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "poster_demande":
            messages.success(request, "✅ Demande publiée.")
            return redirect(f"{request.path}?panel=demande")

        if action == "payer" and facture_order:
            Payment.objects.update_or_create(
                order=facture_order,
                defaults={
                    "client": user,
                    "montant": facture_order.montant,
                    "mode": request.POST.get("paymode", "orange"),
                    "numero": request.POST.get("numero", ""),
                    "statut": "paye",
                }
            )
            messages.success(request, "💳 Paiement effectué avec succès !")
            return redirect(f"{request.path}?panel=paiement")

        if action == "noter":
            order_id = request.POST.get("order_id")
            order_a_noter = Order.objects.filter(
                id=order_id, client=user, statut='termine'
            ).first()
            if order_a_noter:
                Review.objects.get_or_create(
                    order=order_a_noter,
                    defaults={
                        "client": user,
                        "prestataire": order_a_noter.service.prestataire,
                        "note": int(request.POST.get("note", 5)),
                        "commentaire": request.POST.get("commentaire", ""),
                    }
                )
            messages.success(request, "⭐ Avis publié — merci !")
            return redirect(f"{request.path}?panel=reservations")

        if action == "sauvegarder_profil":
            user.nom = request.POST.get("last_name", user.nom)
            user.prenom = request.POST.get("first_name", user.prenom)
            user.email = request.POST.get("email", user.email)
            user.save()
            messages.success(request, "✅ Profil mis à jour.")
            return redirect(f"{request.path}?panel=profil")

    context = {
        "user": user,
        "panel": panel,
        "stats": {
            "reservations_actives": reservations_actives,
            "services_consultes": prestataires.count(),
            "total_depense": f"{int(total):,}".replace(",", " "),
        },
        "prestataires": prestataires,
        "reservations": reservations,
        "historique": historique,
        "facture": facture,
    }

    return render(request, "accounts/dashboard_client.html", context)

def dashboard_prestataire(request):

    return render(
        request,
        "accounts/dashboard_prestataire.html"
    )