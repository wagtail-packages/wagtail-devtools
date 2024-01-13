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

from wagtail_devtools.api.helpers import (
    get_admin_edit_url,
    get_host,
    get_model_admin_types,
    results_base,
    results_item,
    session_login,
)


def api_view(request):
    """API index view for wagtail-devtools."""

    ret = {
        "api-views": [
            f"{get_host(request)}{reverse('get_page_model_types')}",
            f"{get_host(request)}{reverse('get_wagtail_core_listing_pages')}",
            f"{get_host(request)}{reverse('get_wagtail_core_edit_pages')}",
            f"{get_host(request)}{reverse('get_settings_types')}",
            f"{get_host(request)}{reverse('get_snippet_types')}",
            f"{get_host(request)}{reverse('get_model_admin_types')}",
            f"{get_host(request)}{reverse('get_form_types')}",
        ]
    }
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

    ret = results_base(request, "api_view", page_models)
    index = []

    for page_model in page_models:
        if item := page_model.objects.first():
            fe_response = session.get(item.get_url())

            if fe_response.status_code == 200:
                ret["meta"]["fe_OK"] += 1
            if fe_response.status_code == 500:
                ret["meta"]["fe_500_ERROR"] += 1
            if fe_response.status_code == 404:
                ret["meta"]["fe_404_Response"] += 1

            be_response = session.get(f"{get_admin_edit_url(request, item)}")

            if be_response.status_code == 200:
                ret["meta"]["be_OK"] += 1
            if be_response.status_code == 500:
                ret["meta"]["be_500_ERROR"] += 1
            if be_response.status_code == 404:
                ret["meta"]["be_404_Response"] += 1

            ret["results"].append(results_item(request, item, fe_response, be_response))

            index.append(item.__class__.__name__)

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def wagtail_core_listing_pages(request):
    """API view for wagtail core listing pages.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    listing_pages = [
        # DASHBOARD
        ("DASHBOARD", f"{reverse('wagtailadmin_home')}"),
        # PAGES LIST
        ("PAGES list", f"{reverse('wagtailadmin_explore_root')}"),
        # SEARCH PAGES
        ("SEARCH all", f"{reverse('wagtailadmin_pages:search')}"),
        # AGING PAGES
        ("AGING PAGES list", f"{reverse('wagtailadmin_reports:aging_pages')}"),
        # COLLECTIONS
        ("COLLECTIONS list", f"{reverse('wagtailadmin_collections:index')}"),
        # DOCUMENTS
        ("DOCUMENTS list", f"{reverse('wagtaildocs:index')}"),
        # GROUPS
        ("GROUPS list", f"{reverse('wagtailusers_groups:index')}"),
        # IMAGES
        ("IMAGES list", f"{reverse('wagtailimages:index')}"),
        # LOCKED PAGES
        ("LOCKED PAGES list", f"{reverse('wagtailadmin_reports:locked_pages')}"),
        # REDIRECTS
        ("REDIRECTS list", f"{reverse('wagtailredirects:index')}"),
        # SITES
        ("SITES list", f"{reverse('wagtailsites:index')}"),
        # SITE HISTORY
        ("SITE HISTORY list", f"{reverse('wagtailadmin_reports:site_history')}"),
        # SNIPPETS
        ("SNIPPETS list", f"{reverse('wagtailsnippets:index')}"),
        # USERS
        ("USERS list", f"{reverse('wagtailusers_users:index')}"),
        # WORKFLOWS
        ("WORKFLOWS list", f"{reverse('wagtailadmin_workflows:index')}"),
        # WORKFLOWS TASKS
        ("WORKFLOWS TASKS list", f"{reverse('wagtailadmin_workflows:task_index')}"),
    ]

    ret = results_base(request, "api_view", listing_pages)
    index = []

    for page in listing_pages:
        response = session.get(f"{get_host(request)}{page[1]}")
        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        ret["results"].append(
            results_item(
                request,
                None,
                None,
                response,
                defaults={
                    "title": page[0],
                    "editor_url": f"{get_host(request)}{page[1]}",
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

        index.append(page[0])

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def wagtail_core_edit_pages(request):
    """API view for wagtail core edit pages.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    edit_pages = [
        # COLLECTIONS edit
        ("COLLECTIONS edit", "wagtailcore", "Collection"),
        # DOCUMENTS edit
        ("DOCUMENTS edit", "wagtaildocs", "Document"),
        # GROUPS edit
        ("GROUPS edit", "auth", "Group"),
        # IMAGES edit
        ("IMAGES edit", "wagtailimages", "Image"),
        # REDIRECTS edit
        ("REDIRECTS edit", "wagtailredirects", "Redirect"),
        # SITES edit
        ("SITES edit", "wagtailcore", "Site"),
        # USERS edit
        ("USERS edit", "auth", "User"),
        # WORKFLOWS edit
        ("WORKFLOWS edit", "wagtailcore", "Workflow"),
        # WORKFLOWS TASK edit
        ("WORKFLOWS TASK edit", "wagtailcore", "Task"),
    ]

    ret = results_base(request, "api_view", edit_pages)
    index = []

    for item in edit_pages:
        model = apps.get_model(item[1], item[2])
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

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        ret["results"].append(results_item(request, first, None, response))

        index.append(item[0])

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def settings_types(request):
    """API view for settings types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    edit_pages = [
        # SETTINGS edit
        ("SETTINGS edit", settings_registry),
    ]

    ret = results_base(request, "api_view", edit_pages)
    index = []
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

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        ret["results"].append(results_item(request, obj, None, response))

        index.append(obj.__class__.__name__)

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def snippet_types(request):
    """API view for snippet types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    edit_pages = [
        # SNIPPETS edit
        ("SNIPPETS edit", get_snippet_models()),
    ]
    ret = results_base(request, "api_view", edit_pages)
    index = []

    for cls in get_snippet_models():
        obj = cls.objects.first()

        response = session.get(f"{get_admin_edit_url(request, obj)}")

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        ret["results"].append(results_item(request, obj, None, response))

        index.append(obj.__class__.__name__)

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def model_admin_types(request):
    """API view for model admin types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    model_admin_types = get_model_admin_types()
    ret = results_base(request, "api_view", model_admin_types)
    index = []

    for item in model_admin_types:
        model = apps.get_model(item)
        first = model.objects.first()

        response = session.get(f"{get_admin_edit_url(request, first)}")

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        ret["results"].append(results_item(request, first, None, response))

        index.append(item)

    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)


def form_types(request):
    """API view for form types.
    It will check the response status code for each edit url and return the results."""

    session = session_login(request)
    index = []
    models = []
    results = []

    for model in get_page_models():
        if "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]:
            models.append(apps.get_model(model._meta.app_label, model.__name__))

    ret = results_base(request, "api_view", models)

    for model in models:
        first = model.objects.first()

        response = session.get(f"{get_admin_edit_url(request, first)}")

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

        results.append(results_item(request, first, response, response))

        index.append(model.__name__)

        editor_url = reverse("wagtailforms:list_submissions", args=[first.id])

        response = session.get(f"{get_host(request)}{editor_url}")

        if response.status_code == 200:
            ret["meta"]["be_OK"] += 1
        if response.status_code == 500:
            ret["meta"]["be_500_ERROR"] += 1
        if response.status_code == 404:
            ret["meta"]["be_404_Response"] += 1

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

    ret = results_base(request, "api_view", models)
    ret["results"] = results
    ret["meta"]["index"] = index

    return JsonResponse(ret, safe=False)
