from django import forms

from .models import Citizenship, DocType, Passenger


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["citizenship"].queryset = Citizenship.objects.all()
        self.fields["doc_type"].queryset = DocType.objects.all()
