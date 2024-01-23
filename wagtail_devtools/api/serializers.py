from django.apps import apps
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models.collections import Collection
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.conf import installed_apps, wagtail_core_listing_pages_config
from wagtail_devtools.api.dataclasses import ResultsListingItem, ResultsModelItem
from wagtail_devtools.api.helpers import get_host, init_ret


def wagtail_core_listing_pages_serializer(request, title):
    ret = init_ret(title)

    for page in wagtail_core_listing_pages_config():
        editor_url = f"{get_host(request)}{reverse(page)}"

        ret["results"].append(ResultsListingItem(request, page, editor_url).get())

    return ret


def wagtail_core_apps_serializer(request, title, all=False):
    ret = init_ret(title)

    for app in installed_apps():
        models = apps.get_app_config(app).get_models()
        if not all:
            for model in models:
                item = model.objects.first()
                if isinstance(item, Collection):
                    item = Collection.objects.first().get_first_child()
                if AdminURLFinder().get_edit_url(item):
                    ret["results"].append(ResultsModelItem(request, item).get())
        else:
            for model in models:
                items = model.objects.all()
                if isinstance(items.first(), Collection):
                    for item in items:
                        if AdminURLFinder().get_edit_url(item):
                            ret["results"].append(ResultsModelItem(request, item).get())
                snippet_models = [model.__name__ for model in get_snippet_models()]
                if model.__name__ in snippet_models:
                    for item in items:
                        if AdminURLFinder().get_edit_url(item):
                            ret["results"].append(ResultsModelItem(request, item).get())
                else:
                    for item in items:
                        if AdminURLFinder().get_edit_url(item):
                            ret["results"].append(ResultsModelItem(request, item).get())

    return ret
