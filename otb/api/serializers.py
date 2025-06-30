from rest_framework import serializers
from passengers.models import Passenger, Citizenship, DocType
from route.models import CrewMember, Ferry, Voyage


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


class FerrySerializer(serializers.ModelSerializer):
    flag = serializers.StringRelatedField()
    ship_class = serializers.StringRelatedField()

    class Meta:
        model = Ferry
        fields = ['id', 'name', 'registration_number', 'flag', 'ship_class']


class CrewMemberSerializer(serializers.ModelSerializer):
    citizenship = serializers.StringRelatedField()

    class Meta:
        model = CrewMember
        fields = ['id', 'surname', 'name', 'patronymic', 'position', 'citizenship', 'passport_number', 'date_of_birth', 'gender']

class VoyageSerializer(serializers.ModelSerializer):
    ferry = FerrySerializer(read_only=True)
    passengers = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(),
        many=True,
        required=False
    )
    crew = serializers.PrimaryKeyRelatedField(
        queryset=CrewMember.objects.all(),
        many=True,
        required=False
    )
    passenger_count = serializers.SerializerMethodField()
    crew_count = serializers.SerializerMethodField()

    def get_passenger_count(self, obj):
        return obj.passengers.count()

    def get_crew_count(self, obj):
        return obj.crew.count()

    class Meta:
        model = Voyage
        fields = '__all__'