from unittest.mock import patch

from django.conf import settings
from django.db import models
from django.test import RequestFactory, TestCase, override_settings
from wagtail.models import Page

from wagtail_devtools.api.helpers import (
    get_admin_edit_url,
    get_host,
    init_ret,
    results_item,
)
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

    def test_results_item(self):
        ret = results_item(None, None, None, None)
        self.assertEqual(
            ret,
            {
                "app_name": None,
                "class_name": None,
                "editor_status_code": None,
                "editor_status_text": None,
                "editor_url": None,
                "fe_status_code": None,
                "fe_status_text": None,
                "fe_url": None,
                "title": None,
            },
        )

    def test_results_with_defaults(self):
        the_nones = [None, None, None, None]
        ret = results_item(
            *the_nones,
            defaults={
                "title": "Test Title",
                "editor_url": None,
                "editor_status_code": None,
                "editor_status_text": None,
                "fe_url": None,
                "fe_status_code": None,
                "fe_status_text": None,
                "app_name": "app",
                "class_name": "class_name",
            },
        )
        self.assertEqual(
            ret,
            {
                "title": "Test Title",
                "editor_url": None,
                "editor_status_code": None,
                "editor_status_text": None,
                "fe_url": None,
                "fe_status_code": None,
                "fe_status_text": None,
                "app_name": "app",
                "class_name": "class_name",
            },
        )

    @patch("wagtail_devtools.api.helpers.get_admin_edit_url")
    def test_results_with_item(self, mock_get_admin_edit_url):
        mock_get_admin_edit_url.return_value = "/test/"

        fe_response = self.client.get("/")
        fe_response.status_code = 200
        fe_response.reason = "OK"
        be_response = self.client.get("/admin/")
        be_response.status_code = 200
        be_response.reason = "OK"

        class TestItem(models.Model):
            title = models.CharField(max_length=255)

            def get_url(self):
                return "/test/"

            class Meta:
                app_label = "test_item"

        item = TestItem(title="Test Item")
        ret = results_item(RequestFactory().get("/"), item, fe_response, be_response)
        self.assertEqual(
            ret,
            {
                "title": "Test Item",
                "editor_url": "/test/",
                "editor_status_code": 200,
                "editor_status_text": "OK",
                "fe_url": "/test/",
                "fe_status_code": 200,
                "fe_status_text": "OK",
                "app_name": "test_item",
                "class_name": "TestItem",
            },
        )

    def test_get_admin_edit_url(self):
        create_standard_pages()
        page = Page.objects.get(title="Standard Page One")
        page_id = page.id
        url = get_admin_edit_url("http://localhost:8000", page)
        self.assertEqual(url, f"http://localhost:8000/admin/pages/{page_id}/edit/")


# TODO: Test session_login helper
# class TestSessionLogin(LiveServerTestCase):
#     """Test the session_login helper."""

#     host = "localhost"
#     port = 8000

#     def test_session_login(self):
#         request = RequestFactory().get("/")
#         session = session_login(request)
#         self.assertIsNotNone(session)
#         self.assertIsNotNone(session.cookies["sessionid"])
