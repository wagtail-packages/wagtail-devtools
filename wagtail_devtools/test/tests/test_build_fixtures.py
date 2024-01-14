import os
import shutil

from io import StringIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from wagtail.contrib.redirects.models import Redirect
from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.models import Page, Site
from wagtail.models.collections import Collection
from wagtail.snippets.models import get_snippet_models


class TestBuildFixtures(TestCase):
    """Test the build_fixtures command.

    There is a custom test runner in test/runner (WagtailDevToolsTestRunner) that runs after the test suite has run
    that rebuilds the test-media folder."""

    def test_fixtures(self):
        with StringIO() as out:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=out)
            self.assertIn("Fixtures created.", out.getvalue())

    def test_fixtures_creates_pages(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        pages = Page.objects.all().exclude(title="Root")
        self.assertEqual(pages.count(), 14)

    def test_fixtures_creates_snippets(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        snippet_models = get_snippet_models()
        for model in snippet_models:
            self.assertEqual(model.objects.count(), 4)

    def test_fixtures_creates_media(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        image_model = get_image_model()
        self.assertEqual(image_model.objects.count(), 4)

    def test_fixtures_creates_documents(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        document_model = get_document_model()
        self.assertEqual(document_model.objects.count(), 4)

    def test_fixtures_creates_user(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        user_model = get_user_model()
        self.assertEqual(user_model.objects.count(), 1)

    def test_fixtures_creates_collections(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        collection_model = Collection
        self.assertEqual(collection_model.objects.count(), 5)

    def test_fixtures_creates_settings(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        self.assertEqual(len(settings_registry), 6)

    def test_fixtures_creates_sites(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        site_model = Site
        self.assertEqual(site_model.objects.count(), 2)

        first_site = site_model.objects.get(is_default_site=True)
        self.assertEqual(first_site.hostname, "localhost")
        self.assertEqual(first_site.port, 8000)
        self.assertEqual(first_site.site_name, "Default Site")
        self.assertEqual(first_site.root_page.title, "Home Page")

        second_site = site_model.objects.get(is_default_site=False)
        self.assertEqual(second_site.hostname, "127.0.0.1")
        self.assertEqual(second_site.port, 8000)
        self.assertEqual(second_site.site_name, "Second Site")
        self.assertEqual(second_site.root_page.title, "Second Site Home Page")

    def test_fixtures_creates_redirects(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        redirect_model = Redirect
        self.assertEqual(redirect_model.objects.count(), 4)

    def test_fixtures_creates_search_promotions(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)
        search_promotion_model = SearchPromotion
        self.assertEqual(search_promotion_model.objects.count(), 4)

    def test_fixtures_create_test_media(self):
        media_path = Path(os.getcwd()) / "test-media"
        if media_path.exists():
            shutil.rmtree(media_path)
        self.assertFalse(media_path.exists())

        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

        self.assertTrue(media_path.exists())
