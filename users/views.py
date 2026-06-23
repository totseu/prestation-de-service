from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import ClientRegistrationForm, PrestataireRegisterForm


def choix_inscription(request):

    form_client = ClientRegistrationForm()
    form_prestataire = PrestataireRegisterForm()

    if request.method == "POST":

        role = request.POST.get("role")

        if role not in ["client", "prestataire"]:
            return redirect("choix_inscription")


        if role == "client":

            form_client = ClientRegistrationForm(request.POST)

            if form_client.is_valid():

                user = form_client.save(commit=False)
                user.role = "client"
                user.save()

                login(request, user)

                return redirect("dashboard_client")


            else:
                print(form_client.errors)



        elif role == "prestataire":

            form_prestataire = PrestataireRegisterForm(
                request.POST,
                request.FILES
            )

            if form_prestataire.is_valid():

                user = form_prestataire.save(commit=False)
                user.role = "prestataire"
                user.save()

                login(request, user)

                return redirect("dashboard_prestataire")


            else:
                print(form_prestataire.errors)


    return render(request, "accounts/choix_inscription.html", {
        "form_client": form_client,
        "form_prestataire": form_prestataire,
    })



@login_required
def dashboard_client(request):

    if request.user.role != "client":
        return redirect("dashboard_prestataire")

    return render(
        request,
        "accounts/dashboardClient.html"
    )



@login_required
def dashboard_prestataire(request):

    if request.user.role != "prestataire":
        return redirect("dashboard_client")

    return render(
        request,
        "accounts/dashboardPrestataire.html"
    )