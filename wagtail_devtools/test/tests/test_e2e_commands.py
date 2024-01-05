import logging

from io import StringIO
from sys import stderr

from django.core.management import call_command
from django.test import LiveServerTestCase, TestCase, override_settings


class TestE2ELoadFixtures(TestCase):
    def test_build_fixtures(self):
        args = []
        opts = {}

        with StringIO() as out:
            call_command("build_fixtures", *args, **opts, stdout=out, stderr=stderr)
            output = out.getvalue().strip()
            print(output)  # Just for debugging

        expected = [
            "Creating superuser.",
            "Updating home page.",
            "Creating standard pages.",
            "Creating snippets.",
            "Creating model admins.",
            "Creating settings.",
            "Creating collections.",
            "Creating redirects.",
            "Creating promoted searches.",
            "Importing media files.",
        ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)


@override_settings(DEBUG=True)
class TestE2EAdminContentTypes(TestCase):
    def setUp(self):
        with StringIO() as out:
            call_command("build_fixtures", stdout=out, stderr=stderr)

    def test_console_out(self):
        args = []
        opts = {
            "cid": 3,
        }

        with StringIO() as out:
            call_command(
                "cmd_test_content_types", *args, **opts, stdout=out, stderr=out
            )
            output = out.getvalue().strip()
            print(output)  # Just for debugging

            expected = [  # Not testing for existence of the edit links or cid value as can't be guaranteed
                "Using this command:",
                "Enter a C-Type ID from the list below",
                "to view a report of all the admin edit pages of that type.",
                "Index of Page Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "HomePage                    wagtail_devtools_test",
                "StandardPageOne             wagtail_devtools_test",
                "StandardPageTwo             wagtail_devtools_test",
                "StandardPageThree           wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of Snippet Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "TestSnippetOne              wagtail_devtools_test",
                "TestSnippetThree            wagtail_devtools_test",
                "TestSnippetTwo              wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of ModelAdmin Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "TestModelAdminOne           wagtail_devtools_test",
                "TestModelAdminTwo           wagtail_devtools_test",
                "TestModelAdminThree         wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
                "Index of Settings Types",
                "---------------------------------------------------------------------------------",
                "Model                       App                         C-Type ID",
                "---------------------------------------------------------------------------------",
                "GenericSettingOne           wagtail_devtools_test",
                "GenericSettingTwo           wagtail_devtools_test",
                "GenericSettingThree         wagtail_devtools_test",
                "SiteSettingOne              wagtail_devtools_test",
                "SiteSettingTwo              wagtail_devtools_test",
                "SiteSettingThree            wagtail_devtools_test",
                "---------------------------------------------------------------------------------",
            ]

        for line in expected:
            if line not in output:
                # Just for debugging
                print(f"Missing this line: {line}")
            self.assertIn(line, output)


@override_settings(DEBUG=True)
class TestE2EAdminResponses(LiveServerTestCase):
    def setUp(self):
        with StringIO() as out:
            call_command("build_fixtures", stdout=out, stderr=stderr)

    def test_console_out(self):
        args = [
            "superuser",
            "superuser",
        ]
        opts = {
            "host": self.live_server_url,
        }
        logging.disable(logging.CRITICAL)

        with StringIO() as out:
            call_command(
                "cmd_test_admin_responses", *args, **opts, stdout=out, stderr=out
            )
            output = out.getvalue().strip()
            print(output)  # Just for debugging

        # Not testing edit page messages as the id's aren't guaranteed
        # The important test is the response error and draft page messages are found
        # For good measure we'll include a test for the first and almost last lines of the output
        lines_expected = [
            "Checking the admin and frontend responses of 4 page types ...",
            "==============================================================",
            " 1. HomePage",
            " 2. StandardPageOne",
            " 3. StandardPageThree",
            " 4. StandardPageTwo",
            "Home Page ( HomePage ) ↓",
            f"{self.live_server_url}/ ← 200",
            "Standard Page One ( StandardPageOne ) ↓",
            f"{self.live_server_url}/standard-page-one/ ← 200",
            "Standard Page Two ( StandardPageTwo ) ↓",
            f"{self.live_server_url}/standard-page-two/ ← 404 probably a draft page",
            "Standard Page Three ( StandardPageThree ) ↓",
            f"{self.live_server_url}/standard-page-three/ ← 500",
            "DASHBOARD page ...",
            "===================",
            f"{self.live_server_url}/admin/ ← 200",
            "PAGES list page ...",
            "====================",
            f"{self.live_server_url}/admin/pages/ ← 200",
            "SEARCH all page ...",
            "====================",
            f"{self.live_server_url}/admin/pages/search/ ← 200",
            "AGING PAGES list page ...",
            "==========================",
            f"{self.live_server_url}/admin/reports/aging-pages/ ← 200",
            "COLLECTIONS list page ...",
            "==========================",
            f"{self.live_server_url}/admin/collections/ ← 200",
            "COLLECTIONS EDIT page ...",
            "WORKFLOWS TASK edit page ...",
            "==========================",
            "Task ↓",
        ]

        line_count = 0

        for line in lines_expected:
            line_count += 1

            if line not in output:
                print(f"Missing this line: {line}")  # Just for debugging
            self.assertIn(line, output)

        print(f"Line count: {line_count}")  # Just for debugging

        self.assertTrue(
            line_count >= 30,
        )
