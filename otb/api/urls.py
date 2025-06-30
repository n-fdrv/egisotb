from django.urls import path
from . import views

urlpatterns = [
    path('passengers/', views.passenger_list),
    path('passengers/<int:pk>/', views.passenger_detail),
    path('citizenships/', views.citizenship_list),
    path('doctypes/', views.doctype_list),
    path('passengers/last_ticket/', views.get_last_ticket),
    path('schedules/', views.voyage_list),
    path('schedules/<int:pk>/', views.voyage_detail),
    path('ferries/', views.ferries_list),
]