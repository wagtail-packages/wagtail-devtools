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
    get_registered_modeladmin,
    wagtail_core_edit_pages_config,
    wagtail_core_listing_pages_config,
)
from wagtail_devtools.api.helpers import (
    generate_title,
    get_admin_edit_url,
    get_backend_response,
    get_creatable_page_models,
    get_frontend_response,
    get_host,
    get_model_admin_models,
    init_ret,
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
    It will check the response status code for each form submissions listing page."""

    session = session_login(request)
    models = []

    for model in get_page_models():
        if "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]:
            models.append(apps.get_model(model._meta.app_label, model.__name__))

    ret = init_ret("Form types")

    results = []

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

    ret = init_ret("Model admin types")

    if not get_registered_modeladmin():
        return JsonResponse(ret, safe=False)

    registered_modeladmin = get_registered_modeladmin()
    model_admins = get_model_admin_models(registered_modeladmin)

    for item in model_admins:
        be_response = get_backend_response(session, item)
        ret["results"].append(results_item(session, item, None, be_response))

    return JsonResponse(ret, safe=False)


def page_model_types(request):
    """API view for page model types.
    It will check the response status code for each edit url and one front end page return the results.
    """

    session = session_login(request)

    ret = init_ret("Page model types")

    for page_model in get_creatable_page_models():
        pages = page_model.objects.live()
        if pages:
            if item := pages.first():
                fe_response = get_frontend_response(session, item)
                be_response = get_backend_response(session, item)

                ret["results"].append(
                    results_item(request, item, fe_response, be_response)
                )

    return JsonResponse(ret, safe=False)


def settings_types(request):
    """API view for settings types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = init_ret("Settings types")

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

    ret = init_ret("Snippet types")

    for cls in get_snippet_models():
        item = cls.objects.first()
        be_response = get_backend_response(session, item)
        ret["results"].append(results_item(request, item, None, be_response))

    return JsonResponse(ret, safe=False)


def wagtail_core_edit_pages(request):
    """API view for wagtail core edit pages.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)

    ret = init_ret("Wagtail core edit pages")

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

    ret = init_ret("Wagtail core listing pages")

    for page in wagtail_core_listing_pages_config():
        editor_url = f"{get_host(request)}{reverse(page)}"
        be_response = get_backend_response(session, page, editor_url)

        ret["results"].append(
            results_item(
                request,
                None,
                None,
                be_response,
                defaults={
                    "title": generate_title(page),
                    "editor_url": editor_url,
                    "editor_status_code": be_response.status_code,
                    "editor_status_text": be_response.reason,
                    "fe_url": None,
                    "fe_status_code": None,
                    "fe_status_text": None,
                    "app_name": None,
                    "class_name": None,
                },
            )
        )

    return JsonResponse(ret, safe=False)
