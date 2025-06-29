from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from passenger.models import Passenger, DocType, Citizenship

from .forms import PassengerForm
from .utils import paginator


PASSENGER_SHOW_LIMIT = 30

def index(request):
    passengers = Passenger.objects.filter(is_active=True)
    page_obj = paginator(request, passengers, PASSENGER_SHOW_LIMIT)
    context = {
        'passengers': passengers,
        'page_obj': page_obj
    }
    return render(request, 'index.html', context)

@login_required
def passenger_list(request):
    passengers = Passenger.objects.filter(is_active=True)
    doc_types = DocType.objects.all()
    citizenships = Citizenship.objects.all()
    page_obj = paginator(request, passengers, PASSENGER_SHOW_LIMIT)
    if request.method == 'POST':
        form = PassengerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.created_by = request.user
            passenger.save()
            return redirect('passenger:passenger_list')
        return render(request, 'passenger/passenger_list.html', {'form': form})
    form = PassengerForm()
    context = {
        'passengers': passengers,
        'page_obj': page_obj,
        'doc_types': doc_types,
        'citizenships': citizenships,
        'form': form
    }
    return render(request, 'passenger/passenger_list.html', context)


def passenger_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')