from io import BytesIO
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.management import BaseCommand
from django.db import IntegrityError
from wagtail.contrib.redirects.models import Redirect
from wagtail.contrib.search_promotions.models import Query, SearchPromotion
from wagtail.documents.models import Document as WagtailDocument
from wagtail.images.models import Image as WagtailImage
from wagtail.models import Site
from wagtail.models.collections import Collection

from wagtail_devtools.test.models import (
    GenericSettingOne,
    GenericSettingThree,
    GenericSettingTwo,
    HomePage,
    SiteSettingOne,
    SiteSettingThree,
    SiteSettingTwo,
    StandardPageOne,
    StandardPageThree,
    StandardPageTwo,
    TestModelAdminOne,
    TestModelAdminThree,
    TestModelAdminTwo,
    TestSnippetOne,
    TestSnippetThree,
    TestSnippetTwo,
)


class Command(BaseCommand):
    help = "Create or load fixtures for testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing fixtures. If not specified, load fixtures.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.clear_fixtures()

        self.create_superuser()
        self.update_home_page()
        self.create_standard_pages()
        self.create_snippets()
        self.create_modeladmins()
        self.create_settings()
        self.create_collections()
        self.create_redirects()
        self.create_promoted_searches()
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
        rev = home_page.save_revision()
        rev.publish()

    def create_standard_pages(self):
        self.stdout.write("Creating standard pages.")

        home_page = HomePage.objects.first()

        sp = StandardPageOne(title="Standard Page One")
        home_page.add_child(instance=sp)
        rev = sp.save_revision()
        rev.publish()

        # Intentionally is a draft page
        sp = StandardPageTwo(title="Standard Page Two")
        home_page.add_child(instance=sp)
        rev = sp.save_revision()
        rev.publish()
        sp.unpublish()

        # Intentionally has a template error
        sp = StandardPageThree(title="Standard Page Three")
        home_page.add_child(instance=sp)
        rev = sp.save_revision()
        rev.publish()

    def create_snippets(self):
        self.stdout.write("Creating snippets.")

        for x in range(1, 5):
            TestSnippetOne.objects.create(title=f"Test Snippet {x}")
            TestSnippetTwo.objects.create(title=f"Test Snippet {x}")
            TestSnippetThree.objects.create(title=f"Test Snippet {x}")

    def create_modeladmins(self):
        self.stdout.write("Creating model admins.")

        for x in range(1, 5):
            TestModelAdminOne.objects.create(title=f"Test Model Admin {x}")
            TestModelAdminTwo.objects.create(title=f"Test Model Admin {x}")
            TestModelAdminThree.objects.create(title=f"Test Model Admin {x}")

    def create_settings(self):
        self.stdout.write("Creating settings.")

        site_setting = SiteSettingOne.for_site(Site.objects.first())
        site_setting.name = "Site Setting One"
        site_setting.save()

        site_setting = SiteSettingTwo.for_site(Site.objects.first())
        site_setting.name = "Site Setting Two"
        site_setting.save()

        site_setting = SiteSettingThree.for_site(Site.objects.first())
        site_setting.name = "Site Setting Three"
        site_setting.save()

        generic_setting = GenericSettingOne.load(Site.objects.first())
        generic_setting.name = "Generic Setting One"
        generic_setting.save()

        generic_setting = GenericSettingTwo.load(Site.objects.first())
        generic_setting.name = "Generic Setting Two"
        generic_setting.save()

        generic_setting = GenericSettingThree.load(Site.objects.first())
        generic_setting.name = "Generic Setting Three"
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

    def create_promoted_searches(self):
        self.stdout.write("Creating promoted searches.")

        home_page = HomePage.objects.first()
        for x in range(1, 5):
            try:
                SearchPromotion.objects.create(
                    page=home_page,
                    query=Query.objects.create(query_string=f"Test Query {x}"),
                    description=f"Test Search Promotion {x}",
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Search promotion for query 'Test Query {x}' already exists. Skipping creation."
                    )
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

    def clear_fixtures(self):
        self.stdout.write(self.style.SUCCESS("Clearing fixtures."))

        StandardPageOne.objects.all().delete()
        StandardPageTwo.objects.all().delete()
        StandardPageThree.objects.all().delete()
        TestSnippetOne.objects.all().delete()
        TestSnippetTwo.objects.all().delete()
        TestSnippetThree.objects.all().delete()
        TestModelAdminOne.objects.all().delete()
        TestModelAdminTwo.objects.all().delete()
        TestModelAdminThree.objects.all().delete()
        SiteSettingOne.objects.all().delete()
        SiteSettingTwo.objects.all().delete()
        SiteSettingThree.objects.all().delete()
        GenericSettingOne.objects.all().delete()
        GenericSettingTwo.objects.all().delete()
        GenericSettingThree.objects.all().delete()
        WagtailImage.objects.all().delete()
        WagtailDocument.objects.all().delete()
        Query.objects.all().delete()
        SearchPromotion.objects.all().delete()
