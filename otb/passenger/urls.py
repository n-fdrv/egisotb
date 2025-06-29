from django.urls import path
from . import views

app_name = 'passenger'

urlpatterns = [
    path('', views.index, name='index'),
    path('passenger/', views.passenger_list, name='passenger_list'),
    path('passenger/<pk>/', views.passenger_detail),
    path('api/passengers/', views.passenger_search_api, name='passenger_search'),
    path('api/passengers/<int:pk>/', views.passenger_detail_api, name='passenger_detail'),
]