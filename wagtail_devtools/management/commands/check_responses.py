from django.core.management.base import BaseCommand

from wagtail_devtools.auth import LoginHandler


class Command(BaseCommand):
    help = "Check responses of API views."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username to use for login.",
            default="superuser",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password to use for login.",
            default="superuser",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Check all API views (slow).",
        )
        parser.add_argument(
            "--url",
            type=str,
            help="The url to test (default=http://localhost:8000)",
            default="http://localhost:8000",
        )

    def handle(self, *args, **options):
        login_handler = LoginHandler(options["url"])
        login_handler.login(options["username"], options["password"])
        if not options["all"]:
            response = login_handler.get_response(
                f"{options['url']}/wagtail-devtools-api/"
            )
        else:
            response = login_handler.get_response(
                f"{options['url']}/wagtail-devtools-api/?all=true"
            )

        if not response.status_code == 200:
            raise Exception("API view not found")

        resp_200 = []
        resp_404 = []
        resp_500 = []
        resp_302 = []

        for item in response.json():
            response = login_handler.get_response(item["url"])
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"{item['name']} - {item['url']}"))
                resp_200.append(item["url"])
            elif response.status_code == 404:
                self.stdout.write(self.style.WARNING(f"{item['name']} - {item['url']}"))
                resp_404.append(item["url"])
            elif response.status_code == 500:
                self.stdout.write(self.style.ERROR(f"{item['name']} - {item['url']}"))
                resp_500.append(item["url"])
            elif response.status_code == 302:
                self.stdout.write(self.style.WARNING(f"{item['name']} - {item['url']}"))
                resp_302.append(item["url"])

        # print("200 responses:")
        # print(resp_200)
        # print("404 responses:")
        # print(resp_404)
        # print("500 responses:")
        # print(resp_500)
        # print("302 responses:")
        # print(resp_302)
        login_handler.logout()
        print("Done")
