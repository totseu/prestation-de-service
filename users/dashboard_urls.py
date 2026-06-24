# users/dashboard_urls.py
from django.urls import path
from users import views as usr_views
from services import views as svc_views

urlpatterns = [
    path('', usr_views.dashboard_overview, name='dashboard'),
    path('services/', svc_views.mes_services, name='mes-services'),
    path('services/creer/', svc_views.service_create, name='service-create'),
    path('services/<int:pk>/toggle/', svc_views.service_toggle_statut, name='service-toggle'),
]