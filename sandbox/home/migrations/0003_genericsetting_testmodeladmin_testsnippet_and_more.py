# Generated by Django 4.2.7 on 2023-11-04 16:52

from django.db import migrations, models
import django.db.models.deletion
from wagtail import VERSION as WAGTAIL_VERSION


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0002_create_homepage"),
    ]

    if not WAGTAIL_VERSION >= (5, 2):
        operations = [
            migrations.CreateModel(
                name="GenericSetting",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("name", models.CharField(max_length=255)),
                ],
                options={
                    "abstract": False,
                },
            ),
            migrations.CreateModel(
                name="TestModelAdmin",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("title", models.CharField(max_length=255)),
                ],
            ),
            migrations.CreateModel(
                name="TestSnippet",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("title", models.CharField(max_length=255)),
                ],
            ),
            migrations.CreateModel(
                name="SiteSetting",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("name", models.CharField(max_length=255)),
                    (
                        "site",
                        models.OneToOneField(
                            editable=False,
                            on_delete=django.db.models.deletion.CASCADE,
                            to="wagtailcore.site",
                        ),
                    ),
                ],
                options={
                    "abstract": False,
                },
            ),
        ]
    else:
        operations = [
            migrations.CreateModel(
                name="GenericSetting",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("name", models.CharField(max_length=255)),
                ],
                options={
                    "abstract": False,
                },
            ),
            migrations.CreateModel(
                name="TestSnippet",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("title", models.CharField(max_length=255)),
                ],
            ),
            migrations.CreateModel(
                name="SiteSetting",
                fields=[
                    (
                        "id",
                        models.BigAutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("name", models.CharField(max_length=255)),
                    (
                        "site",
                        models.OneToOneField(
                            editable=False,
                            on_delete=django.db.models.deletion.CASCADE,
                            to="wagtailcore.site",
                        ),
                    ),
                ],
                options={
                    "abstract": False,
                },
            ),
        ]
