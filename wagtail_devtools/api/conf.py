from django.apps import apps
from django.conf import settings


LISTING_PAGES_CONFIG = {
    "wagtail.contrib.search_promotions": {
        "title": "Search promotions",
        "app_name": "wagtailsearchpromotions",
        "listing_name": "wagtailsearchpromotions:index",
    },
    "wagtail.contrib.forms": {
        "title": "Forms",
        "app_name": "wagtailforms",
        "listing_name": "wagtailforms:index",
    },
    "wagtail.contrib.redirects": {
        "title": "Redirects",
        "app_name": "wagtailredirects",
        "listing_name": "wagtailredirects:index",
    },
    "wagtail.users": {
        "title": "Users",
        "app_name": "wagtailusers",
        "listing_name": "wagtailusers_users:index",
    },
    "wagtail.snippets": {
        "title": "Snippets",
        "app_name": "wagtailsnippets",
        "listing_name": "wagtailsnippets:index",
    },
    "wagtail.documents": {
        "title": "Documents",
        "app_name": "wagtaildocs",
        "listing_name": "wagtaildocs:index",
    },
    "wagtail.images": {
        "title": "Images",
        "app_name": "wagtailimages",
        "listing_name": "wagtailimages:index",
    },
    "wagtail.search": {
        "title": "Search",
        "app_name": "wagtailsearch",
        "listing_name": "wagtailadmin_pages:search",
    },
    "wagtail.contrib.styleguide": {
        "title": "Styleguide",
        "app_name": "wagtailstyleguide",
        "listing_name": "wagtailstyleguide",
    },
    "wagtail.sites": {
        "title": "Sites",
        "app_name": "wagtailsites",
        "listing_name": "wagtailsites:index",
    },
    "wagtail.admin": [
        {
            "title": "Dashboard",
            "app_name": None,
            "listing_name": "wagtailadmin_home",
        },
        {
            "title": "Collections",
            "app_name": None,
            "listing_name": "wagtailadmin_collections:index",
        },
        {
            "title": "Login",
            "app_name": None,
            "listing_name": "wagtailadmin_login",
        },
        {
            "title": "Password reset",
            "app_name": None,
            "listing_name": "wagtailadmin_password_reset",
        },
        {
            "title": "Reports Locked Pages",
            "app_name": None,
            "listing_name": "wagtailadmin_reports:locked_pages",
        },
        {
            "title": "Reports Aging Pages",
            "app_name": None,
            "listing_name": "wagtailadmin_reports:aging_pages",
        },
        {
            "title": "Reports Site History",
            "app_name": None,
            "listing_name": "wagtailadmin_reports:site_history",
        },
        {
            "title": "Reports Workflow",
            "app_name": None,
            "listing_name": "wagtailadmin_reports:workflow",
        },
        {
            "title": "Reports Workflow Tasks",
            "app_name": None,
            "listing_name": "wagtailadmin_reports:workflow_tasks",
        },
        {
            "title": "Reports Workflows",
            "app_name": None,
            "listing_name": "wagtailadmin_workflows:index",
        },
        {
            "title": "Groups",
            "app_name": None,
            "listing_name": "wagtailusers_groups:index",
        },
        {
            "title": "Example Calendar (admin view)",
            "app_name": None,
            "listing_name": "calendar",
        },
        {
            "title": "Example Calendar (admin view - month)",
            "app_name": None,
            "listing_name": "calendar-month",
        },
    ],
}

if (
    hasattr(settings, "DEVTOOLS_LISTING_PAGES_REPLACE")
    and settings.DEVTOOLS_LISTING_PAGES_REPLACE
):
    LISTING_PAGES_CONFIG = {}

if hasattr(settings, "DEVTOOLS_LISTING_PAGES"):
    LISTING_PAGES_CONFIG.update(settings.DEVTOOLS_LISTING_PAGES)


def get_wagtail_core_listing_pages_config():
    configuration = {
        "title": "Wagtail core listing pages",
        "apps": [],
    }

    for app, config in LISTING_PAGES_CONFIG.items():
        if app not in settings.INSTALLED_APPS:
            break
        if isinstance(config, dict):
            if not config["listing_name"]:
                continue
            configuration["apps"].append(
                {
                    "title": config["title"],
                    "app_name": config["app_name"],
                    "listing_name": config["listing_name"],
                }
            )
        elif isinstance(config, list):
            for item in config:
                if not item["listing_name"]:
                    continue
                configuration["apps"].append(
                    {
                        "title": item["title"],
                        "app_name": item["app_name"],
                        "listing_name": item["listing_name"],
                    }
                )

    return configuration


def get_wagtail_core_edit_pages_config():
    configuration = {
        "title": "Wagtail core edit pages",
        "apps": [],
    }

    for a in apps.get_app_configs():
        configuration["apps"].append(
            {
                "app_name": a.label,
                "label": a.name,
                "models": [apps.get_model(a.label, m).__name__ for m in a.models],
            }
        )

    return configuration
