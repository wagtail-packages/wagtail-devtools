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


def rewrite_installed_apps(apps):
    """Rewrite installed apps to be compatible with the core API"""
    return [
        app.replace(".contrib.", "")
        .replace("_", "")
        .replace(".", "")
        .replace("documents", "docs")
        .replace("apiv2", "api_v2")
        .strip()
        for app in apps
    ]


def installed_apps():
    if hasattr(settings, "WAGTAIL_DEVTOOLS_INSTALLED_APPS"):
        return settings.WAGTAIL_DEVTOOLS_INSTALLED_APPS

    custom = (
        settings.WAGTAIL_DEVTOOLS_CUSTOM_INSTALLED_APPS
        if hasattr(settings, "WAGTAIL_DEVTOOLS_CUSTOM_INSTALLED_APPS")
        else []
    )

    core = [
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

    all_apps = custom + rewrite_installed_apps(core) + ["wagtailcore", "auth"]

    return all_apps
