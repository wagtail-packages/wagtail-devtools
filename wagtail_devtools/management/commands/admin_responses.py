from django.core.management.base import BaseCommand

from wagtail_devtools.auth import LoginHandler
from wagtail_devtools.reporting import Report


class Command(BaseCommand):
    help = "Access the devtools api and check admin and frontend urls."

    def add_arguments(self, parser):
        """Add arguments."""
        parser.add_argument(
            "--host",
            action="store",
            dest="host",
            default="http://localhost:8000",
            help="Host to check",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all",
            default=False,
            help="Check all pages",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Verbose output",
        )

    def handle(self, *args, **options):
        # Listing page types
        session = LoginHandler(options["host"])
        session.login("superuser", "superuser")

        if not session.is_authenticated():
            self.stdout.write(self.style.ERROR("Not authenticated"))
            return

        index_endpoint = options["host"] + "/wagtail-devtools-api/"

        response = session.get_response(index_endpoint)
        endpoints = response.json()["api-views"]

        results_500 = []
        results_404 = []
        results_302 = []
        results_200 = []

        for endpoint in endpoints:
            if options["all"]:
                endpoint = endpoint + "?all=true"
            response = session.get_response(endpoint)
            results = response.json()["results"]
            title = response.json()["meta"]["title"]
            report = Report(title, results, session)
            results_500.extend(report.get_errors_500())
            results_404.extend(report.get_errors_404())
            results_302.extend(report.get_errors_302())
            results_200.extend(report.get_success_200())

        self.stdout.write(self.style.ERROR(f"500 errors: {len(results_500)}"))
        self.stdout.write("=====================================")
        if len(results_500) > 0:
            for result in results_500:
                self.stdout.write(self.style.HTTP_INFO(result.title))
                self.stdout.write(
                    self.style.HTTP_INFO(result.url)
                ) if result.url else None
                if result.editor_url:
                    self.stdout.write(self.style.HTTP_INFO(result.editor_url))
        self.stdout.write("\n")

        self.stdout.write(self.style.WARNING(f"404 errors: {len(results_404)}"))
        self.stdout.write("=====================================")
        if len(results_404) > 0:
            for result in results_404:
                self.stdout.write(self.style.HTTP_INFO(result.title))
                self.stdout.write(
                    self.style.HTTP_INFO(result.url)
                ) if result.url else None
                if result.editor_url:
                    self.stdout.write(self.style.HTTP_INFO(result.editor_url))
        self.stdout.write("\n")

        self.stdout.write(self.style.WARNING(f"302 errors: {len(results_302)}"))
        self.stdout.write("=====================================")
        if len(results_302) > 0:
            for result in results_302:
                self.stdout.write(self.style.HTTP_INFO(result.title))
                self.stdout.write(
                    self.style.HTTP_INFO(result.url)
                ) if result.url else None
                if result.editor_url:
                    self.stdout.write(self.style.HTTP_INFO(result.editor_url))
        self.stdout.write("\n")

        self.stdout.write(self.style.SUCCESS(f"200 success: {len(results_200)}"))
        self.stdout.write("=====================================")
        if options["verbose"]:
            if len(results_200) > 0:
                for result in results_200:
                    self.stdout.write(self.style.HTTP_INFO(result.title))
                    self.stdout.write(
                        self.style.HTTP_INFO(result.url)
                    ) if result.url else None
                    if result.editor_url:
                        self.stdout.write(self.style.HTTP_INFO(result.editor_url))

        self.stdout.write(self.style.SUCCESS(f"Total: {len(endpoints)}"))
        self.stdout.write("=====================================")
