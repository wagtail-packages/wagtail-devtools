from urllib.parse import urlparse

import requests

from django.apps import apps
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_str
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Site, get_page_models


def get_admin_edit_url(host, obj):
    return f"{get_host(host)}{AdminURLFinder().get_edit_url(obj)}"


def get_host(request=None):
    # Modified from wagtail.api.v2.utils.get_base_url
    if hasattr(settings, "WAGTAIL_DEVTOOLS_BASE_URL"):
        base_url = settings.WAGTAIL_DEVTOOLS_BASE_URL
    else:
        base_url = getattr(settings, "WAGTAILADMIN_BASE_URL", None)

    if base_url is None and request:
        site = Site.find_for_request(request)
        if site:
            base_url = site.root_url

    if base_url:
        # We only want the scheme and netloc
        base_url_parsed = urlparse(force_str(base_url))

        return base_url_parsed.scheme + "://" + base_url_parsed.netloc


def init_ret(title):
    return {"meta": {"title": title}, "results": []}


def results_item(request, item, editor_url=None):
    ret = {}

    if not editor_url:
        ret["title"] = (
            item.title
            if hasattr(item, "title")
            else item.name
            if hasattr(item, "name")
            else item.hostname
            if hasattr(item, "hostname")
            else item.username
            if hasattr(item, "username")
            else item.__str__()
        )
        ret["fe_url"] = item.get_url() if hasattr(item, "get_url") else None
        ret["editor_url"] = f"{get_admin_edit_url(request, item)}"
        # TODO: Add app_name and class_name
        # ret["app_name"] = item._meta.app_label
        # ret["class_name"] = item.__class__.__name__
    else:
        ret["title"] = generate_title(item)
        ret["editor_url"] = editor_url

    return ret


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


def get_creatable_page_models():
    return [model for model in get_page_models() if model.is_creatable]


def get_form_page_models():
    models = []
    for model in get_page_models():
        if "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]:
            models.append(apps.get_model(model._meta.app_label, model.__name__))
    return models


def get_frontend_response(session, item):
    return session.get(item.get_url())


def get_backend_response(session, item, editor_url=None):
    if not editor_url:
        return session.get(f"{get_admin_edit_url(session, item)}")
    return session.get(editor_url)


def get_model_admin_models(model_admin_types):
    return [apps.get_model(item).objects.first() for item in model_admin_types]


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
