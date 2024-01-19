from io import StringIO
from pathlib import Path

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Builds a fixture file for the API tests.

    This isn't required but is a nice to have if you need to load the data outside of the
    build_fixtures command."""

    def handle(self, *args, **options):
        cwd = Path.cwd()
        fixtures_dir = cwd / "wagtail_devtools" / "test" / "fixtures"
        fixture_filename = "api_fixtures.json"
        fixture_file = fixtures_dir / fixture_filename
        self.delete_fixture_file(fixture_file)
        self.load_fixtures_from_script()
        self.create_fixture_file(fixture_file)

    def delete_fixture_file(self, fixture_file):
        if fixture_file.exists():
            fixture_file.unlink()

    def load_fixtures_from_script(self):
        with StringIO() as _:
            # Don't want to see the output of the command
            call_command("build_fixtures", "--clear", stdout=_)

    def create_fixture_file(self, fixture_file):
        with StringIO() as _:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                exclude=["contenttypes", "wagtailsearch"],  # excludes,
                output=fixture_file,
                indent=2,
                stdout=_,
            )
