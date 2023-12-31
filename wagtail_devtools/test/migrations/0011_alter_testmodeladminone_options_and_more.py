# Generated by Django 4.0.10 on 2023-11-18 15:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_devtools_test", "0010_rename_testsnippet_testsnippetone"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="testmodeladminone",
            options={
                "verbose_name": "Model Admin One",
                "verbose_name_plural": "Model Admins One",
            },
        ),
        migrations.AlterModelOptions(
            name="testmodeladminthree",
            options={
                "verbose_name": "Model Admin Three",
                "verbose_name_plural": "Model Admins Three",
            },
        ),
        migrations.AlterModelOptions(
            name="testmodeladmintwo",
            options={
                "verbose_name": "Model Admin Two",
                "verbose_name_plural": "Model Admins Two",
            },
        ),
        migrations.AlterModelOptions(
            name="testsnippetone",
            options={
                "verbose_name": "Test Snippet One",
                "verbose_name_plural": "Test Snippets One",
            },
        ),
        migrations.AlterModelOptions(
            name="testsnippetthree",
            options={
                "verbose_name": "Test Snippet Three",
                "verbose_name_plural": "Test Snippets Three",
            },
        ),
        migrations.AlterModelOptions(
            name="testsnippettwo",
            options={
                "verbose_name": "Test Snippet Two",
                "verbose_name_plural": "Test Snippets Two",
            },
        ),
    ]
