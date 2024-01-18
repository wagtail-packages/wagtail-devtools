from django.http import JsonResponse
from django.urls import reverse

from wagtail_devtools.api.helpers import get_host
from wagtail_devtools.api.serializers import (
    form_types_serializer,
    model_admin_types_serializer,
    page_model_types_serializer,
    settings_types_serializer,
    snippet_types_serializer,
    wagtail_core_edit_pages_serializer,
    wagtail_core_listing_pages_serializer,
)


def api_view(request):
    """API index view for wagtail-devtools."""

    ret = {
        "api-views": [
            f"{get_host(request)}{reverse('edit-types')}",
            f"{get_host(request)}{reverse('form-types')}",
            f"{get_host(request)}{reverse('listing-types')}",
            f"{get_host(request)}{reverse('modeladmin-types')}",
            f"{get_host(request)}{reverse('page-types')}",
            f"{get_host(request)}{reverse('settings-types')}",
            f"{get_host(request)}{reverse('snippet-types')}",
        ]
    }
    return JsonResponse(ret, safe=False)


def form_types(request):
    """API view for form types.
    It will check the response status code for each form submissions listing page."""

    results = form_types_serializer(request, "Form types")

    return JsonResponse(results, safe=False)


def model_admin_types(request):
    """API view for model admin types.
    It will check the response status code for each edit url and return the results."""

    results = model_admin_types_serializer(request, "Model admin types")

    return JsonResponse(results, safe=False)


def page_model_types(request):
    """API view for page model types.
    It will check the response status code for each edit url and one front end page return the results.
    """

    results = page_model_types_serializer(request, "Page model types")

    return JsonResponse(results, safe=False)


def settings_types(request):
    """API view for settings types.
    It will check the response status code for each edit url and return the results."""

    results = settings_types_serializer(request, "Settings types")

    return JsonResponse(results, safe=False)


def snippet_types(request):
    """API view for snippet types.
    It will check the response status code for each edit url and return the results."""

    results = snippet_types_serializer(request, "Snippet types")

    return JsonResponse(results, safe=False)


def wagtail_core_edit_pages(request):
    """API view for wagtail core edit pages.
    It will check the response status code for each edit url and return the results."""

    results = wagtail_core_edit_pages_serializer(request, "Wagtail core edit pages")

    return JsonResponse(results, safe=False)


def wagtail_core_listing_pages(request):
    """API view for wagtail core listing pages.
    It will check the response status code for each edit url and return the results."""

    results = wagtail_core_listing_pages_serializer(
        request, "Wagtail core listing pages"
    )

    return JsonResponse(results, safe=False)
