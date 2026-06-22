from django.urls import path
from . import views


urlpatterns = [
    path(
        'inscription/',
        views.choix_inscription,
        name='choix_inscription'
    ),

    path(
        'inscription/client/',
        views.inscription_client,
        name='inscription_client'
    ),

    path(
        'inscription/prestataire/',
        views.inscription_prestataire,
        name='inscription_prestataire'
    ),

     path('dashboard/', views.dashboard, name='dashboard'),
     
]