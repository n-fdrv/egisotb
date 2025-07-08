from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

from core.middlewares.users import is_operator
from passengers.models import Passenger
from route.models import CrewMember, CrewVoyage, Ferry, PassengerVoyage, Voyage


@login_required
@user_passes_test(is_operator)
def passengers_list(request):
    return render(request, "passengers/passenger_list.html")


@login_required
@user_passes_test(is_operator)
def crew_list(request):
    return render(request, "crew_list.html")


@login_required
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    all_users = User.objects.all()
    passenger_count = Passenger.objects.filter(created_by=user).count()
    schedules_created = Voyage.objects.filter(created_by=user).count()

    # --- Рейсы, в которых пользователь добавлял пассажиров ---
    added_passengers_schedules = (
        PassengerVoyage.objects.filter(created_by=user)
        .values_list("voyage_id", flat=True)
        .count()
    )
    added_crew_schedules = (
        CrewVoyage.objects.filter(created_by=user)
        .values_list("voyage_id", flat=True)
        .count()
    )

    # --- Последние рейсы, где был пользователь ---
    recent_schedules = (
        Voyage.objects.filter(created_by=user)
        .select_related("ferry")
        .order_by("-departure_date")[:30]
    )

    for schedule in recent_schedules:
        print(schedule.ferry)

    passenger_actions = Passenger.objects.filter(created_by=user).values(
        "id", "surname", "name", "ticket_number", "doc_number", "created_at"
    )

    crew_actions = CrewMember.objects.filter(created_by=user).values(
        "id", "surname", "name", "rank", "created_at"
    )

    schedule_passenger_actions = (
        PassengerVoyage.objects.filter(created_by=user)
        .select_related("passenger", "voyage")
        .values(
            "id",
            "passenger__surname",
            "passenger__name",
            "voyage__name",
            "created_at",
            "voyage__departure_date",
            "voyage__departure_time",
        )
    )

    schedule_crew_actions = (
        CrewVoyage.objects.filter(created_by=user)
        .select_related("crew_member", "voyage")
        .values(
            "id",
            "crew__surname",
            "crew__name",
            "voyage__name",
            "created_at",
            "voyage__departure_date",
            "voyage__departure_time",
        )
    )

    ferry_actions = Ferry.objects.filter(created_by=user).values(
        "id", "name", "registration_number", "created_at"
    )

    # --- Формируем логи ---
    logs = []

    for p in passenger_actions:
        logs.append(
            {
                "time": p["created_at"].strftime("%d.%m.%Y %H:%M"),
                "object_type": "Пассажир",
                "object_repr": f"{p['surname']} {p['name']}",
                "action": "Создан",
                "schedule": "",
            }
        )

    for sp in schedule_passenger_actions:
        logs.append(
            {
                "time": sp["created_at"].strftime("%d.%m.%Y %H:%M"),
                "object_type": "пассажир -",
                "object_repr": f"{sp['passenger__surname']} {sp['passenger__name']}",
                "action": "Добавлен на рейс",
                "schedule": f"Рейс {sp['voyage__name']} - {sp['voyage__departure_date']} {sp['voyage__departure_time']}",
            }
        )

    for c in crew_actions:
        logs.append(
            {
                "time": c["created_at"].strftime("%d.%m.%Y %H:%M"),
                "object_type": "экипаж -",
                "object_repr": f"{c['surname']} {c['name']}",
                "action": "Создан",
                "schedule": "",
            }
        )

    for sc in schedule_crew_actions:
        logs.append(
            {
                "time": sc["created_at"].strftime("%d.%m.%Y %H:%M"),
                "object_type": "экипаж - ",
                "object_repr": f"{sc['crew__surname']} {sc['crew__name']}",
                "action": "Добавлен на рейс",
                "schedule": f"Рейс {sc['voyage__name']} - {sc['voyage__departure_date']} {sc['voyage__departure_time']}",
            }
        )

    for f in ferry_actions:
        logs.append(
            {
                "time": f["created_at"].strftime("%d.%m.%Y %H:%M"),
                "object_type": "Паром",
                "object_repr": f["name"],
                "action": "Создан",
                "schedule": "",
            }
        )

    # ← можно отсортировать по времени
    logs.sort(
        key=lambda x: datetime.strptime(x["time"], "%d.%m.%Y %H:%M"),
        reverse=True,
    )

    context = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "passenger_count": passenger_count,
        "crew_member_count": added_crew_schedules,
        "schedules_created": schedules_created,
        "added_passengers_on_schedule": added_passengers_schedules,
        "activity_log": logs,
        "all_users": all_users,
        "recent_schedules": [
            {
                "id": s.id,
                "name": s.name,
                "ferry": s.ferry.name if s.ferry else "Не указан",
                "departure_date": s.departure_date,
                "departure_time": s.departure_time,
                "passenger_count": PassengerVoyage.objects.filter(
                    voyage=s
                ).count(),
            }
            for s in recent_schedules
        ],
    }
    return render(request, "profile.html", context)
