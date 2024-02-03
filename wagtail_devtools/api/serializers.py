from django.apps import apps
from wagtail.admin.admin_url_finder import AdminURLFinder
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

    """
    Loop though all the apps and models and get the first item for each model
    But pages need to be children of the current site
    """

    for app in config["apps"]:
        models = apps.get_app_config(app["app_name"]).get_models()
        for model in models:
            is_collection = model.__name__ == "Collection"
            is_snippet = model.__name__ in [
                model.__name__ for model in get_snippet_models()
            ]

            if is_collection:
                items = (
                    # don't include the root collection
                    [model.objects.first().get_first_child()]
                    if not all
                    else model.objects.all().exclude(depth=1)
                )

            if is_snippet:
                items = [model.objects.first()] if not all else model.objects.all()

            if not is_collection and not is_snippet:
                # must be some other model that doesn't need special handling
                items = [model.objects.first()] if not all else model.objects.all()

            for item in items:
                if AdminURLFinder().get_edit_url(item):
                    results.add(ResultsModelItem(request, item).get())

    ret["results"] = results.get()

    return ret
