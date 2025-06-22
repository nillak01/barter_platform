from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from barter.views import register, static_test
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barter.urls')),  # Подключаем URL-ы вашего приложения
    path('accounts/', include('django.contrib.auth.urls')),
]
