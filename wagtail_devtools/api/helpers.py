import requests

from django.conf import settings
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import get_page_models


def get_host(request):
    if not request.GET.get("host"):
        return settings.WAGTAILADMIN_BASE_URL

    return (
        request.GET.get("host")
        if request.GET.get("host").startswith("http")
        else f"http://{request.GET.get('host')}"
    )


def get_admin_edit_url(host, obj):
    return f"{get_host(host)}{AdminURLFinder().get_edit_url(obj)}"


def filter_page_models():
    """Filter out page models that are not creatable or are in the core apps."""

    filtered_page_models = []

    for page_model in get_page_models():
        if page_model._meta.app_label == "wagtailcore":
            # Skip the core apps
            continue
        if not page_model.is_creatable:
            # Skip pages that can't be created
            continue
        filtered_page_models.append(page_model)

    return filtered_page_models


def session_login(request):
    session = requests.Session()
    session.get(f"{get_host(request)}{reverse('wagtailadmin_login')}")
    login_data = {
        "username": "superuser",
        "password": "superuser",
        "csrfmiddlewaretoken": session.cookies["csrftoken"],
    }
    session.post(f"{get_host(request)}{reverse('wagtailadmin_login')}", data=login_data)

    return session


def get_model_admin_types():
    if not hasattr(settings, "WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES"):
        return [
            "wagtail_devtools_test.TestModelAdminOne",
            "wagtail_devtools_test.TestModelAdminTwo",
            "wagtail_devtools_test.TestModelAdminThree",
        ]
    return settings.WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES


def results_base(request, url_name, models):
    defaults = {
        "index": [
            f"{get_host(request)}{reverse(url_name)}",
        ],
        "meta": {
            "host": get_host(request),
            "fe_OK": 0,
            "fe_500_ERROR": 0,
            "fe_404_Response": 0,
            "be_OK": 0,
            "be_500_ERROR": 0,
            "be_404_Response": 0,
            "total_checks": 0,
            "index": [],
        },
        "results": [],
    }
    if models:
        defaults["meta"]["total_checks"] = len(models)

    return defaults


def results_item(request, item, fe_response, be_response, **kwargs):
    if kwargs.get("defaults"):
        defaults = kwargs.get("defaults")
    else:
        defaults = {
            "title": None,
            "editor_url": None,
            "editor_status_code": None,
            "editor_status_text": None,
            "fe_url": None,
            "fe_status_code": None,
            "fe_status_text": None,
            "app_name": None,
            "class_name": None,
        }

        if item:
            if hasattr(item, "title"):
                defaults["title"] = item.title
            elif hasattr(item, "name"):
                defaults["title"] = item.name
            elif hasattr(item, "hostname"):
                defaults["title"] = item.hostname
            elif hasattr(item, "username"):
                defaults["title"] = item.username
            else:
                defaults["title"] = item.__str__()

            # Not all items have a front-end URL
            if hasattr(item, "get_url"):
                defaults["fe_url"] = item.get_url()
                defaults["fe_status_code"] = fe_response.status_code
                defaults["fe_status_text"] = fe_response.reason

            defaults["fe_url"] = item.get_url() if hasattr(item, "get_url") else None
            defaults["editor_url"] = f"{get_admin_edit_url(request, item)}"
            defaults["app_name"] = item._meta.app_label
            defaults["class_name"] = item.__class__.__name__

            defaults["editor_status_code"] = be_response.status_code
            defaults["editor_status_text"] = be_response.reason

    return defaults
