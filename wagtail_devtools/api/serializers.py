from django.apps import apps
from django.contrib.auth import get_user_model
from django.urls import reverse
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.models.collections import Collection
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import (
    get_registered_modeladmin,
    wagtail_core_edit_pages_config,
    wagtail_core_listing_pages_config,
)
from wagtail_devtools.api.dataclasses import ResultsListingItem, ResultsModelItem
from wagtail_devtools.api.helpers import (
    get_creatable_page_models,
    get_form_page_models,
    get_host,
    get_model_admin_models,
    init_ret,
)


def form_types_serializer(request, title):
    ret = init_ret(title)

    for model in get_form_page_models():
        item = model.objects.first()
        ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def model_admin_types_serializer(request, title):
    if not get_registered_modeladmin():
        return {}

    ret = init_ret(title)

    registered_modeladmin = get_registered_modeladmin()
    model_admins = get_model_admin_models(registered_modeladmin)

    for item in model_admins:
        ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def wagtail_core_edit_pages_serializer(request, title):
    ret = init_ret(title)

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

        ret["results"].append(ResultsModelItem(request, first).get())

    return ret


def wagtail_core_listing_pages_serializer(request, title):
    ret = init_ret(title)

    for page in wagtail_core_listing_pages_config():
        editor_url = f"{get_host(request)}{reverse(page)}"

        ret["results"].append(ResultsListingItem(request, page, editor_url).get())

    return ret


def page_model_types_serializer(request, title):
    ret = init_ret(title)

    for page_model in get_creatable_page_models():
        pages = page_model.objects.live()
        if pages:
            if item := pages.first():
                ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def settings_types_serializer(request, title):
    ret = init_ret(title)

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

    for item in objects:
        ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def snippet_types_serializer(request, title):
    ret = init_ret(title)

    for cls in get_snippet_models():
        item = cls.objects.first()
        ret["results"].append(ResultsModelItem(request, item).get())

    return ret
