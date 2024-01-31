# Wagtail devtools

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A set of developer tools in the form of management commands.

## Supported versions

- Python 3.8+
- Django 3.2+
- Wagtail 4.1+

## Features

### API

There is an api available at `/wagtail-devtools-api/` which will list all available endpoints.

- List all editor listing pages
- List all editor edit pages

### Admin Responses

The `admin_responses` command will use the API endpoints above to create a report of error and success pages in the console.

- [Documentation](docs/admin_responses.md)

### Content Types report

The `content_types` report will generate a report for all content types in the project.

- [Documentation](docs/content_types.md)

## Installation

~~Install the package~~ - There's no release yet so you'll need to install from the main branch.

```bash
python -m pip install wagtail-devtools
```

Install from the main branch.

```bash
python -m pip install git+https://github.com/wagtail-packages/wagtail-devtools#egg=wagtail_devtools
```

Add the package to your installed apps in your development settings file. The site will need to be running in `DEBUG` mode.

```python
DEBUG = True
INSTALLED_APPS += ["wagtail_devtools"]
```

## Links

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
