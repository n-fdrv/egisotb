import csv
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from core.middlewares.users import is_operator
from route.models import CrewVoyage, PassengerVoyage, Voyage


@login_required
@user_passes_test(is_operator)
def schedule_list(request):
    return render(request, "voyage_list.html")


@login_required
@user_passes_test(is_operator)
def voyage_detail(request, pk):
    schedule = Voyage.objects.get(pk=pk)
    context = {
        "schedule": schedule,
    }
    return render(request, "schedule_detail.html", context)


@login_required
@user_passes_test(is_operator)
def download_schedule_data(request, pk):
    # --- Получаем рейс ---
    schedule = get_object_or_404(
        Voyage.objects.prefetch_related("passengers", "crew"), pk=pk
    )

    # --- Коррекция даты на -3 часа ---
    def adjust_date(d, t):
        if not d or not t:
            return None
        dt_str = f"{d}T{t}"
        dt = datetime.datetime.fromisoformat(dt_str)
        adjusted = dt - datetime.timedelta(hours=3)
        return f"{adjusted.isoformat(timespec='minutes')}Z"

    def format_date(d: datetime.date):
        if not d:
            return ""
        return d.isoformat()  # ← только дата без времени

    # --- Подготавливаем данные ---
    passengers = list(schedule.passengers.all())
    crew = list(schedule.crew.all())

    # --- Генерируем имя файла ---
    now = datetime.datetime.now() - datetime.timedelta(hours=3)
    timestamp = (
        now.strftime("%Y_%m_%d_%H_%M_%S") + f"_{now.microsecond // 1000:03d}"
    )
    operator_id = "32039"
    filename = f"{operator_id}_{timestamp}.csv"

    # --- Заголовок CSV ---
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(
        response,
        delimiter=";",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
    )

    headers = [
        "surname",
        "name",
        "patronymic",
        "birthday",
        "docType",
        "docNumber",
        "route",
        "departPlace",
        "arrivePlace",
        "departDate",
        "arriveDate",
        "routeType",
        "citizenship",
        "gender",
        "recType",
        "rank",
        "operationType",
        "operatorId",
        "places",
        "seatsCount",
        "buyDate",
        "shipClass",
        "shipNumber",
        "shipName",
        "flagState",
        "registerTimeIS",
        "operatorVersion",
        "phoneNumber",
        "email",
        "accountLogin",
        "accountPasswordHash",
        "internetInformation",
        "payInfoOrganization",
        "payInfoAccountNumber",
        "ticket",
        "amount",
        "currency",
        "travelClass",
        "speId",
        "gpeId",
    ]
    writer.writerow(headers)

    # --- Общие данные для всех записей ---
    route_type = 0
    depart_date = adjust_date(schedule.departure_date, schedule.departure_time)
    arrive_date = adjust_date(schedule.arrival_date, schedule.arrival_time)
    ship_class = "0"
    travel_class = "б/к"
    operator_version = "20"
    operation_type_for_passenger = "8"
    operation_type_for_crew = "50"
    amount = float(0)
    currency = "RUB"
    register_time_is = f"{now.isoformat(timespec='minutes')}Z"

    # --- Экипаж ---
    for c in crew:
        row = [
            c.surname,
            c.name,
            c.patronymic or "NA",
            format_date(c.birthday),
            c.doc_type.pk_for_file,  # или используйте p.doc_type если нужно значение
            c.doc_number,
            schedule.name,
            schedule.departure_port,
            schedule.arrival_port,
            depart_date,
            arrive_date,
            route_type,
            c.citizenship.name,
            c.gender,
            "0",  # recType — пассажир
            c.rank,  # rank — только для экипажа
            operation_type_for_crew,
            operator_id,
            "",
            "",
            "",
            ship_class,
            schedule.ferry.registration_number,
            schedule.ferry.name,
            schedule.ferry.flag,
            register_time_is,
            operator_version,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "б/н",
            "б/н",
        ]
        writer.writerow(row)

    # --- Пассажиры ---
    for p in passengers:
        row = [
            p.surname,  # Фамилия
            p.name,  # Имя
            p.patronymic or "NA",  # Отчество
            format_date(p.birthday),
            p.doc_type.pk_for_file,  # или используйте p.doc_type если нужно значение
            p.doc_number,
            schedule.name,
            schedule.departure_port,
            schedule.arrival_port,
            depart_date,
            arrive_date,
            route_type,
            p.citizenship.name,
            p.gender,
            "1",  # recType — пассажир
            "",  # rank — только для экипажа
            operation_type_for_passenger,
            operator_id,
            "б/м",  # places
            "",  # seatsCount
            register_time_is,
            ship_class,
            schedule.ferry.registration_number,
            schedule.ferry.name,
            schedule.ferry.flag,
            register_time_is,
            operator_version,
            "",  # PhoneNumber
            "",  # Email
            "",  # AccountLogin
            "",  # AccountPassword
            "",  # InternetInformation
            "",  # PayInfoOrganization
            "",  # PayInfoAccountNumber
            "",  # Билет
            amount,  # Стоимость
            currency,  # Валюта
            travel_class,  # Класс
            "б/н",
            "б/н",
        ]
        writer.writerow(row)

    # Добавляем автора этого рейса

    schedule.created_by = request.user
    CrewVoyage.objects.filter(voyage=schedule).update(created_by=request.user)
    PassengerVoyage.objects.filter(voyage=schedule).update(
        created_by=request.user
    )

    schedule.is_active = False
    schedule.save()

    return response
