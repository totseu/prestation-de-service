from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
     path('prestataire/', include('users.dashboard_urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)