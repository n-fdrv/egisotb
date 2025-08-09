from django.urls import path

from . import views

urlpatterns = [
    path("passengers/", views.passenger_list),
    path("passengers/<int:pk>/", views.passenger_detail),
    path("citizenships/", views.citizenship_list),
    path("doctypes/", views.doctype_list),
    path("passengers/last_ticket/", views.get_last_ticket),
    path("passengers/<int:pk>/checkin/", views.checkin_passenger_by_qr),
    path("schedules/", views.voyage_list),
    path("schedules/<int:pk>/", views.voyage_detail),
    path("schedules/<int:pk>/passengers/", views.schedule_passengers),
    path("schedules/<int:pk>/crew/", views.voyage_crew),
    path("schedules/<int:pk>/add_crew/", views.add_crew_to_schedule),
    path("schedules/<int:pk>/remove_crew/", views.remove_crew_from_schedule),
    path(
        "schedules/<int:schedule_id>/clear_data/",
        views.clear_schedule_data,
        name="clear_schedule_data",
    ),
    path("ferries/", views.ferries_list),
    path("schedules/bulk/", views.bulk_create_schedules),
    path("schedules/<int:pk>/add_passenger/", views.add_passenger_to_schedule),
    path(
        "schedules/<int:pk>/remove_passenger/",
        views.remove_passenger_from_schedule,
    ),
    path(
        "schedules/<int:pk>/ferry/",
        views.update_schedule_ferry,
        name="update-schedule-ferry",
    ),
    path("schedules/<int:pk>/apply_ferry/", views.apply_ferry_and_add_members),
    path("schedules/<int:pk>/unlock/", views.unlock_schedule),
    path("crew/", views.crew_list),
    path("crew/<int:pk>/", views.crew_detail),
]
