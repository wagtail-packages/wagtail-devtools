from django.test import TestCase


# from wagtail_devtools.test.management.commands.build_fixtures import (
#     create_form_pages,
# )

# from wagtail_devtools.api.views import (
#     api_view,
#     form_types,
#     model_admin_types,
#     page_model_types,
#     settings_types,
#     snippet_types,
#     wagtail_core_edit_pages,
#     wagtail_core_listing_pages,
# )


class TestApiViews(TestCase):
    # fixtures = ["wagtail_devtools/test/fixtures/fixtures.json"]

    def test_api_view(self):
        # liver_server_url = self.live_server_url
        response = self.client.get("/wagtail-devtools-api/")
        self.assertEqual(response.status_code, 200)

        api_views = response.json()["api-views"]
        self.assertEqual(len(api_views), 7)
        self.assertEqual(
            api_views[0],
            "http://localhost:8000/wagtail-devtools-api/edit-types/",
        )
        self.assertEqual(
            api_views[1],
            "http://localhost:8000/wagtail-devtools-api/form-types/",
        )
        self.assertEqual(
            api_views[2],
            "http://localhost:8000/wagtail-devtools-api/listing-types/",
        )
        self.assertEqual(
            api_views[3],
            "http://localhost:8000/wagtail-devtools-api/modeladmin-types/",
        )
        self.assertEqual(
            api_views[4],
            "http://localhost:8000/wagtail-devtools-api/page-types/",
        )
        self.assertEqual(
            api_views[5],
            "http://localhost:8000/wagtail-devtools-api/settings-types/",
        )
        self.assertEqual(
            api_views[6],
            "http://localhost:8000/wagtail-devtools-api/snippet-types/",
        )
