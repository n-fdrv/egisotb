from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class DocType(CreatedModel):
    name = models.CharField(
        verbose_name='Название'
    )
    pk_for_file = models.IntegerField(
        verbose_name='Ключ для сайта'
    )

    def __str__(self):
        return self.name

class Citizenship(CreatedModel):
    name = models.CharField(
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Passenger(CreatedModel):
    class GenderChoices(models.TextChoices):
        MALE = "M", _("Мужской")
        FEMALE = "F", _("Женский")


    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=200
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=200,
        default="NA"
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
    )
    doc_type = models.ForeignKey(
        DocType,
        on_delete=models.SET_NULL,
        related_name='passenger',
        verbose_name='Вид документа',
        null=True,
        blank=True
    )
    doc_number = models.CharField(
        verbose_name="Номер документа",
        max_length=200
    )
    citizenship = models.ForeignKey(
        Citizenship,
        on_delete=models.SET_NULL,
        related_name='passenger',
        verbose_name='Гражданство',
        null=True,
        blank=True
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        choices=GenderChoices,
        default=GenderChoices.MALE,
    )
    is_active = models.BooleanField(
        verbose_name="Находится в порту",
        default=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='passenger',
        null=True,
        blank=True
    )


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"