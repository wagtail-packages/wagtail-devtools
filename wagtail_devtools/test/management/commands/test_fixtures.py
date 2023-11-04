import subprocess

from django.core.management import BaseCommand, call_command
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.images.models import Rendition


class Command(BaseCommand):
    help = "Create or load fixtures for Wagtail >= 4.1, < 5.2"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l", "--load", action="store_true", help="Load test fixtures."
        )
        parser.add_argument(
            "-d", "--dump", action="store_true", help="Dump test fixtures."
        )

    def handle(self, *args, **options):
        self.load_fixtures() if options["load"] else None
        self.dump_fixtures() if options["dump"] else None

    def dump_fixtures(self):
        Rendition.objects.all().delete()

        include = [
            "wagtail_devtools_test.HomePage",
            "wagtail_devtools_test.TestSnippet",
            "wagtail_devtools_test.GenericSetting",
            "wagtail_devtools_test.SiteSetting",
            "wagtailimages.image",
            "auth.User",
        ]

        if not WAGTAIL_VERSION >= (5, 2):
            include.append("wagtail_devtools_test.TestModelAdmin")
            file_name = "wagtail_devtools/test/fixtures/data/wagtail_less_52_data.json"
            out = "Dumping data for Wagtail>=4.1,<5.2"
        else:
            file_name = "wagtail_devtools/test/fixtures/data/wagtail_equal_52_data.json"
            out = "Dumping data for Wagtail>=5.2"

        self.stdout.write(out)

        with open(file_name, "w") as f:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                "--indent",
                "4",
                include,
                stdout=f,
            )

        self.stdout.write(self.style.SUCCESS("Successfully dumped data"))

    def load_fixtures(self):
        if not WAGTAIL_VERSION >= (5, 2):
            file_name = "wagtail_devtools/test/fixtures/data/wagtail_less_52_data.json"
            out = "Loading data for Wagtail>=5.2"
        else:
            file_name = "wagtail_devtools/test/fixtures/data/wagtail_equal_52_data.json"
            out = "Loading data for Wagtail>=4.1,<5.2"

        self.stdout.write(out)
        call_command("loaddata", file_name)

        self.stdout.write("Copying fixture media files")

        subprocess.run(
            ["cp", "-r", "wagtail_devtools/test/fixtures/media/", "test-media"]
        )
