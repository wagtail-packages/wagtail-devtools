# Generated by Django 4.0.10 on 2023-11-18 15:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        (
            "wagtail_devtools_test",
            "0007_genericsettingthree_genericsettingtwo_sitesettingtwo_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GenericSetting",
            new_name="GenericSettingOne",
        ),
        migrations.RenameModel(
            old_name="SiteSetting",
            new_name="SiteSettingOne",
        ),
    ]
