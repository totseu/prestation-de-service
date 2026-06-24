# services/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service
from .forms import ServiceForm

@login_required
def mes_services(request):
    services = Service.objects.filter(prestataire=request.user)
    publies = services.filter(statut='publie')
    brouillons = services.filter(statut='brouillon')
    context = {
        'services': services,
        'publies': publies,
        'brouillons': brouillons,
    }
    return render(request, 'dashboard/mes_services.html', context)

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.prestataire = request.user
            # Publier ou sauver en brouillon selon le bouton cliqué
            if 'publier' in request.POST:
                service.statut = 'publie'
                messages.success(request, 'Service publié avec succès.')
            else:
                service.statut = 'brouillon'
                messages.info(request, 'Service sauvegardé en brouillon.')
            service.save()
            return redirect('mes-services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/service_form.html', {'form': form})

@login_required
def service_toggle_statut(request, pk):
    service = get_object_or_404(Service, pk=pk, prestataire=request.user)
    if service.statut == 'publie':
        service.statut = 'suspendu'
        messages.info(request, 'Service masqué.')
    else:
        service.statut = 'publie'
        messages.success(request, 'Service publié.')
    service.save()
    return redirect('mes-services')