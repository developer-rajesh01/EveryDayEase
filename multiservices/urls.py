from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/admin/', admin.site.urls),
    path('', include("home.urls"),name='home'),
    path("accounts/", include("authentication.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
