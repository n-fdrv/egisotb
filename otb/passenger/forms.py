import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Passenger, Citizenship, DocType


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = (
            'doc_type',
            'doc_number',
            'citizenship',
            'surname',
            'name',
            'patronymic',
            'birthday',
            'gender',
            'ticket_number'
        )

        widgets = {
            'birthday': forms.TextInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doc_type = cleaned_data.get('doc_type')
        doc_number = cleaned_data.get('doc_number')

        if doc_type and doc_number:
            if doc_type.name == 'Паспорт РФ':
                if not re.fullmatch(r'^\d{10}$', doc_number):
                    raise ValidationError({
                        'doc_number': 'Для паспорта РФ введите ровно 10 цифр'
                    })
            elif doc_type.name == 'Свидетельство о рождении':
                if not re.fullmatch(r'^[IVXLCDM]{1,3}[А-ЯЁ]{2}\d{6}$', doc_number, re.IGNORECASE):
                    raise ValidationError({
                        'doc_number': 'Формат свидетельства: 1-3 римские цифры, 2 буквы, 6 цифр (пример: XIIАБ123456)'
                    })

        return cleaned_data
