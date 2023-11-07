from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import TestModelAdmin


class TestModelAdmin(ModelAdmin):
    model = TestModelAdmin


modeladmin_register(TestModelAdmin)
