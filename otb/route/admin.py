from django.contrib import admin
from .models import Ferry, Voyage

@admin.register(Ferry)
class FerryAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'flag', 'ship_class']
    search_fields = ['name', 'registration_number']
    list_filter = ['flag', 'ship_class']

@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = ['name', 'departure_date', 'departure_time', 'arrival_date', 'ferry', 'route_type']
    filter_horizontal = ['passengers', 'crew']
    list_filter = ['departure_date', 'ferry', 'route_type']
    search_fields = ['name', 'departure_port', 'arrival_port']