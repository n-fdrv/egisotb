from django.contrib import admin

from passenger.models import Passenger, DocType, Citizenship

admin.site.register(Passenger)
admin.site.register(DocType)
admin.site.register(Citizenship)
