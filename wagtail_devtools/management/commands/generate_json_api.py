import json

from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.admin.admin_url_finder import AdminURLFinder

from wagtail_devtools.api.helpers import get_creatable_page_models, init_ret


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--all-pages",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--reverse",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if not hasattr(settings, "WAGTAIL_DEVTOOLS_CONFIG"):
            print("WAGTAIL_DEVTOOLS_CONFIG is not defined in settings.py")
            return
        json_dir = settings.WAGTAIL_DEVTOOLS_CONFIG.get("json_dir")
        result = create_page_types_json(options["all_pages"], options["reverse"])
        with open(f"{json_dir}/page_types.json", "w") as outfile:
            json.dump(result, outfile, indent=4)


def create_page_types_json(all_pages: bool = False, reverse: bool = False):
    ret = init_ret("Page model types")
    ret["results"] = []

    for page_model in get_creatable_page_models():
        # page ordered by first_published_at descending so we get the latest pages/page
        order = "first_published_at" if reverse else "-first_published_at"

        pages = (
            page_model.objects.live().order_by(order)[:1]
            if not all_pages
            else page_model.objects.live().order_by(order)
        )

        for item in pages:
            url_parts = item.get_url_parts()
            path = url_parts[1]

            admin_edit_url = f"{path}{AdminURLFinder().get_edit_url(item)}"
            page_url = f"{path}{url_parts[2]}"

            ret["results"].append(
                {
                    "title": item.title,
                    "editor_url": admin_edit_url,
                    "url": page_url,
                    "app_name": page_model._meta.app_label,
                    "class_name": page_model.__name__,
                }
            )

    return ret
