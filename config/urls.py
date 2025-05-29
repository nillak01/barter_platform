from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barter.urls')),  # Подключаем URL-ы вашего приложения
    path('accounts/', include('django.contrib.auth.urls')),
]
