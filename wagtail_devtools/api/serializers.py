from django.apps import apps
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Collection
from wagtail.snippets.models import get_snippet_models

from wagtail_devtools.api.dataclasses import (
    Results,
    ResultsListingItem,
    ResultsModelItem,
)
from wagtail_devtools.api.helpers import init_ret


def wagtail_core_listing_pages_serializer(request, config, title):
    ret = init_ret(title)
    results = Results()

    for app in config["apps"]:
        results.add(ResultsListingItem(request, app).get())

    ret["results"] = results.get()

    return ret


def wagtail_core_apps_serializer(request, config, title, all=False):
    ret = init_ret(title)

    # Making the assumption here that any page visible on the frontend will have an editor url

    results = Results()

    for app in config["apps"]:
        models = apps.get_app_config(app["app_name"]).get_models()
        if not all:
            for model in models:
                item = model.objects.first()
                if isinstance(item, Collection):
                    item = Collection.objects.first().get_first_child()
                if AdminURLFinder().get_edit_url(item):
                    results.add(ResultsModelItem(request, item).get())
        else:
            for model in models:
                items = model.objects.all()
                if isinstance(items.first(), Collection):
                    for item in items:
                        # if AdminURLFinder().get_edit_url(item): # TODO decide if this is required, do some testing on real data
                        results.add(ResultsModelItem(request, item).get())
                snippet_models = [model.__name__ for model in get_snippet_models()]
                if model.__name__ in snippet_models:
                    for item in items:
                        # if AdminURLFinder().get_edit_url(item): # TODO decide if this is required, do some testing on real data
                        results.add(ResultsModelItem(request, item).get())
                else:
                    for item in items:
                        if AdminURLFinder().get_edit_url(item):
                            results.add(ResultsModelItem(request, item).get())

    ret["results"] = results.get()

    return ret
