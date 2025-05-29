from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from barter.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('barter.urls')),  # Подключаем URL-ы вашего приложения
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', auth_views.LogoutView.as_view(), name='register'),
]
