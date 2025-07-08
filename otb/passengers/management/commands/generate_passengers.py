import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from passengers.models import Citizenship, DocType, Passenger

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Генерирует тестовые данные для модели Passenger"

    def handle(self, *args, **options):
        citizenships = list(Citizenship.objects.all())
        doc_types = list(DocType.objects.all())

        if not citizenships:
            self.stdout.write(
                self.style.ERROR(
                    "Нет записей в Citizenship. Сначала загрузите справочник стран"
                )
            )
            return

        if not doc_types:
            self.stdout.write(
                self.style.ERROR(
                    "Нет записей в DocType. Сначала загрузите типы документов"
                )
            )
            return

        if not User.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    "Нет пользователей. Создайте хотя бы одного суперпользователя"
                )
            )
            return

        admin_user = User.objects.first()

        for i in range(1, 51):  # Генерируем 50 записей
            ticket_number = 1000 + i
            surname = fake.last_name()
            name = fake.first_name()
            patronymic = fake.middle_name()
            birthday = fake.date_between(start_date="-60y", end_date="-18y")
            gender = random.choice(["M", "F"])
            citizenship = random.choice(citizenships)
            doc_type = random.choice(doc_types)
            doc_number = self.generate_doc_number(doc_type.name)

            Passenger.objects.get_or_create(
                ticket_number=ticket_number,
                defaults={
                    "surname": surname,
                    "name": name,
                    "patronymic": patronymic,
                    "birthday": birthday,
                    "gender": gender,
                    "citizenship": citizenship,
                    "doc_type": doc_type,
                    "doc_number": doc_number,
                    "is_active": True,
                    "created_by": admin_user,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("✅ Тестовые данные успешно загружены")
        )

    def generate_doc_number(self, doc_type_name):
        if "паспорт" in doc_type_name.lower():
            return f"{fake.random_int(min=1000, max=9999)} {fake.random_int(min=100000, max=999999)}"
        elif "рождения" in doc_type_name.lower():
            return f"{fake.random_int(min=100, max=999)}-{fake.random_int(min=100, max=999)}"
        elif "загран" in doc_type_name.lower():
            return f"{fake.random_int(min=10, max=99)} {fake.random_int(min=100000, max=999999)}"
        else:
            return fake.bothify(text="??-######")
