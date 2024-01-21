from django.apps import apps
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models.collections import Collection

from wagtail_devtools.api.conf import wagtail_core_listing_pages_config
from wagtail_devtools.api.dataclasses import ResultsListingItem, ResultsModelItem
from wagtail_devtools.api.helpers import get_host, init_ret, mangle_installed_apps


def wagtail_core_listing_pages_serializer(request, title):
    ret = init_ret(title)

    for page in wagtail_core_listing_pages_config():
        editor_url = f"{get_host(request)}{reverse(page)}"

        ret["results"].append(ResultsListingItem(request, page, editor_url).get())

    return ret


def wagtail_core_apps_serializer(request, title):
    ret = init_ret(title)

    a = [
        "wagtail.contrib.search_promotions",
        "wagtail.contrib.forms",
        "wagtail.contrib.redirects",
        "wagtail.contrib.settings",
        "wagtail.embeds",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail.api.v2",
        "wagtail.contrib.modeladmin",
        "wagtail.contrib.routable_page",
        "wagtail.contrib.styleguide",
        "wagtail.sites",
    ]

    all_apps = (
        ["wagtail_devtools_test"] + mangle_installed_apps(a) + ["wagtailcore", "auth"]
    )

    for app in all_apps:
        models = apps.get_app_config(app).get_models()
        for model in models:
            item = model.objects.first()
            if isinstance(item, Collection):
                item = Collection.objects.first().get_first_child()
            if AdminURLFinder().get_edit_url(item):
                ret["results"].append(ResultsModelItem(request, item).get())

    return ret
