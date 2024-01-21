from django.conf import settings
from django.contrib.auth import get_user_model


def get_user_model_string():
    return f"{get_user_model()._meta.app_label}.{get_user_model()._meta.model_name.capitalize()}"


def wagtail_core_listing_pages_config():
    if hasattr(settings, "WAGTAIL_DEVTOOLS_LISTING_PAGES"):
        return settings.WAGTAIL_DEVTOOLS_LISTING_PAGES
    return [
        "wagtailadmin_collections:index",
        "wagtailadmin_explore_root",
        "wagtailadmin_home",
        "wagtailadmin_pages:search",
        "wagtailadmin_reports:aging_pages",
        "wagtailadmin_reports:locked_pages",
        "wagtailadmin_reports:site_history",
        "wagtailadmin_workflows:index",
        "wagtailadmin_workflows:task_index",
        "wagtaildocs:index",
        "wagtailimages:index",
        "wagtailredirects:index",
        "wagtailsites:index",
        "wagtailsnippets:index",
        "wagtailusers_groups:index",
        "wagtailusers_users:index",
    ]
