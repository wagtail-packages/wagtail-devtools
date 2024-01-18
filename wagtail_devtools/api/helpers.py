from urllib.parse import urlparse

from django.apps import apps
from django.conf import settings
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


def get_creatable_page_models():
    return [model for model in get_page_models() if model.is_creatable]


def get_form_page_models():
    models = []
    for model in get_page_models():
        if "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]:
            models.append(apps.get_model(model._meta.app_label, model.__name__))
    return models


def get_model_admin_models(model_admin_types):
    return [apps.get_model(item).objects.first() for item in model_admin_types]
