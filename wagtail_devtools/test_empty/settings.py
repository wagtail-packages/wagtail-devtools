"""
Django settings for temp project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os

import dj_database_url


# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "c6u0-9c!7nilj_ysatsda0(f@e_2mws2f!6m0n^o*4#*q#kzp)"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "testserver", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "wagtail_devtools",
    "wagtail_devtools.test_empty",
    # "wagtail_devtools.search",
    # "wagtail.contrib.search_promotions",
    # "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    # "wagtail.contrib.settings",
    # "wagtail.embeds",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    # "wagtail.search",
    "wagtail.admin",
    # "wagtail.api.v2",
    "wagtail.contrib.modeladmin",
    # "wagtail.contrib.routable_page",
    # "wagtail.contrib.styleguide",
    "wagtail.sites",
    "wagtail",
    "taggit",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "wagtail_devtools.test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# don't use the intentionally slow default password hasher
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///test_wagtail_devtools_empty.db"
    ),
}


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

# USE_L10N = True # this isn't required here and removed in Django 5.0

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "test-static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "test-media")


# Wagtail settings

WAGTAIL_SITE_NAME = "Wagtail devtools test site"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# testing
# this restores the test-media folder after the test suite has run
# not using this at the moment, see how it goes.
# TEST_RUNNER = "wagtail_devtools.test.tests.runner.WagtailDevToolsTestRunner"

# wagtail_devtools settings

# WAGTAIL_DEVTOOLS_ENABLED = True
# WAGTAIL_DEVTOOLS_TEST_USER = {
#     "login_url": "http://localhost:8000/admin/login/",
#     "username": "admin",
#     "password": "admin",
# }

# WAGTAIL_DEVTOOLS_CONFIG = {
#     "json_dir": os.path.join(PROJECT_DIR, "test", "json"),
# }
# WAGTAIL_DEVTOOLS_MODEL_ADMIN_TYPES = [  # optional but required if you use modeladmin
#     "wagtail_devtools_test.TestModelAdminOne",
#     "wagtail_devtools_test.TestModelAdminTwo",
#     "wagtail_devtools_test.TestModelAdminThree",
# ]

# WAGTAIL_DEVTOOLS_EDIT_PAGES = [ # optional
# "auth.Group",
# "auth.User",
# "wagtailcore.Collection",
# "wagtailcore.Site",
# "wagtailcore.Task",
# "wagtailcore.Workflow",
# "wagtaildocs.Document",
# "wagtailimages.Image",
# "wagtailredirects.Redirect",
# ]

# WAGTAIL_DEVTOOLS_LISTING_PAGES = [ # optional
# "wagtailadmin_collections:index",
# "wagtailadmin_explore_root",
# "wagtailadmin_home",
# "wagtailadmin_pages:search",
# "wagtailadmin_reports:aging_pages",
# "wagtailadmin_reports:locked_pages",
# "wagtailadmin_reports:site_history",
# "wagtailadmin_workflows:index",
# "wagtailadmin_workflows:task_index",
# "wagtaildocs:index",
# "wagtailimages:index",
# "wagtailredirects:index",
# "wagtailsites:index",
# "wagtailsnippets:index",
# "wagtailusers_groups:index",
# "wagtailusers_users:index",
# ]