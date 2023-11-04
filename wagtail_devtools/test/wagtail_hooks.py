from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


if not WAGTAIL_VERSION >= (5, 2):
    from .models import TestModelAdmin

    class TestModelAdmin(ModelAdmin):
        model = TestModelAdmin

    modeladmin_register(TestModelAdmin)
