from django.core.paginator import Paginator


def paginator(request, items_list, show_lmt):
    paginator = Paginator(items_list, show_lmt)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj