from django.urls import path
from . import views


urlpatterns = [
      path('inscription/', views.choix_inscription, name='choix_inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('dashboard/client/', views.dashboard_client, name='dashboard_client'),
    path('dashboard/prestataire/', views.dashboard_prestataire, name='dashboard_prestataire'),
]