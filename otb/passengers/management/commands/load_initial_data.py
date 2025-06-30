import json
from django.core.management.base import BaseCommand
from passengers.models import Citizenship, DocType

class Command(BaseCommand):
    help = 'Загружает начальные данные для гражданства и типов документов'

    def handle(self, *args, **options):
        # Загрузка гражданства
        with open('passengers/fixtures/countries.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
            for item in countries:
                Citizenship.objects.get_or_create(name=item['name'].upper())
            self.stdout.write(self.style.SUCCESS(f'✅ {len(countries)} записей гражданства загружено'))

        # Загрузка типов документов
        with open('passengers/fixtures/doc_types.json', 'r', encoding='utf-8') as f:
            doc_types = json.load(f)
            for item in doc_types:
                DocType.objects.get_or_create(
                    name=item['name'],
                    defaults={'pk_for_file': item['pk_for_file']}
                )
            self.stdout.write(self.style.SUCCESS(f'✅ {len(doc_types)} записей типов документов загружено'))