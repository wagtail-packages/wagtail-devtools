from django.test import SimpleTestCase

from wagtail_devtools.api.urls import urlpatterns


class TestApiUrls(SimpleTestCase):
    def test_api_index(self):
        path = urlpatterns[0]
        self.assertEqual(path.name, "api_index")
        self.assertEqual(path.pattern._route, "")
        self.assertEqual(path.callback.__name__, "api_view")

    def test_edit_types(self):
        path = urlpatterns[1]
        self.assertEqual(path.name, "edit-types")
        self.assertEqual(path.pattern._route, "edit-types/")
        self.assertEqual(path.callback.__name__, "wagtail_core_edit_pages")

    def test_form_types(self):
        path = urlpatterns[2]
        self.assertEqual(path.name, "form-types")
        self.assertEqual(path.pattern._route, "form-types/")
        self.assertEqual(path.callback.__name__, "form_types")

    def test_listing_types(self):
        path = urlpatterns[3]
        self.assertEqual(path.name, "listing-types")
        self.assertEqual(path.pattern._route, "listing-types/")
        self.assertEqual(path.callback.__name__, "wagtail_core_listing_pages")

    def test_modeladmin_types(self):
        path = urlpatterns[4]
        self.assertEqual(path.name, "modeladmin-types")
        self.assertEqual(path.pattern._route, "modeladmin-types/")
        self.assertEqual(path.callback.__name__, "model_admin_types")

    def test_page_types(self):
        path = urlpatterns[5]
        self.assertEqual(path.name, "page-types")
        self.assertEqual(path.pattern._route, "page-types/")
        self.assertEqual(path.callback.__name__, "page_model_types")

    def test_settings_types(self):
        path = urlpatterns[6]
        self.assertEqual(path.name, "settings-types")
        self.assertEqual(path.pattern._route, "settings-types/")
        self.assertEqual(path.callback.__name__, "settings_types")

    def test_snippet_types(self):
        path = urlpatterns[7]
        self.assertEqual(path.name, "snippet-types")
        self.assertEqual(path.pattern._route, "snippet-types/")
        self.assertEqual(path.callback.__name__, "snippet_types")
