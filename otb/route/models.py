from django.db import models

from core.models import CreatedModel
from passengers.models import Citizenship, Passenger, GENDER_CHOICES, DocType


SHIP_CLASS_CHOICES = [
    ('0', 'Морские'),
    ('1', 'Рейдовые'),
    ('2', 'Внутреннего плавания'),
    ('3', 'Смешанного плавания'),
]

ROUTE_TYPE_CHOICES = [
    ('0', 'Беспересадочный'),
    ('1', 'Транзитный'),
]


class Ferry(CreatedModel):
    name = models.CharField('Название парома', max_length=100)
    registration_number = models.CharField('Регистрационный номер судна', max_length=50, unique=True)
    flag = models.ForeignKey(
        Citizenship,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Флаг регистрации'
    )
    ship_class = models.CharField('Класс судна', max_length=1, choices=SHIP_CLASS_CHOICES)

    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Паром'
        verbose_name_plural = 'Паромы'


class CrewMember(CreatedModel):
    surname = models.CharField('Фамилия', max_length=100)
    name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, null=True)
    birthday = models.DateField('Дата рождения')
    rank = models.CharField('Должность', max_length=100)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES)
    citizenship = models.ForeignKey(
        Citizenship, on_delete=models.CASCADE, verbose_name='Гражданство'
    )
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Вид документа')
    doc_number = models.CharField('Номер документа', max_length=50)
    ferry = models.ForeignKey(
        Ferry, on_delete=models.CASCADE, verbose_name='Паром'
    )
    is_active = models.BooleanField('На смене', default=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    def fullname(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = 'Член экипажа'
        verbose_name_plural = 'Экипаж'



class Voyage(CreatedModel):
    name = models.CharField('Название рейса', max_length=100)
    departure_port = models.CharField('Пункт отправления', max_length=100)
    arrival_port = models.CharField('Пункт прибытия', max_length=100)
    departure_date = models.DateField('Дата отправления')
    departure_time = models.TimeField('Время отправления')
    arrival_date = models.DateField('Дата прибытия')
    arrival_time = models.TimeField('Время прибытия')
    ferry = models.ForeignKey(Ferry, on_delete=models.SET_NULL, verbose_name='Паром', null=True, blank=True)
    route_type = models.CharField('Тип маршрута', max_length=1, choices=ROUTE_TYPE_CHOICES)
    passengers = models.ManyToManyField(Passenger, verbose_name='Пассажиры', null=True, blank=True, through="PassengerVoyage", related_name="schedules")
    crew = models.ManyToManyField(CrewMember, related_name='schedules', verbose_name='Экипаж', null=True, blank=True, through="CrewVoyage")
    is_active = models.BooleanField(default=True, verbose_name='Статус рейса')


    def __str__(self):
        return f"{self.ferry} → {self.departure_date} - {self.departure_time}"

    def route_time(self):
        return f"{self.departure_time}-{self.arrival_time}"

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

class PassengerVoyage(CreatedModel):
    voyage = models.ForeignKey(
        Voyage, on_delete=models.CASCADE, verbose_name='Рейс'
    )
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, verbose_name='Пассажир'
    )

    def __str__(self):
        return f"{self.voyage}: {self.passenger}"

    class Meta:
        verbose_name = 'Пассажир на пароме'
        verbose_name_plural = 'Пассажиры на пароме'


class CrewVoyage(CreatedModel):
    voyage = models.ForeignKey(
        Voyage, on_delete=models.CASCADE, verbose_name='Рейс'
    )
    crew = models.ForeignKey(
        CrewMember, on_delete=models.CASCADE, verbose_name='Экипаж'
    )

    def __str__(self):
        return f"{self.voyage}: {self.crew}"

    class Meta:
        verbose_name = 'Экипаж на пароме'
        verbose_name_plural = 'Экипаж на пароме'