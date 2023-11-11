# Wagtail devtools

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A set of developer tools in the form of management commands.

## Features

### Admin Responses

The `admin_responses` command will make a request to the admin interface using get requests for all the wagtail core admin page. It will right a response result to the console.

Optionally you can specify your ModelAdmin models in settings a include them in the results.

```bash
python manage.py admin_responses
```

The command is only available in debug mode `DEBUG=True`

Your site will need data in place, either from fixtures or a sample of a live sites data to get meaningful results.

### Model Admin Reporting

Add the models you want to report on to your settings

```python
DEVTOOLS_REGISTERED_MODELADMIN = [
    "app_name_one.ModelNameOne",
    "app_name_one.ModelNameTwo",
    "app_name_tow.ModelNameOne",
    ...,
]
```

### Content Types report

This is a Work in progress.

## Supported versions

- Python 3.8+
- Django 3.2+
- Wagtail 4.1+

## Usage

Install the package

```bash
python -m pip install wagtail-devtools
```

Add the package to your installed apps

```python
INSTALLED_APPS = ["wagtail_devtools"]
```
