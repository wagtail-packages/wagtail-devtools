from django.apps import AppConfig


class WagtailDevtoolsTestAppConfig(AppConfig):
    label = "wagtail_devtools_test"
    name = "wagtail_devtools.test"
    verbose_name = "Wagtail devtools tests"
    default_auto_field = "django.db.models.AutoField"
