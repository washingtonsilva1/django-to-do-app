from math import ceil
from django.core.paginator import Paginator


def custom_pagination_range(page_range, current_page, pages_to_display):
    middle_page = ceil(pages_to_display / 2)
    first_page = current_page - middle_page
    last_page = current_page + middle_page
    total_pages = len(page_range)
    if current_page >= total_pages - middle_page:
        first_page = total_pages - pages_to_display
        last_page = total_pages
    if current_page < middle_page:
        first_page = 0
        last_page = pages_to_display
    return {
        'pagination': page_range[first_page:last_page],
        'page_range': page_range,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'total_pages': total_pages,
        'first_page_out_of_range': current_page > middle_page,
        'last_page_out_of_range': current_page < total_pages - middle_page,
    }


def custom_paginator(request, query_set, objects_per_page, pages_to_display):
    paginator = Paginator(query_set, objects_per_page)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)
    custom_page_range = custom_pagination_range(
        page_range=paginator.page_range,
        current_page=page.number,
        pages_to_display=pages_to_display
    )
    return {
        'page_range': custom_page_range,
        'page': page,
    }
