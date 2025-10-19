from django.urls import path
from . import views

urlpatterns = [
    path('', views.us_trending_map, name='trending.us_map'),
    path('api/orders/', views.order_locations_api, name='trending.order_locations_api'),
]

