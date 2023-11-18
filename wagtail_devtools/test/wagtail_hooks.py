from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import TestModelAdminOne, TestModelAdminThree, TestModelAdminTwo


class TestModelAdminOne(ModelAdmin):
    model = TestModelAdminOne


class TestModelAdminTwo(ModelAdmin):
    model = TestModelAdminTwo


class TestModelAdminThree(ModelAdmin):
    model = TestModelAdminThree


modeladmin_register(TestModelAdminOne)
modeladmin_register(TestModelAdminTwo)
modeladmin_register(TestModelAdminThree)
