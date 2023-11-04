from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5fsz%!%$ai6mzr@klo0^0is_)^xi6dpp&3@(34r75v9td5wa7s"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Wagtail Devtools
DEVTOOLS_APPS_PREFIX = "sandbox"
DEVTOOLS_REGISTERED_MODELADMIN = [
    "home.TestModelAdmin",
]


try:
    from .local import *  # noqa
except ImportError:
    pass
