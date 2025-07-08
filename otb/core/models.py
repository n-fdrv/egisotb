from django.contrib.auth import get_user_model
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Создан пользователем",
    )

    class Meta:
        abstract = True
