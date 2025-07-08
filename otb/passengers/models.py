from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

GENDER_CHOICES = [
    ('M', 'Мужской'),
    ('F', 'Женский'),
]

class Citizenship(CreatedModel):
    name = models.CharField('Гражданство', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гражданство'
        verbose_name_plural = 'Гражданства'


class DocType(CreatedModel):
    name = models.CharField('Название документа', max_length=100)
    short_name = models.CharField("Краткое название", max_length=32, blank=True, null=True)
    pk_for_file = models.PositiveIntegerField(
        'Уникальный номер (для файла)', unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Passenger(CreatedModel):
    ticket_number = models.PositiveIntegerField('Номер билета')
    surname = models.CharField('Фамилия', max_length=100)
    name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, blank=True, null=True)
    birthday = models.DateField('Дата рождения')
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES)
    citizenship = models.ForeignKey(
        Citizenship, on_delete=models.CASCADE, verbose_name='Гражданство'
    )
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Вид документа')
    doc_number = models.CharField('Номер документа', max_length=50)
    is_active = models.BooleanField('Активный', default=True)

    def __str__(self):
        return f"{self.surname} {self.name}"


    def fullname(self):
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'

    # Отчество по умолчанию выводится как NA, если нет значения
    @property
    def patronymic_or_na(self):
        return self.patronymic if self.patronymic else 'NA'
