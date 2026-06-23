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



@login_required
def dashboard_client(request):
    context = {
        "user": request.user,
        "panel": request.GET.get("panel", "overview"),
        "stats": {
            "reservations_actives": 0,
            "services_consultes": 0,
            "total_depense": "0",
        },
        "prestataires": [],
        "reservations": [],
        "historique": [],
        "facture": {
            "service": "-",
            "prestataire": "-",
            "duree": "-",
            "sous_total": 0,
            "frais_plateforme": 0,
            "total": 0,
        },
    }
    return render(request, "accounts/dashboard_client.html", context)

def dashboard_prestataire(request):

    return render(
        request,
        "accounts/dashboard_prestataire.html"
    )