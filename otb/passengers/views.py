from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from core.middlewares.users import is_operator


@login_required
@user_passes_test(is_operator)
def passengers_list(request):
    return render(request, 'passengers/passenger_list.html')


@login_required
@user_passes_test(is_operator)
def crew_list(request):
    return render(request, 'crew_list.html')