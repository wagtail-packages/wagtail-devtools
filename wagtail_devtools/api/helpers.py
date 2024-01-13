from urllib.parse import urlparse

import requests

from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_str
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Site


def get_host(request=None):
    # Modified from wagtail.api.v2.utils.get_base_url
    base_url = getattr(settings, "WAGTAILADMIN_BASE_URL", None)

    if base_url is None and request:
        site = Site.find_for_request(request)
        if site:
            base_url = site.root_url

    if base_url:
        # We only want the scheme and netloc
        base_url_parsed = urlparse(force_str(base_url))

        return base_url_parsed.scheme + "://" + base_url_parsed.netloc


def get_admin_edit_url(host, obj):
    return f"{get_host(host)}{AdminURLFinder().get_edit_url(obj)}"


def wagtail_core_edit_pages_config():
    return [
        ("COLLECTIONS edit", "wagtailcore", "Collection"),
        ("DOCUMENTS edit", "wagtaildocs", "Document"),
        ("GROUPS edit", "auth", "Group"),
        ("IMAGES edit", "wagtailimages", "Image"),
        ("REDIRECTS edit", "wagtailredirects", "Redirect"),
        ("SITES edit", "wagtailcore", "Site"),
        ("USERS edit", "auth", "User"),
        ("WORKFLOWS edit", "wagtailcore", "Workflow"),
        ("WORKFLOWS TASK edit", "wagtailcore", "Task"),
    ]


def wagtail_core_listing_pages_config():
    return [
        ("DASHBOARD", f"{reverse('wagtailadmin_home')}"),
        ("PAGES list", f"{reverse('wagtailadmin_explore_root')}"),
        ("SEARCH all", f"{reverse('wagtailadmin_pages:search')}"),
        ("AGING PAGES list", f"{reverse('wagtailadmin_reports:aging_pages')}"),
        ("COLLECTIONS list", f"{reverse('wagtailadmin_collections:index')}"),
        ("DOCUMENTS list", f"{reverse('wagtaildocs:index')}"),
        ("GROUPS list", f"{reverse('wagtailusers_groups:index')}"),
        ("IMAGES list", f"{reverse('wagtailimages:index')}"),
        ("LOCKED PAGES list", f"{reverse('wagtailadmin_reports:locked_pages')}"),
        ("REDIRECTS list", f"{reverse('wagtailredirects:index')}"),
        ("SITES list", f"{reverse('wagtailsites:index')}"),
        ("SITE HISTORY list", f"{reverse('wagtailadmin_reports:site_history')}"),
        ("SNIPPETS list", f"{reverse('wagtailsnippets:index')}"),
        ("USERS list", f"{reverse('wagtailusers_users:index')}"),
        ("WORKFLOWS list", f"{reverse('wagtailadmin_workflows:index')}"),
        ("WORKFLOWS TASKS list", f"{reverse('wagtailadmin_workflows:task_index')}"),
    ]


def session_login(request):
    session = requests.Session()
    session.get(f"{get_host(request)}{reverse('wagtailadmin_login')}")
    login_data = {
        "username": "superuser",
        "password": "superuser",
        "csrfmiddlewaretoken": session.cookies["csrftoken"],
    }
    session.post(f"{get_host(request)}{reverse('wagtailadmin_login')}", data=login_data)

    return session


def get_model_admin_types():
    if not hasattr(settings, "WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES"):
        return [
            "wagtail_devtools_test.TestModelAdminOne",
            "wagtail_devtools_test.TestModelAdminTwo",
            "wagtail_devtools_test.TestModelAdminThree",
        ]
    return settings.WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES


def results_item(request, item, fe_response, be_response, **kwargs):
    if kwargs.get("defaults"):
        defaults = kwargs.get("defaults")
    else:
        defaults = {
            "title": None,
            "editor_url": None,
            "editor_status_code": None,
            "editor_status_text": None,
            "fe_url": None,
            "fe_status_code": None,
            "fe_status_text": None,
            "app_name": None,
            "class_name": None,
        }

        if item:
            if hasattr(item, "title"):
                defaults["title"] = item.title
            elif hasattr(item, "name"):
                defaults["title"] = item.name
            elif hasattr(item, "hostname"):
                defaults["title"] = item.hostname
            elif hasattr(item, "username"):
                defaults["title"] = item.username
            else:
                defaults["title"] = item.__str__()

            # Not all items have a front-end URL
            if hasattr(item, "get_url"):
                defaults["fe_url"] = item.get_url()
                defaults["fe_status_code"] = fe_response.status_code
                defaults["fe_status_text"] = fe_response.reason

            defaults["fe_url"] = item.get_url() if hasattr(item, "get_url") else None
            defaults["editor_url"] = f"{get_admin_edit_url(request, item)}"
            defaults["app_name"] = item._meta.app_label
            defaults["class_name"] = item.__class__.__name__

            defaults["editor_status_code"] = be_response.status_code
            defaults["editor_status_text"] = be_response.reason

    return defaults
