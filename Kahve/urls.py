from django.contrib import admin
from django.urls import include, path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cafe/', include("cafe.urls")),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
