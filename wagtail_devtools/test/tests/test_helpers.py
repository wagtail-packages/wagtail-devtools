from django.conf import settings
from django.test import RequestFactory, TestCase, override_settings
from wagtail.models import Page

from wagtail_devtools.api.helpers import get_admin_edit_url, get_host, init_ret
from wagtail_devtools.test.management.commands.build_fixtures import (
    create_standard_pages,
)


class TestApiHelpers(TestCase):
    """Test the API helpers."""

    @override_settings(WAGTAIL_DEVTOOLS_BASE_URL=None, WAGTAILADMIN_BASE_URL=None)
    def test_get_host(self):
        del settings.WAGTAIL_DEVTOOLS_BASE_URL
        del settings.WAGTAILADMIN_BASE_URL
        host = get_host()
        self.assertIsNone(host)

    @override_settings(WAGTAIL_DEVTOOLS_BASE_URL=None, WAGTAILADMIN_BASE_URL=None)
    def test_get_host_with_request(self):
        del settings.WAGTAIL_DEVTOOLS_BASE_URL
        host = get_host(request=RequestFactory().get("/"))
        self.assertEqual(host, "http://localhost:8000")

    @override_settings(WAGTAIL_DEVTOOLS_BASE_URL="http://example.com")
    def test_get_host_with_unhelpful_request(self):
        host = get_host(request=RequestFactory().get("/"))
        self.assertEqual(host, "http://example.com")

    @override_settings(WAGTAIL_DEVTOOLS_BASE_URL="https://example.com")
    def test_get_host_with_request_parses_url(self):
        host = get_host(request=RequestFactory().get("/"))
        self.assertEqual(host, "https://example.com")

    @override_settings(
        WAGTAIL_DEVTOOLS_BASE_URL="https://example.com",
        WAGTAILADMIN_BASE_URL="http://localhost:8000",
    )
    def test_get_host_with_request_and_setting(self):
        # WAGTAIL_DEVTOOLS_BASE_URL takes precedence
        request = RequestFactory().get("/")
        host = get_host(request=request)
        self.assertEqual(host, "https://example.com")
        del settings.WAGTAIL_DEVTOOLS_BASE_URL
        host = get_host(request=request)
        self.assertEqual(host, "http://localhost:8000")

    def test_init_ret(self):
        ret = init_ret("test")
        self.assertEqual(ret, {"meta": {"title": "test"}, "results": []})

    def test_get_admin_edit_url(self):
        create_standard_pages()
        page = Page.objects.get(title="Standard Page One")
        page_id = page.id
        url = get_admin_edit_url("http://localhost:8000", page)
        self.assertEqual(url, f"http://localhost:8000/admin/pages/{page_id}/edit/")
