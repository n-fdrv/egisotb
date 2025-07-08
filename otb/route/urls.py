from django.urls import path

from route import views

urlpatterns = [
    path("", views.schedule_list, name="voyage_list"),
    path("<int:pk>/", views.voyage_detail, name="schedule_detail"),
    path(
        "<int:pk>/download/",
        views.download_schedule_data,
        name="schedule_download",
    ),
]
