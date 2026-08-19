from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls', namespace='homepage')),
    path('about/', include('about.urls', namespace='about')),
    path('ice_cream/', include('ice_cream.urls', namespace='ice_cream')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
