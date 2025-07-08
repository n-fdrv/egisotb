from django.contrib import admin

from .models import CrewMember, CrewVoyage, Ferry, PassengerVoyage, Voyage


class CrewVoyageInline(admin.TabularInline):
    model = CrewVoyage
    extra = 1
    readonly_fields = ("created_at", "created_by")
    autocomplete_fields = ["crew"]
    fields = ("crew", "created_by", "created_at")


class PassengerVoyageInline(admin.TabularInline):
    model = PassengerVoyage
    extra = 1
    readonly_fields = ("created_at", "created_by")
    autocomplete_fields = ["passenger"]
    fields = ("passenger", "created_by", "created_at")


@admin.register(Ferry)
class FerryAdmin(admin.ModelAdmin):
    list_display = ["name", "registration_number", "flag", "ship_class"]
    search_fields = ["name", "registration_number"]
    list_filter = ["flag", "ship_class"]


@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = [
        "departure_date",
        "route_time",
        "ferry",
        "get_crew_count",
        "get_passenger_count",
    ]
    inlines = [CrewVoyageInline, PassengerVoyageInline]
    list_filter = ["departure_date", "ferry"]

    def get_crew_count(self, obj):
        return obj.crewvoyage_set.count()

    get_crew_count.short_description = "Членов экипажа"

    def get_passenger_count(self, obj):
        return obj.passengervoyage_set.count()

    get_passenger_count.short_description = "Пассажиров"


@admin.register(CrewMember)
class CrewAdmin(admin.ModelAdmin):
    list_display = [
        "fullname",
        "ferry",
        "birthday",
        "rank",
        "is_active",
    ]

    search_fields = ["surname", "name", "doc_number"]
    list_filter = ["ferry", "is_active"]

    def patronymic_or_na(self, obj):
        return obj.patronymic if obj.patronymic else "NA"

    patronymic_or_na.short_description = "Отчество"
