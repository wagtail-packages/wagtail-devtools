from io import StringIO

from django.core.management import call_command
from django.test import RequestFactory, TestCase

from wagtail_devtools.test.models import (
    FrontendPage200,
    FrontendPage302,
    FrontendPage404,
    FrontendPage500,
    TestModelAdminOne,
    TestModelAdminThree,
    TestModelAdminTwo,
    TestSnippetOne,
    TestSnippetThree,
    TestSnippetTwo,
)


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_snippet_one_title(self):
        item = TestSnippetOne.objects.first()
        self.assertEqual(item.__str__(), "Test Snippet 1")

    def test_snippet_two_title(self):
        item = TestSnippetTwo.objects.first()
        self.assertEqual(item.__str__(), "Test Snippet 1")

    def test_snippet_three_title(self):
        item = TestSnippetThree.objects.first()
        self.assertEqual(item.__str__(), "Test Snippet 1")

    def test_model_admin_one_title(self):
        item = TestModelAdminOne.objects.first()
        self.assertEqual(item.__str__(), "Test Model Admin One 1")

    def test_model_admin_two_title(self):
        item = TestModelAdminTwo.objects.first()
        self.assertEqual(item.__str__(), "Test Model Admin Two 1")

    def test_model_admin_three_title(self):
        item = TestModelAdminThree.objects.first()
        self.assertEqual(item.__str__(), "Test Model Admin Three 1")

    def test_frontend_page_200_title(self):
        item = FrontendPage200.objects.first()
        self.assertEqual(item.__str__(), "Frontend Page 200")

    def test_frontend_page_404_title(self):
        item = FrontendPage404.objects.first()
        self.assertEqual(item.__str__(), "Frontend Page 404")

    def test_frontend_page_500_title(self):
        item = FrontendPage500.objects.first()
        self.assertEqual(item.__str__(), "Frontend Page 500")

    def test_frontend_page_302_title(self):
        item = FrontendPage302.objects.first()
        self.assertEqual(item.__str__(), "Frontend Page 302")
