from io import BytesIO
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.management import BaseCommand
from django.db import IntegrityError
from wagtail.contrib.redirects.models import Redirect
from wagtail.documents.models import Document as WagtailDocument
from wagtail.images.models import Image as WagtailImage
from wagtail.models.collections import Collection

from wagtail_devtools.test.models import (
    GenericSetting,
    HomePage,
    SiteSetting,
    TestModelAdmin,
    TestSnippet,
)


class Command(BaseCommand):
    help = "Create or load fixtures for testing."

    def handle(self, *args, **options):
        self.create_superuser()
        self.create_snippets()
        self.create_modeladmins()
        self.create_settings()
        self.create_collections()
        self.create_redirects()
        self.import_media()

    def create_superuser(self):
        self.stdout.write("Creating superuser.")

        try:
            User.objects.create_superuser(
                username="superuser",
                email="superuser@admin.com",
                password="superuser",
            )
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("Superuser already exists. Skipping creation.")
            )

    def update_home_page(self):
        self.stdout.write("Updating home page.")

        home_page = HomePage.objects.first()
        home_page.title = "Home Page"

    def create_snippets(self):
        self.stdout.write("Creating snippets.")

        for x in range(1, 5):
            TestSnippet.objects.create(title=f"Test Snippet {x}")

    def create_modeladmins(self):
        self.stdout.write("Creating model admins.")

        for x in range(1, 5):
            TestModelAdmin.objects.create(title=f"Test Model Admin {x}")

    def create_settings(self):
        self.stdout.write("Creating settings.")

        site_setting = SiteSetting.objects.first()
        site_setting.name = "Site Setting"
        site_setting.save()

        generic_setting = GenericSetting.objects.first()
        generic_setting.name = "Generic Setting"
        generic_setting.save()

    def create_collections(self):
        self.stdout.write("Creating collections.")
        root_collection = Collection.objects.get(depth=1)

        for x in range(1, 5):
            root_collection.add_child(name=f"Test Collection {x}")

    def create_redirects(self):
        self.stdout.write("Creating redirects.")

        for x in range(1, 5):
            redirect_page = HomePage.objects.first()
            Redirect.objects.create(
                old_path=f"/test-redirect-{x}",
                redirect_page=redirect_page,
            )

    def import_media(self):
        self.stdout.write("Importing media files.")

        original_images = ["one.jpg", "two.jpg", "three.jpg", "four.jpg"]

        for image in original_images:
            title = f"Image {Path(image).stem.capitalize()}"
            name = Path(image)
            directory = Path.cwd() / Path("wagtail_devtools/test/fixtures/media/images")
            image_path = directory / Path(image)

            with open(image_path, "rb") as f:
                image = WagtailImage(
                    file=ImageFile(BytesIO(f.read()), name=name),
                )
                image.title = title
                image.save()

        # DOCUMENTS
        original_documents = [
            "sample-pdf.pdf",
            "sample-doc.doc",
            "sample-json.json",
            "sample-xls.xls",
        ]

        for document in original_documents:
            title = f"Document {Path(document).stem.capitalize()}"
            name = f"{Path(document)}"
            directory = Path.cwd() / Path(
                "wagtail_devtools/test/fixtures/media/documents"
            )
            document_path = directory / Path(document)

            with open(document_path, "rb") as f:
                document = WagtailDocument(
                    file=ImageFile(BytesIO(f.read()), name=name),
                )
                document.title = title
                document.save()
