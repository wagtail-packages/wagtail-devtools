from django.conf import settings


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


def default_field_identifier():
    if hasattr(settings, "WAGTAIL_DEVTOOLS_FIELD_IDENTIFIER"):
        return settings.WAGTAIL_DEVTOOLS_FIELD_IDENTIFIER
    return ["title", "name", "username", "hostname"]
