# Contributing to devtools

Contributions are welcome, and they are greatly appreciated!

### Install

To make changes to this project, first clone this repository:

```sh
git clone https://github.com/nickmoreton/wagtail-devtools.git
cd wagtail-devtools
```

With your preferred virtualenv activated, install testing dependencies:

#### Using pip

```sh
python -m pip install --upgrade pip>=21.3
python -m pip install -e '.[testing,dev]' -U
```

#### Using flit

```sh
python -m pip install flit
flit install
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit).
It is included in the project testing requirements. To set up locally:

```shell
# go to the project directory
$ cd wagtail-devtools
# initialize pre-commit
$ pre-commit install

# Optional, run all checks once for this, then the checks will run only on the changed files
$ git ls-files --others --cached --exclude-standard | xargs pre-commit run --files
```

### How to run tests with tox

With tox installed, you can run the tests for all supported environments with:

```sh
tox
```

or, you can run them for a specific environment `tox -e python3.11-django4.2-wagtail5.1` or specific test
`tox -e python3.11-django4.2-wagtail5.1-sqlite wagtail-devtools.tests.test_file.TestClass.test_method`

To run the test app interactively, use `tox -e interactive`, visit `http://127.0.0.1:8020/admin/` and log in with `admin`/`changeme`.

### Development setup

With your preferred virtualenv activated:

```sh
python testmanage.py migrate
python testmanage.py build_fixtures
python testmanage.py runserver
```

You can access the site at `http://localhost:8000/` and the admin at `http://localhost:8000/admin/`.

To log in to the admin, use `superuser`/`superuser`.

#### Optional use of build_fixtures

The `build_fixtures` command will create a set of pages and images for use in the testing app. It is not required to run the tests, but it can be useful for testing the devtools in a real-world scenario.

The option to clear old data is available with `--clear`. This will delete all data from the database before creating new data.

```sh
python testmanage.py build_fixtures --clear
```
