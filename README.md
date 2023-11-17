# Wagtail devtools

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A set of developer tools in the form of management commands.

## Supported versions

- Python 3.8+
- Django 3.2+
- Wagtail 4.1+

## Features

### Admin Responses

- [Documentation](docs/admin_responses.md)

### Content Types report

- [Documentation](docs/content_types.md)

## Installation

Install the package

```bash
python -m pip install wagtail-devtools
```

Add the package to your installed apps in your development settings file. The site will need to be running in `DEBUG` mode.

```python
DEBUG = True
INSTALLED_APPS += ["wagtail_devtools"]
```
