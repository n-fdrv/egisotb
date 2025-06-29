from django.urls import path
from . import views

app_name = 'passenger'

urlpatterns = [
    path('', views.index, name='index'),
    path('passenger/', views.passenger_list, name='passenger_list'),
    path('passenger/<pk>/', views.passenger_detail),
]