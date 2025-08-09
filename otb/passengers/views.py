from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render

from core.middlewares.users import is_operator
from passengers.models import UserStats


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
    passenger_count = UserStats.objects.filter(
        created_by=user, action="add_passenger"
    ).count()
    schedules_created = UserStats.objects.filter(
        created_by=user, action="send_schedule"
    ).count()

    # --- Рейсы, в которых пользователь добавлял пассажиров ---
    added_passengers_schedules = UserStats.objects.filter(
        created_by=user, action="passenger_to_schedule"
    ).aggregate(total_amount=Sum("amount"))["total_amount"]

    added_passengers_schedules = added_passengers_schedules or 0

    logs = (
        UserStats.objects.filter(created_by=user)
        .order_by("-created_at")
        .all()[:30]
    )

    context = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "passenger_count": passenger_count,
        "schedules_created": schedules_created,
        "logs": logs,
        "added_passengers_on_schedule": added_passengers_schedules,
        "all_users": all_users,
    }
    return render(request, "profile.html", context)
