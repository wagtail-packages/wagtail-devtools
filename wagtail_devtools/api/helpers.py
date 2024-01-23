from urllib.parse import urlparse

from django.conf import settings
from django.utils.encoding import force_str
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Site


def get_admin_edit_url(host, obj):
    return f"{get_host(host)}{AdminURLFinder().get_edit_url(obj)}"


def get_host(request=None):
    # Modified from wagtail.api.v2.utils.get_base_url
    if hasattr(settings, "WAGTAIL_DEVTOOLS_BASE_URL"):
        base_url = settings.WAGTAIL_DEVTOOLS_BASE_URL
    else:
        base_url = getattr(settings, "WAGTAILADMIN_BASE_URL", None)

    if base_url is None and request:
        site = Site.find_for_request(request)
        if site:
            base_url = site.root_url

    if base_url:
        # We only want the scheme and netloc
        base_url_parsed = urlparse(force_str(base_url))

        return base_url_parsed.scheme + "://" + base_url_parsed.netloc


def init_ret(title):
    return {"meta": {"title": title}, "results": []}
