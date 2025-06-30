from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from passengers.models import Passenger
from api.serializers import PassengerSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET', 'POST'])
def passenger_list(request):
    if request.method == 'GET':
        passengers = Passenger.objects.all()
        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['created_by'] = request.user.id  # Автоматически ставим создателя
        serializer = PassengerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        passenger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)