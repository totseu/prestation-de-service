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

    reservations = Order.objects.filter(
        client=user
    ).select_related('service', 'service__prestataire')

    reservations_actives = reservations.filter(
        statut__in=['planifie', 'en_cours']
    ).count()

    historique = Order.objects.filter(
        client=user,
        statut__in=['termine', 'annule']
    ).select_related('service', 'service__prestataire')

    total = Payment.objects.filter(
        client=user,
        statut='paye'
    ).aggregate(total=models.Sum('montant_total'))['total'] or 0

    prestataires = Service.objects.filter(
        disponible=True
    ).select_related('prestataire')

    facture_order = reservations.filter(
        statut='en_cours'
    ).exclude(payment__statut='paye').first()

    if facture_order:
        frais = int(facture_order.montant * 5 / 100)
        facture = {
            "service": facture_order.service.titre,
            "prestataire": facture_order.service.prestataire.prenom,
            "duree": str(facture_order.date_livraison) if facture_order.date_livraison else "-",
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

        if action == "reserver":
            service_id = request.POST.get("service_id")
            service = Service.objects.filter(id=service_id, disponible=True).first()
            if service:
                Order.objects.create(
                    client=user,
                    service=service,
                    montant=service.prix,
                    statut='planifie'
                )
                messages.success(request, "📅 Réservation créée avec succès !")
            return redirect(f"{request.path}?panel=reservations")

        if action == "annuler":
            order_id = request.POST.get("order_id")
            Order.objects.filter(
                id=order_id, client=user, statut='planifie'
            ).update(statut='annule')
            messages.success(request, "🗑 Réservation annulée.")
            return redirect(f"{request.path}?panel=reservations")

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






# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from services.models import Service
from orders.models import Order
from reviews.models import Review
from django.db.models import Sum, Avg, Count

@login_required
def dashboard_overview(request):
    user = request.user
    
    # Métriques services
    mes_services = Service.objects.filter(prestataire=user)
    services_publies = mes_services.filter(statut='publie').count()

    # Métriques commandes
    from django.utils import timezone
    from datetime import timedelta
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0)

    commandes = Order.objects.filter(prestataire=user)
    commandes_actives = commandes.filter(statut='en_cours')
    commandes_mois = commandes.filter(created_at__gte=debut_mois)

    # Revenus
    revenus_mois = commandes_mois.filter(
        statut='livre'
    ).aggregate(total=Sum('montant'))['total'] or 0

    # Évaluations
    evaluations = Review.objects.filter(prestataire=user)
    note_moyenne = evaluations.aggregate(avg=Avg('note'))['avg'] or 0

    # Dernières demandes (commandes en attente)
    nouvelles_demandes = commandes.filter(
        statut='en_attente'
    ).select_related('client', 'service').order_by('-created_at')[:5]

    # Commandes en cours
    en_cours = commandes_actives.select_related(
        'client', 'service'
    ).order_by('date_livraison')[:5]

    # Dernières évaluations
    dernieres_evals = evaluations.select_related(
        'client'
    ).order_by('-created_at')[:3]

    # Taux de complétion
    total_terminees = commandes.filter(statut__in=['livre', 'annule']).count()
    livrees_temps = commandes.filter(statut='livre').count()
    taux_completion = round((livrees_temps / total_terminees * 100) if total_terminees else 0)

    context = {
        'services_publies': services_publies,
        'commandes_actives': commandes_actives.count(),
        'revenus_mois': revenus_mois,
        'note_moyenne': round(note_moyenne, 1),
        'nb_evaluations': evaluations.count(),
        'nouvelles_demandes': nouvelles_demandes,
        'en_cours': en_cours,
        'dernieres_evals': dernieres_evals,
        'taux_completion': taux_completion,
        'livrees_temps': livrees_temps,
        'total_terminees': total_terminees,
    }
    return render(request, 'dashboard/overview.html', context)

# Alias pour compatibilité avec users/urls.py
dashboard_prestataire = dashboard_overview