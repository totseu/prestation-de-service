from django.http import HttpResponse


def home(request):
    return HttpResponse("Bienvenue sur la plateforme de prestation de services")