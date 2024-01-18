from django.conf import settings
from django.test import RequestFactory, TestCase, override_settings
from wagtail.models import Page

from wagtail_devtools.api.helpers import (
    get_admin_edit_url,
    get_creatable_page_models,
    get_form_page_models,
    get_host,
    get_model_admin_models,
    init_ret,
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

    # def test_results_item(self):
    #     ret = results_item(None, None)
    #     self.assertEqual(
    #         ret,
    #         {
    #             # "app_name": None,
    #             # "class_name": None,
    #             "editor_url": None,
    #             "fe_url": None,
    #             "title": None,
    #         },
    #     )

    # @patch("wagtail_devtools.api.helpers.get_admin_edit_url")
    # def test_results_with_item(self, mock_get_admin_edit_url):
    #     mock_get_admin_edit_url.return_value = "/test/"

    #     # fe_response = self.client.get("/")
    #     # fe_response.status_code = 200
    #     # fe_response.reason = "OK"
    #     # be_response = self.client.get("/admin/")
    #     # be_response.status_code = 200
    #     # be_response.reason = "OK"

    #     class TestItem(models.Model):
    #         title = models.CharField(max_length=255)

    #         def get_url(self):
    #             return "/test/"

    #         class Meta:
    #             app_label = "test_item"

    #     item = TestItem(title="Test Item")
    #     ret = results_item(RequestFactory().get("/"), item)
    #     self.assertEqual(
    #         ret,
    #         {
    #             "title": "Test Item",
    #             "editor_url": "/test/",
    #             # "editor_status_code": 200,
    #             # "editor_status_text": "OK",
    #             "fe_url": "/test/",
    #             # "fe_status_code": 200,
    #             # "fe_status_text": "OK",
    #             # "app_name": "test_item",
    #             # "class_name": "TestItem",
    #         },
    #     )

    def test_get_admin_edit_url(self):
        create_standard_pages()
        page = Page.objects.get(title="Standard Page One")
        page_id = page.id
        url = get_admin_edit_url("http://localhost:8000", page)
        self.assertEqual(url, f"http://localhost:8000/admin/pages/{page_id}/edit/")

    def test_get_creatable_page_models(self):
        self.assertIsInstance(get_creatable_page_models(), list)

    def test_get_form_page_models(self):
        models = get_form_page_models()
        self.assertIsInstance(models, list)
        self.assertEqual(len(models), 2)
        for model in models:
            self.assertTrue(
                "AbstractEmailForm" in [cls.__name__ for cls in model.__mro__]
            )

    def test_get_model_admin_models(self):
        model_admin_types = [
            "wagtail_devtools_test.TestModelAdminOne",
        ]
        models = get_model_admin_models(model_admin_types)
        self.assertIsInstance(models, list)
        self.assertEqual(len(models), 1)

    # def test_generate_title(self):
    #     page = "wagtailadmin_collections:index"
    #     title = generate_title(page)
    #     self.assertEqual(title, "Admin Collections Index")


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
