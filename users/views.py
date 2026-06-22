from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import ClientRegistrationForm, PrestataireRegisterForm


def choix_inscription(request):
    return render(
        request,
        'accounts/choix_inscription.html'
    )


def inscription_client(request):

 if request.method == "POST":

    form = ClientRegistrationForm(request.POST)

    if form.is_valid():

        print("FORMULAIRE VALIDE")

        user = form.save()

        login(request, user)

        return redirect('dashboard')

    else:
        print(form.errors)


def inscription_prestataire(request):

    if request.method == "POST":

        form = PrestataireRegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:
        form = PrestataireRegisterForm()

    return render(
        request,
        'accounts/inscription_prestataire.html',
        {'form': form}
    )


@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboardClient.html'
    )


def connexion(request):
    return render(
        request,
        'accounts/connexion.html'
    )