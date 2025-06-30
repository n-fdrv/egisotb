from rest_framework import serializers
from passengers.models import Passenger, Citizenship, DocType

class CitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = ['id', 'name']


class DocTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocType
        fields = ['id', 'name', 'pk_for_file']


class PassengerSerializer(serializers.ModelSerializer):
    citizenship = serializers.PrimaryKeyRelatedField(queryset=Citizenship.objects.all())
    doc_type = serializers.PrimaryKeyRelatedField(queryset=DocType.objects.all())

    class Meta:
        model = Passenger
        fields = [
            'id',
            'ticket_number',
            'surname',
            'name',
            'patronymic',
            'birthday',
            'gender',
            'citizenship',
            'doc_type',
            'doc_number',
            'created_at',
            'created_by',
            'is_active'
        ]
        read_only_fields = ['created_at', 'created_by']