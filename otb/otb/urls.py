"""
URL configuration for otb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('passengers/', TemplateView.as_view(template_name='passengers/passenger_list.html'), name='passenger_list'),
    path('crew/', TemplateView.as_view(template_name='crew_list.html'), name='crew_list'),
    path('accounts/login/', TemplateView.as_view(template_name='stub.html'), name='login'),
    path('accounts/register/', TemplateView.as_view(template_name='stub.html'), name='register'),
    path('accounts/logout/', TemplateView.as_view(template_name='stub.html'), name='logout'),
    path('api/', include('api.urls')),
    path('schedules/', include('route.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
