from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from passenger.models import Passenger, DocType, Citizenship

from .forms import PassengerForm
from .utils import paginator


PASSENGER_SHOW_LIMIT = 30


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o, 'isoformat'):
            return o.isoformat()
        return super().default(o)

class PassengerEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, DocType):
            return {
                'id': obj.id,
                'name': obj.name,
                # добавьте другие нужные поля
            }
        return super().default(obj)

def index(request):
    passengers = Passenger.objects.filter(is_active=True)
    page_obj = paginator(request, passengers, PASSENGER_SHOW_LIMIT)
    context = {
        'passengers': passengers,
        'page_obj': page_obj
    }
    return render(request, 'index.html', context)


@login_required
def passenger_list(request):
    passengers = Passenger.objects.filter(is_active=True)
    doc_types = DocType.objects.all()
    citizenships = Citizenship.objects.all()
    page_obj = paginator(request, passengers, PASSENGER_SHOW_LIMIT)
    russia = Citizenship.objects.get_or_create(name="РОССИЯ")[0]
    passport = DocType.objects.get_or_create(name='Паспорт РФ', pk_for_file=0)[0]
    last_passenger = Passenger.objects.last()
    ticket_number = 1
    if last_passenger:
        ticket_number = last_passenger.ticket_number + 1
    initial_data = {
        'doc_type': passport,
        'citizenship': russia,
        'ticket_number': ticket_number
    }
    form = PassengerForm(initial=initial_data)

    if request.method == 'POST':
        form = PassengerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            doc_number = form.cleaned_data.get('doc_number')
            existing_passenger = Passenger.objects.filter(doc_number=doc_number).first()

            if existing_passenger:
                # Активируем существующего пассажира
                existing_passenger.is_active = True
                existing_passenger.surname = form.cleaned_data.get('surname')
                existing_passenger.name = form.cleaned_data.get('name')
                existing_passenger.patronymic = form.cleaned_data.get('patronymic')
                existing_passenger.doc_type = form.cleaned_data.get('doc_type')
                existing_passenger.citizenship = form.cleaned_data.get('citizenship')
                existing_passenger.birthday = form.cleaned_data.get('birthday')
                existing_passenger.gender = form.cleaned_data.get('gender')
                existing_passenger.ticket_number = form.cleaned_data.get('ticket_number')
                existing_passenger.created_by = request.user
                existing_passenger.save()
                messages.success(request, 'Существующий пассажир активирован и обновлен')
            else:
                # Создаем нового пассажира
                passenger = form.save(commit=False)
                passenger.created_by = request.user
                passenger.is_active = True
                passenger.save()
                messages.success(request, 'Новый пассажир успешно создан')

            return redirect('passenger:passenger_list')

        messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
        return render(request, 'passenger/passenger_list.html', {
            'form': form,
            'passengers': passengers,
            'page_obj': page_obj,
            'doc_types': doc_types,
            'citizenships': citizenships
        })


    context = {
        'passengers': passengers,
        'page_obj': page_obj,
        'doc_types': doc_types,
        'citizenships': citizenships,
        'form': form
    }
    return render(request, 'passenger/passenger_list.html', context)


def passenger_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')


def passenger_search_api(request):
    doc_number = request.GET.get('doc_number', '')

    passengers = Passenger.objects.filter(
        doc_number__icontains=doc_number,
    ).select_related('doc_type', 'citizenship')[:10]

    passenger_list = []
    for passenger in passengers:
        passenger_list.append({
            'id': passenger.id,
            'surname': passenger.surname,
            'name': passenger.name,
            'patronymic': passenger.patronymic,
            'doc_type': {
                'id': passenger.doc_type.id,
                'name': passenger.doc_type.name
            },
            'doc_number': passenger.doc_number,
            'birthday': passenger.birthday.isoformat() if passenger.birthday else None,
            'gender': passenger.gender,
            'citizenship': {
                'id': passenger.citizenship.id,
                'name': passenger.citizenship.name
            } if passenger.citizenship else None
        })

    return JsonResponse(passenger_list, safe=False, encoder=PassengerEncoder)


def passenger_detail_api(request, pk):
    passenger = get_object_or_404(
        Passenger.objects.select_related('doc_type', 'citizenship'),
        pk=pk
    )

    data = {
        'id': passenger.id,
        'surname': passenger.surname,
        'name': passenger.name,
        'patronymic': passenger.patronymic,
        'doc_type': passenger.doc_type.id,  # или полный объект, если нужно
        'doc_number': passenger.doc_number,
        'birthday': passenger.birthday.isoformat() if passenger.birthday else None,
        'gender': passenger.gender,
        'citizenship': passenger.citizenship.id if passenger.citizenship else None
    }

    return JsonResponse(data, encoder=PassengerEncoder)