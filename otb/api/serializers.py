from django.contrib.auth import get_user_model
from rest_framework import serializers

from passengers.models import Citizenship, DocType, Passenger
from route.models import CrewMember, Ferry, Voyage

User = get_user_model()


class CitizenshipSerializer(serializers.ModelSerializer):
    """Сериалайзер пассажиров."""

    class Meta:
        model = Citizenship
        fields = ["id", "name"]


class DocTypeSerializer(serializers.ModelSerializer):
    """Сериалайзер видов документов."""

    class Meta:
        model = DocType
        fields = ["id", "name", "pk_for_file", "short_name"]


class ScheduleSerializer(serializers.ModelSerializer):
    """Сериалайзер рейсов."""

    ferry_name = serializers.SerializerMethodField()

    class Meta:
        model = Voyage
        fields = ["id", "name", "departure_date", "ferry_name"]

    def get_ferry_name(self, obj):
        return obj.ferry.name if obj.ferry else "Неизвестен"


class PassengerSerializer(serializers.ModelSerializer):
    """Сериалайзер пассажиров."""

    citizenship = serializers.PrimaryKeyRelatedField(
        queryset=Citizenship.objects.all()
    )
    doc_type = serializers.PrimaryKeyRelatedField(
        queryset=DocType.objects.all()
    )
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    schedules = ScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Passenger
        fields = [
            "id",
            "ticket_number",
            "surname",
            "name",
            "patronymic",
            "birthday",
            "gender",
            "citizenship",
            "doc_type",
            "doc_number",
            "created_at",
            "created_by",
            "is_active",
            "schedules",
        ]
        read_only_fields = ["created_at", "created_by"]


class FerrySerializer(serializers.ModelSerializer):
    """Сериалайзер паромов."""

    flag = serializers.StringRelatedField()
    ship_class = serializers.StringRelatedField()

    class Meta:
        model = Ferry
        fields = ["id", "name", "registration_number", "flag", "ship_class"]


class CrewMemberSerializer(serializers.ModelSerializer):
    """Сериалайзер экипажа."""

    citizenship = serializers.PrimaryKeyRelatedField(
        queryset=Citizenship.objects.all()
    )
    doc_type = serializers.PrimaryKeyRelatedField(
        queryset=DocType.objects.all()
    )
    ferry = serializers.PrimaryKeyRelatedField(queryset=Ferry.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = CrewMember
        fields = [
            "id",
            "surname",
            "name",
            "patronymic",
            "birthday",
            "rank",
            "citizenship",
            "doc_type",
            "doc_number",
            "gender",
            "ferry",
            "is_active",
            "created_by",
        ]


class VoyageSerializer(serializers.ModelSerializer):
    ferry = serializers.PrimaryKeyRelatedField(
        queryset=Ferry.objects.all(), required=False
    )
    passengers = PassengerSerializer(many=True, read_only=True)
    crew = CrewMemberSerializer(many=True, read_only=True)
    passenger_count = serializers.SerializerMethodField()
    crew_count = serializers.SerializerMethodField()

    def get_passenger_count(self, obj):
        return obj.passengers.count()

    def get_crew_count(self, obj):
        return obj.crew.count()

    class Meta:
        model = Voyage
        fields = "__all__"
