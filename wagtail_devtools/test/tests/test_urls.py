from django.test import SimpleTestCase


# from wagtail_devtools.api.urls import urlpatterns


class TestApiUrls(SimpleTestCase):
    pass
    # def test_api_index(self):
    #     path = urlpatterns[0]
    #     self.assertEqual(path.name, "api_index")
    #     self.assertEqual(path.pattern._route, "")
    #     self.assertEqual(path.callback.__name__, "api_view")

    # def test_listing_types(self):
    #     path = urlpatterns[1]
    #     self.assertEqual(path.name, "listing-types")
    #     self.assertEqual(path.pattern._route, "listing-types/")
    #     self.assertEqual(path.callback.__name__, "wagtail_core_listing_pages")

    # def test_wagtail_core_apps(self):
    #     path = urlpatterns[2]
    #     self.assertEqual(path.name, "wagtail-core-apps")
    #     self.assertEqual(path.pattern._route, "wagtail-core-apps/")
    #     self.assertEqual(path.callback.__name__, "wagtail_core_apps")
