# Wagtail devtools

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A set of developer tools in the form of management commands.

## Supported versions

- Python 3.9+
- Django 4.2+
- Wagtail 5.2+

## Features

### API

There is an api now available at `/wagtail-devtools-api/` which will list all available commands.

### Admin Responses

The `admin_responses` command will make a requests to the admin interface using get requests for a range of models. It will write a response result to the console.

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
