from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder

# from wagtail.models import Site
from wagtail.snippets.models import get_snippet_models

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


# def api_view(request):
#     """API index view for wagtail-devtools."""
#     sites = Site.objects.all()
#     params = ""

#     if request.GET.get("all"):
#         params = "?all=1"

#     ret = {
#         "api-views": [
#             f"{get_host(request)}{reverse('listing-types')}{params}",
#             f"{get_host(request)}{reverse('wagtail-core-apps')}{params}",
#         ],
#     }

#     for site in sites:
#         site_absolute_url = site.root_url
#         request_absolute_url = get_host(request)

#         if site_absolute_url != request_absolute_url:
#             ret["api-views"].append(
#                 f"{site_absolute_url}{reverse('wagtail-core-apps')}{params}",
#             )

#     return JsonResponse(ret, safe=False)


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


def responses_api_view(request):
    if request.GET.get("url"):
        url = request.GET.get("url")
    else:
        url = "http://localhost:8000"

    if request.GET.get("all"):
        all = True
    else:
        all = False

    results = []  # list of tuples (url, name)

    for app in get_wagtail_core_listing_pages_config()["apps"]:
        list_url = f"{url}{reverse(app['listing_name'])}"
        results.append(
            {
                "group": "CoreListingPage",
                "name": f"{app['title']} ({app['listing_name']})",
                "url": list_url,
            }
        )

    configuration = {
        "title": "Wagtail core edit pages",
        "apps": [],
    }

    for a in apps.get_app_configs():
        if hasattr(settings, "DEVTOOLS_APPS_EXCLUDE"):
            if a.name in settings.DEVTOOLS_APPS_EXCLUDE:
                continue
        configuration["apps"].append(
            {
                "app_name": a.label,
                "models": [apps.get_model(a.label, m).__name__ for m in a.models],
            }
        )

    for app in configuration["apps"]:
        models = apps.get_app_config(app["app_name"]).get_models()
        for model in models:
            is_collection = model.__name__ == "Collection"
            is_snippet = model.__name__ in [
                model.__name__ for model in get_snippet_models()
            ]

            if is_collection:
                items = (
                    # don't include the root collection
                    [model.objects.first().get_first_child()]
                    if not all
                    else model.objects.all().exclude(depth=1)
                )

            if is_snippet:
                items = [model.objects.first()] if not all else model.objects.all()

            if not is_collection and not is_snippet:
                # must be some other model that doesn't need special handling
                items = [model.objects.first()] if not all else model.objects.all()

            for item in items:
                if AdminURLFinder().get_edit_url(item):
                    results.append(
                        {
                            "group": "CoreEditPage",
                            "name": f"{model.__name__} ({app['app_name']})",
                            "url": f"{url}{AdminURLFinder().get_edit_url(item)}",
                        }
                    )
                    if hasattr(item, "get_url") and item.get_url():
                        results.append(
                            {
                                "group": "SitePage",
                                "name": f"{model.__name__} ({app['app_name']})",
                                "url": item.get_url(),
                            }
                        )

        sorted_results = sorted(results, key=lambda x: x["group"])

    return JsonResponse(sorted_results, safe=False)
