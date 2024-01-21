#!/bin/bash

coverage run --parallel-mode testmanage.py test wagtail_devtools.test --settings=wagtail_devtools.test.settings
coverage report -m
coverage html
