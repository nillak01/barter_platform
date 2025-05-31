# barter/urls.py
from django.urls import path
from . import views, views_api
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from django.contrib.auth import views as auth_views
from barter.views import register, static_test

app_name = 'barter'

urlpatterns = [
    # Web views
    path('', views.index, name='index'),
    path('static_test/', static_test, name='static_test'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_min.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', register, name='signup'),
    path('my-offers/', views.my_offers, name='my_offers'),
    path('my-items/', views.my_items, name='my_items'),
    path('item/add/', views.create_item, name='create_item'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/toggle-status/', views.toggle_item_status, name='toggle_item_status'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('items/bulk-action/', views.items_bulk_action, name='items_bulk_action'),
    path('offer/create/', views.create_offer, name='create_offer'),
    path('offer/<int:pk>/edit/', views.edit_offer, name='edit_offer'),
    path('offer/<int:pk>/toggle-status/', views.toggle_offer_status, name='toggle_offer_status'),
    path('offer/<int:pk>/delete/', views.delete_offer, name='delete_offer'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/settings', views.profile_settings, name='settings'),
    path('accounts/profile/exchange_history', views.exchange_history, name='exchange_history'),

    # API views
    path('api/items/', views_api.ItemListAPIView.as_view(), name='api_item_list'),
    path('api/items/<int:pk>/', views_api.ItemDetailAPIView.as_view(), name='api_item_detail'),
    path('api/offers/', views_api.OfferListAPIView.as_view(), name='api_offer_list'),
    path('api/offers/<int:pk>/', views_api.OfferDetailAPIView.as_view(), name='api_offer_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
