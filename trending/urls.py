from django.urls import path
from . import views

urlpatterns = [
    path('', views.us_trending_map, name='trending.us_map'),
]

