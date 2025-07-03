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
    path('schedules/<int:pk>/passengers/', views.schedule_passengers),
    path('schedules/<int:pk>/crew/', views.voyage_crew),
    path('ferries/', views.ferries_list),
    path('schedules/bulk/', views.bulk_create_schedules),
    path('schedules/<int:pk>/add_passenger/', views.add_passenger_to_schedule),
    path('schedules/<int:pk>/remove_passenger/', views.remove_passenger_from_schedule),
    path('crew/', views.crew_list),
    path('crew/<int:pk>/', views.crew_detail),
]