from django.apps import apps
from django.contrib.auth import get_user_model
from django.urls import reverse
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

    form_models = get_form_page_models()

    if len(form_models) > 0:
        for model in form_models:
            item = model.objects.first()
            ret["results"].append(ResultsModelItem(request, item).get())
    else:
        ret["results"].append(
            {
                "title": "No form pages found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )

    return ret


def model_admin_types_serializer(request, title):
    ret = init_ret(title)

    if not get_registered_modeladmin():
        ret["results"].append(
            {
                "title": "No modeladmin models found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret

    registered_modeladmin = get_registered_modeladmin()
    model_admins = get_model_admin_models(registered_modeladmin)

    if len(model_admins) == 0:
        ret["results"].append(
            {
                "title": "No modeladmin models found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret
    else:
        for item in model_admins:
            ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def wagtail_core_edit_pages_serializer(request, title):
    ret = init_ret(title)

    for item in wagtail_core_edit_pages_config():
        model = apps.get_model(item.split(".")[0], item.split(".")[1])

        if first := model.objects.first():
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

            if first:
                ret["results"].append(ResultsModelItem(request, first).get())
            else:
                ret["results"].append(
                    {
                        "title": "No pages found",
                        "app_name": None,
                        "class_name": None,
                        "editor_url": None,
                        "url": None,
                    }
                )

    return ret


def wagtail_core_listing_pages_serializer(request, title):
    ret = init_ret(title)

    for page in wagtail_core_listing_pages_config():
        editor_url = f"{get_host(request)}{reverse(page)}"

        ret["results"].append(ResultsListingItem(request, page, editor_url).get())

    return ret


def page_model_types_serializer(request, title):
    ret = init_ret(title)

    page_models = get_creatable_page_models()

    if len(page_models) == 0:
        ret["results"].append(
            {
                "title": "No page models found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret
    else:
        for page_model in page_models:
            pages = page_model.objects.live()
            if pages:
                if item := pages.first():
                    ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def settings_types_serializer(request, title):
    ret = init_ret(title)

    generic_settings_model = None
    site_settings_model = None

    try:
        from wagtail.contrib.settings.registry import registry as settings_registry
    except ImportError:
        ret["results"].append(
            {
                "title": "wagtail.contrib.settings not in INSTALLED_APPS",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret

    if not settings_registry:
        ret["results"].append(
            {
                "title": "No settings found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret

    for cls in settings_registry:
        if cls.__mro__[1].__name__ == "BaseGenericSetting":
            generic_settings_model = cls
        if cls.__mro__[1].__name__ == "BaseSiteSetting":
            site_settings_model = cls

    settings = [
        settings
        for settings in [generic_settings_model, site_settings_model]
        if settings
    ]

    if len(settings) == 0:
        ret["results"].append(
            {
                "title": "No settings found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret

    models = [cls.objects.first() for cls in settings_registry if cls.objects.first()]

    if len(models) == 0:
        ret["results"].append(
            {
                "title": "No settings objects found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret

    for item in models:
        ret["results"].append(ResultsModelItem(request, item).get())

    return ret


def snippet_types_serializer(request, title):
    ret = init_ret(title)

    snippets_types = get_snippet_models()

    if len(snippets_types) == 0:
        ret["results"].append(
            {
                "title": "No snippets found",
                "app_name": None,
                "class_name": None,
                "editor_url": None,
                "url": None,
            }
        )
        return ret
    else:
        for cls in snippets_types:
            item = cls.objects.first()
            ret["results"].append(ResultsModelItem(request, item).get())

    return ret
