from django.test import TestCase


class TestApiViews(TestCase):
    def test_api_view(self):
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

    # TODO: Add further view tests. The views need to be altered to achieve this.
