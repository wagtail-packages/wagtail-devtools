import calendar

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils import timezone
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.models import Page


if WAGTAIL_VERSION < (6, 0):
    from wagtail.search.models import Query
else:
    from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )


def example_calendar(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    return render(
        request,
        "wagtailcalendar/example_calendar.html",
        {
            "current_year": current_year,
            "calendar_html": calendar_html,
        },
    )


def example_calendar_month(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    calendar_html = calendar.HTMLCalendar().formatmonth(current_year, current_month)

    return render(
        request,
        "wagtailcalendar/example_calendar.html",
        {
            "current_year": current_year,
            "calendar_html": calendar_html,
        },
    )
