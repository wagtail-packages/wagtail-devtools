from django.http import JsonResponse
from django.urls import reverse
from wagtail.models import Site

from wagtail_devtools.api.conf import (
    get_wagtail_core_edit_pages_config,
    get_wagtail_core_listing_pages_config,
)

# from wagtail_devtools.api.helpers import get_host
from wagtail_devtools.api.serializers import (
    wagtail_core_apps_serializer,
    wagtail_core_listing_pages_serializer,
)


def get_host(request=None):
    if request:
        return request.build_absolute_uri("/").rstrip("/")
    return None


def api_view(request):
    """API index view for wagtail-devtools."""
    sites = Site.objects.all()
    params = ""

    if request.GET.get("all"):
        params = "?all=1"

    ret = {
        "api-views": [
            f"{get_host(request)}{reverse('listing-types')}{params}",
            f"{get_host(request)}{reverse('wagtail-core-apps')}{params}",
        ],
    }

    for site in sites:
        site_absolute_url = site.root_url
        request_absolute_url = get_host(request)

        if site_absolute_url != request_absolute_url:
            ret["api-views"].append(
                f"{site_absolute_url}{reverse('wagtail-core-apps')}{params}",
            )

    return JsonResponse(ret, safe=False)


def wagtail_core_listing_pages(request):
    """API view for wagtail core listing pages."""
    return JsonResponse(
        wagtail_core_listing_pages_serializer(
            request,
            get_wagtail_core_listing_pages_config(),
            "Wagtail core listing pages",
        ),
        safe=False,
    )


def wagtail_core_apps(request):
    """API view for wagtail core apps."""

    if not request.GET.get("all"):
        return JsonResponse(
            wagtail_core_apps_serializer(
                request, get_wagtail_core_edit_pages_config(), "Wagtail core apps"
            ),
            safe=False,
        )
    return JsonResponse(
        wagtail_core_apps_serializer(
            request, get_wagtail_core_edit_pages_config(), "Wagtail core apps", True
        ),
        safe=False,
    )
