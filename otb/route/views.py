from django.shortcuts import render

from route.models import Voyage


def voyage_detail(request, pk):
    schedule = Voyage.objects.get(pk=pk)
    context = {
        'schedule': schedule,
    }
    print(schedule)
    return render(request, 'schedule_detail.html', context)