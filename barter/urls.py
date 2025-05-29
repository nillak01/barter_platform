# barter/urls.py
from django.urls import path
from . import views, views_api
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'barter'

urlpatterns = [
    # Web views
    path('', views.index, name='index'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/my/', views.my_items, name='my_items'),
    path('offers/create/<int:item_id>/', views.create_offer, name='create_offer'),
    path('offers/my/', views.my_offers, name='my_offers'),
    path('offers/<int:offer_id>/<str:action>/', views.manage_offer, name='manage_offer'),
    path('profile/', views.profile, name='profile'),

    # API views
    path('api/items/', views_api.ItemListAPIView.as_view(), name='api_item_list'),
    path('api/items/<int:pk>/', views_api.ItemDetailAPIView.as_view(), name='api_item_detail'),
    path('api/offers/', views_api.OfferListAPIView.as_view(), name='api_offer_list'),
    path('api/offers/<int:pk>/', views_api.OfferDetailAPIView.as_view(), name='api_offer_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)