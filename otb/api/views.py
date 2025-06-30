from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from passengers.models import Passenger
from api.serializers import PassengerSerializer, VoyageSerializer, FerrySerializer
from django.contrib.auth import get_user_model

from route.models import Voyage, Ferry
from .pagination import StandardResultsSetPagination
from .serializers import CitizenshipSerializer, DocTypeSerializer
from passengers.models import Citizenship, DocType

User = get_user_model()


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

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(passengers, request)

        serializer = PassengerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['created_by'] = request.user.id  # Устанавливаем создателя

        serializer = PassengerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Ловим ошибки
        print(serializer.errors)  # ← посмотри в терминале Django
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
def citizenship_list(request):
    countries = Citizenship.objects.all()
    serializer = CitizenshipSerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doctype_list(request):
    types = DocType.objects.all()
    serializer = DocTypeSerializer(types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_last_ticket(request):
    last_passenger = Passenger.objects.order_by('-id').first()
    last_ticket = last_passenger.ticket_number if last_passenger else 1000
    return Response({'last_ticket': last_ticket})


@api_view(['GET'])
def voyage_list(request):
    voyages = Voyage.objects.all()

    departure_date = request.GET.get('departure_date')
    ferry_id = request.GET.get('ferry_id')

    if departure_date:
        voyages = voyages.filter(departure_date__icontains=departure_date)
    if ferry_id:
        voyages = voyages.filter(ferry__id__icontains=ferry_id)

    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(voyages, request)

    serializer = VoyageSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def voyage_detail(request, pk):
    try:
        voyage = Voyage.objects.get(pk=pk)
        serializer = VoyageSerializer(voyage)
        return Response(serializer.data)
    except Voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def ferries_list(request):
    ferries = Ferry.objects.all()
    serializer = FerrySerializer(ferries, many=True)
    return Response(serializer.data)