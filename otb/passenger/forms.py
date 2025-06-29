from django import forms

from .models import Passenger


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
            'gender'
        )

        widgets = {
            'birthday': forms.TextInput(attrs={'type': 'date'}),
        }

    def clean_text(self):
        data = self.cleaned_data['surname']
        if not data:
            raise forms.ValidationError('Пост не можеть быть без текста!')
        return data
