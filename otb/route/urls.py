from django.urls import path
from django.views.generic import TemplateView

from route import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='voyage_list.html'), name='voyage_list'),
    path('<int:pk>/', views.voyage_detail, name='schedule_detail'),
    path('<int:pk>/download/', views.download_schedule_data, name='schedule_download'),
]