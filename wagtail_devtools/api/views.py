from django.apps import apps
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.models import get_page_models
from wagtail.models.collections import Collection
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import (
    get_model_admin_types,
    wagtail_core_edit_pages_config,
    wagtail_core_listing_pages_config,
)
from wagtail_devtools.api.helpers import (
    get_admin_edit_url,
    get_host,
    results_item,
    session_login,
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
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    models = []
    results = []

    for model in get_page_models():
        if "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]:
            models.append(apps.get_model(model._meta.app_label, model.__name__))

    ret = {"meta": {"title": "Form types"}, "results": []}

    for model in models:
        first = model.objects.first()

        response = session.get(f"{get_admin_edit_url(request, first)}")
        results.append(results_item(request, first, response, response))

        editor_url = reverse("wagtailforms:list_submissions", args=[first.id])

        response = session.get(f"{get_host(request)}{editor_url}")

        results.append(
            results_item(
                request,
                None,
                None,
                response,
                defaults={
                    "title": first.title,
                    "editor_url": f"{get_host(request)}{reverse('wagtailforms:list_submissions', args=[first.id])}",
                    "editor_status_code": response.status_code,
                    "editor_status_text": response.reason,
                    "fe_url": None,
                    "fe_status_code": None,
                    "fe_status_text": None,
                    "app_name": None,
                    "class_name": None,
                },
            )
        )

    ret["results"] = results

    return JsonResponse(ret, safe=False)


def model_admin_types(request):
    """API view for model admin types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    model_admin_types = get_model_admin_types()

    ret = {"meta": {"title": "Model admin types"}, "results": []}

    if not model_admin_types:
        return JsonResponse(ret, safe=False)

    for item in model_admin_types:
        model = apps.get_model(item)
        first = model.objects.first()

        response = session.get(f"{get_admin_edit_url(request, first)}")
        ret["results"].append(results_item(request, first, None, response))

    return JsonResponse(ret, safe=False)


def page_model_types(request):
    """API view for page model types.
    It will check the response status code for each edit url and one front end page return the results.
    """

    session = session_login(request)

    def filter_page_models():
        """Filter out page models that are not creatable or are in the core apps."""
        filtered_page_models = []
        for page_model in get_page_models():
            if page_model.is_creatable:
                filtered_page_models.append(page_model)
        return filtered_page_models

    page_models = filter_page_models()

    ret = {"meta": {"title": "Page model types"}, "results": []}

    for page_model in page_models:
        if item := page_model.objects.first():
            fe_response = session.get(item.get_url())
            be_response = session.get(f"{get_admin_edit_url(request, item)}")

            ret["results"].append(results_item(request, item, fe_response, be_response))

    return JsonResponse(ret, safe=False)


def settings_types(request):
    """API view for settings types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = {"meta": {"title": "Settings types"}, "results": []}

    generic_settings_model = None
    site_settings_model = None

    for cls in settings_registry:
        if (
            cls.__mro__[1].__name__ == "BaseGenericSetting"
            and not generic_settings_model
        ):
            generic_settings_model = cls.objects.first()
            continue
        if cls.__mro__[1].__name__ == "BaseSiteSetting" and not site_settings_model:
            site_settings_model = cls.objects.first()
            continue

    objects = [generic_settings_model, site_settings_model]

    for obj in objects:
        response = session.get(f"{get_admin_edit_url(request, obj)}")
        ret["results"].append(results_item(request, obj, None, response))

    return JsonResponse(ret, safe=False)


def snippet_types(request):
    """API view for snippet types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = {"meta": {"title": "Snippet types"}, "results": []}

    for cls in get_snippet_models():
        obj = cls.objects.first()

        response = session.get(f"{get_admin_edit_url(request, obj)}")
        ret["results"].append(results_item(request, obj, None, response))

    return JsonResponse(ret, safe=False)


def wagtail_core_edit_pages(request):
    """API view for wagtail core edit pages.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = {"meta": {"title": "Wagtail core edit pages"}, "results": []}

    for item in wagtail_core_edit_pages_config():
        model = apps.get_model(item.split(".")[0], item.split(".")[1])
        first = model.objects.first()

        if isinstance(first, Collection):
            first = Collection.objects.first().get_first_child()
        elif isinstance(first, get_document_model()):
            first = get_document_model().objects.first()
        elif isinstance(first, get_image_model()):
            first = get_image_model().objects.first()
        elif isinstance(first, get_user_model()):
            first = get_user_model().objects.first()
        else:
            first = model.objects.first()

        response = session.get(f"{get_admin_edit_url(request, first)}")

        ret["results"].append(results_item(request, first, None, response))

    return JsonResponse(ret, safe=False)


def wagtail_core_listing_pages(request):
    """API view for wagtail core listing pages.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = {"meta": {"title": "Wagtail core listing pages"}, "results": []}

    def generate_title(page):
        splits = page.split("_")
        splits = " ".join(splits)
        splits = splits.split(":")
        splits = " ".join(splits)
        splits = splits.replace("wagtail", "")
        splits = splits.lower()  # just in case

        def upper_words(s):
            return " ".join(w.capitalize() for w in s.split(" "))

        return upper_words(splits)

    for page in wagtail_core_listing_pages_config():
        response = session.get(f"{get_host(request)}{reverse(page)}")

        ret["results"].append(
            results_item(
                request,
                None,
                None,
                response,
                defaults={
                    "title": generate_title(page),
                    "editor_url": f"{get_host(request)}{reverse(page)}",
                    "editor_status_code": response.status_code,
                    "editor_status_text": response.reason,
                    "fe_url": None,
                    "fe_status_code": None,
                    "fe_status_text": None,
                    "app_name": None,
                    "class_name": None,
                },
            )
        )

    return JsonResponse(ret, safe=False)
