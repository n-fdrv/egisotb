from datetime import datetime
from datetime import timezone as dt_timezone

import pytz
from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name="field_type")
def field_type(field, type):
    return field.as_widget(attrs={"type": type})


@register.filter
def to_msk(value):
    if not value:
        return "–"
    try:
        value = datetime.strptime(value, "%d.%m.%Y %H:%M")
        value = timezone.make_aware(value, timezone=dt_timezone.utc)
        msk_time = value.astimezone(pytz.timezone("Europe/Moscow"))
        return msk_time.strftime("%d.%m.%Y %H:%M")
    except Exception as e:
        print(e)
        return "–"
