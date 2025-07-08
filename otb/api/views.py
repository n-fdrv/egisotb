import re

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.middlewares.users import is_operator
from passengers.models import Passenger
from api.serializers import PassengerSerializer, VoyageSerializer, FerrySerializer, CrewMemberSerializer
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from route.models import Voyage, Ferry, CrewMember
from .serializers import CitizenshipSerializer, DocTypeSerializer
from passengers.models import Citizenship, DocType

User = get_user_model()


@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'POST'])
def passenger_list(request):
    if request.method == 'GET':
        passengers = Passenger.objects.all().order_by('-id')

        surname = request.GET.get('surname')
        name = request.GET.get('name')
        doc_number = request.GET.get('doc_number')
        ticket_number = request.GET.get('ticket_number')
        is_active = request.GET.get('is_active')
        limit = request.GET.get('limit')


        if surname:
            passengers = passengers.filter(surname__icontains=surname)
        if name:
            passengers = passengers.filter(name__icontains=name)
        if doc_number:
            passengers = passengers.filter(doc_number__icontains=doc_number)
        if ticket_number:
            passengers = passengers.filter(ticket_number=ticket_number)
        if is_active is not None and is_active != '':
            passengers = passengers.filter(is_active=(is_active == 'true'))
        if limit:
            passengers = passengers[:int(limit)]



        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['created_by'] = request.user.id  # Устанавливаем создателя
        doc_type = data.get('doc_type')
        doc_number = data.get('doc_number')


        # --- Проверка формата документа ---
        if doc_type == 1 and not re.fullmatch(r'^\d{10}$', doc_number):
            return Response({'error': 'Неверный формат паспорта (должен состоять из 10 цифр)'}, status=400)

        if doc_type == 5 and not re.fullmatch(r'^[IVX]{1,3}[А-Я]{2}\d{6}$', doc_number):
            return Response({
                'error': 'Неверный формат свидетельства о рождении'
            }, status=400)

        serializer = PassengerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'PUT', 'DELETE'])
def passenger_detail(request, pk):
    try:
        passenger = Passenger.objects.get(pk=pk)
    except Passenger.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PassengerSerializer(passenger)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['created_by'] = passenger.created_by.id if passenger.created_by else None
        serializer = PassengerSerializer(passenger, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('passengers.delete_passenger'):
            return Response({'detail': 'У вас нет прав на удаление'}, status=status.HTTP_403_FORBIDDEN)
        passenger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return None


@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def citizenship_list(request):
    countries = Citizenship.objects.all()
    serializer = CitizenshipSerializer(countries, many=True)
    return Response(serializer.data)

@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def doctype_list(request):
    types = DocType.objects.all()
    serializer = DocTypeSerializer(types, many=True)
    return Response(serializer.data)

@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def get_last_ticket(request):
    last_passenger = Passenger.objects.order_by('-id').first()
    last_ticket = last_passenger.ticket_number if last_passenger else 1000
    return Response({'last_ticket': last_ticket})

@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'POST'])
def voyage_list(request):
    if request.method == 'GET':
        voyages = Voyage.objects.all()

        departure_date = request.GET.get('departure_date')
        ferry_id = request.GET.get('ferry_id')
        is_active = request.GET.get('is_active')

        if is_active in ['true', 'True', '1']:
            voyages = voyages.filter(is_active=True)
        elif is_active in ['false', 'False', '0']:
            voyages = voyages.filter(is_active=False)
        if departure_date:
            voyages = voyages.filter(departure_date__icontains=departure_date)
        if ferry_id:
            voyages = voyages.filter(ferry__id__icontains=ferry_id)



        serializer = VoyageSerializer(voyages, many=True)
        return Response(serializer.data)

    serializer = VoyageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'PUT'])
def voyage_detail(request, pk):
    try:
        voyage = Voyage.objects.get(pk=pk)
    except Voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        schedule = Voyage.objects.get(pk=pk)
        serializer = VoyageSerializer(voyage)

        passenger_count = schedule.passengers.count()
        crew_count = schedule.crew.count()
        return Response({
            'detail': serializer.data,
            'passenger_count': passenger_count,
            'crew_count': crew_count,
            'is_active': schedule.is_active
        })

    elif request.method == 'PUT':
        try:
            schedule = Voyage.objects.get(pk=pk)
        except Voyage.DoesNotExist:
            return Response(status=404)

        passenger_ids = request.data.get('passengers', [])
        passengers = Passenger.objects.filter(id__in=passenger_ids)

        schedule.passengers.set(passengers)

        for p in passengers:
            p.is_active = False
            p.save()

        return Response({'detail': 'Данные обновлены'})
    return None


@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def schedule_passengers(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        passengers = schedule.passengers.all()
        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)
    except Voyage.DoesNotExist:
        return Response(status=404)

@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def voyage_crew(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        crew = schedule.crew.all()
        serializer = CrewMemberSerializer(crew, many=True)
        return Response(serializer.data)
    except Voyage.DoesNotExist:
        return Response(status=404)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def add_crew_to_schedule(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        crew_id = request.data.get('crew_id')
        crew = CrewMember.objects.get(pk=crew_id)

        schedule.crew.add(crew)
        crew.is_active = False
        crew.save()

        return Response({'detail': 'Член экипажа добавлен'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def remove_crew_from_schedule(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        crew_id = request.data.get('crew_id')
        crew = CrewMember.objects.get(pk=crew_id)

        schedule.crew.remove(crew)
        crew.is_active = True
        crew.save()

        return Response({'detail': 'Член экипажа удалён'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@login_required
@user_passes_test(is_operator)
@api_view(['GET'])
def ferries_list(request):
    ferries = Ferry.objects.all()
    serializer = FerrySerializer(ferries, many=True)
    return Response(serializer.data)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def bulk_create_schedules(request):
    schedules = request.data.get('schedules', [])
    created = []
    for item in schedules:
        serializer = VoyageSerializer(data=item)
        if serializer.is_valid():
            serializer.save()
            created.append(serializer.data)
        else:
            print(serializer.errors)
    return Response(created, status=status.HTTP_201_CREATED)

@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'POST'])
def crew_list(request):
    if request.method == 'GET':
        if request.method == 'GET':
            crew = CrewMember.objects.all().order_by('-id')

            surname = request.GET.get('surname')
            name = request.GET.get('name')
            doc_number = request.GET.get('doc_number')
            rank = request.GET.get('rank')
            ferry = request.GET.get('ferry_id')
            is_active = request.GET.get('is_active')
            limit = request.GET.get('limit')

            if surname:
                crew = crew.filter(surname__icontains=surname)
            if name:
                crew = crew.filter(name__icontains=name)
            if doc_number:
                crew = crew.filter(doc_number__icontains=doc_number)
            if rank:
                crew = crew.filter(rank__icontains=rank)
            if ferry:
                crew = crew.filter(ferry__id=ferry)
            if is_active is not None and is_active != '':
                crew = crew.filter(is_active=(is_active == 'true'))
            if limit:
                crew = crew[:int(limit)]



            serializer = CrewMemberSerializer(crew, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CrewMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


@login_required
@user_passes_test(is_operator)
@api_view(['GET', 'PUT', 'DELETE'])
def crew_detail(request, pk):
    try:
        member = CrewMember.objects.get(pk=pk)
    except CrewMember.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrewMemberSerializer(member)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CrewMemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def add_passenger_to_schedule(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        passenger_id = request.data.get('passenger_id')

        if not passenger_id:
            return Response({'error': 'Не передан ID пассажира'}, status=400)

        passenger = Passenger.objects.get(pk=passenger_id)
        schedule.passengers.add(passenger)
        passenger.is_active = False
        passenger.save()

        return Response({'detail': 'Пассажир добавлен'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def remove_passenger_from_schedule(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
        passenger_id = request.data.get('passenger_id')

        if not passenger_id:
            return Response({'error': 'Не передан ID пассажира'}, status=400)

        passenger = Passenger.objects.get(pk=passenger_id)
        schedule.passengers.remove(passenger)

        passenger.is_active = True
        passenger.save()

        return Response({'detail': 'Пассажир удалён'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@login_required
@user_passes_test(is_operator)
@api_view(['POST', 'PUT'])
def update_schedule_ferry(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
    except Voyage.DoesNotExist:
        return Response({'error': 'Рейс не найден'}, status=404)

    serializer = VoyageSerializer(schedule, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # Сохраняем обновлённый рейс
    serializer.save()

    # Отправляем обновлённые данные обратно
    return Response(serializer.data)

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def apply_ferry_and_add_members(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
    except Voyage.DoesNotExist:
        return Response({'error': 'Рейс не найден'}, status=404)

    ferry_id = request.data.get('ferry_id')

    if not ferry_id:
        return Response({'error': 'Не передан ferry_id'}, status=400)

    # --- Добавляем весь экипаж этого парома ---
    crew = CrewMember.objects.filter(ferry_id=ferry_id, is_active=True)

    schedule.crew.clear()
    # --- Добавляем членов экипажа к рейсу ---
    schedule.crew.add(*crew)

    # --- Сохраняем рейс ---
    schedule.ferry_id = ferry_id
    schedule.save()

    # --- Возвращаем данные ---
    return Response({
        'detail': 'Паром и участники успешно обновлены',
        'crew': list(crew.values('id', 'surname', 'name', 'doc_number'))
    })


@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def unlock_schedule(request, pk):
    try:
        schedule = Voyage.objects.get(pk=pk)
    except Voyage.DoesNotExist:
        return Response({'error': 'Рейс не найден'}, status=404)

    schedule.is_active = True
    schedule.save()

    return Response({
        'detail': 'Рейс разблокирован'
    })

@login_required
@user_passes_test(is_operator)
@api_view(['POST'])
def checkin_passenger_by_qr(request, pk):
    try:
        passenger = Passenger.objects.get(pk=pk)
    except Passenger.DoesNotExist:
        return Response({'error': 'Пассажир не найден'}, status=404)

    schedule_id = request.data.get('schedule_id');
    if not schedule_id:
        return Response({'error': 'Не указан рейс'}, status=400)

    try:
        schedule = Voyage.objects.get(pk=schedule_id)
    except Voyage.DoesNotExist:
        return Response({'error': 'Рейс не найден'}, status=404)

    schedule.passengers.add(passenger)
    passenger.is_active = False
    passenger.save()

    return Response({'detail': 'Пассажир добавлен на рейс'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # --- Проверки ---
        if not all([first_name, last_name, username, password1, password2]):
            return JsonResponse({'success': False, 'error': 'Заполните все поля'})

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Логин уже занят'})

        try:
            user = User.objects.create_user(
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return JsonResponse({
                'success': True,
                'redirect_url': '/',
                'user': {
                    'name': f"{user.first_name} {user.last_name}",
                    'username': user.username
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            return JsonResponse({'success': False, 'error': 'Неверные учетные данные'})

    return render(request, 'login.html')


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect_url': '/login/'})
