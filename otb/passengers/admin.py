from django.contrib import admin

from .models import Citizenship, DocType, Passenger, UserStats


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ["action", "created_by", "created_at"]
    list_filter = ["action", "created_by"]


@admin.register(Citizenship)
class CitizenshipAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "pk_for_file"]
    search_fields = ["name"]


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [
        "ticket_number",
        "fullname",
        "birthday",
        "gender",
    ]
    list_display_links = ["ticket_number", "fullname"]
    readonly_fields = ["created_at"]
    search_fields = ["surname", "name", "doc_number"]
    list_filter = ["is_active", "citizenship", "doc_type", "gender"]

    def patronymic_or_na(self, obj):
        return obj.patronymic if obj.patronymic else "NA"

    patronymic_or_na.short_description = "Отчество"
