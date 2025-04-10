from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from auths.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('auths/', include('auths.urls')),
    path('profiles/', include('profiles.urls')),
    path('safety/', include('safety.urls')),
    path('hr/', include('hr.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
