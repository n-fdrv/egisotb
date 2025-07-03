from django.contrib import admin
from .models import Ferry, Voyage, CrewMember


@admin.register(Ferry)
class FerryAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'flag', 'ship_class']
    search_fields = ['name', 'registration_number']
    list_filter = ['flag', 'ship_class']

@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'departure_date', 'departure_time', 'arrival_date', 'ferry', 'route_type']
    filter_horizontal = ['passengers', 'crew']
    list_filter = ['departure_date', 'ferry', 'route_type']
    search_fields = ['name', 'departure_port', 'arrival_port']


@admin.register(CrewMember)
class CrewAdmin(admin.ModelAdmin):
    list_display = [
        'surname',
        'name',
        'patronymic_or_na',
        'birthday',
        'gender',
        'citizenship',
        'doc_type',
        'doc_number',
        'rank',
        'created_at',
    ]

    search_fields = ['surname', 'name', 'doc_number']
    list_filter = ['citizenship', 'doc_type', 'gender']

    def patronymic_or_na(self, obj):
        return obj.patronymic if obj.patronymic else 'NA'
    patronymic_or_na.short_description = 'Отчество'