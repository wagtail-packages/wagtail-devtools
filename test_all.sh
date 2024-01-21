#!/bin/bash

coverage run --parallel-mode testmanage.py test wagtail_devtools.test --settings=wagtail_devtools.test.settings
coverage run --parallel-mode testmanage_empty.py test wagtail_devtools.test_empty --settings=wagtail_devtools.test_empty.settings
coverage combine
coverage report -m
coverage html
