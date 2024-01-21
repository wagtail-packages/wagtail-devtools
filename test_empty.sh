#!/bin/bash

coverage run testmanage_empty.py test wagtail_devtools.test_empty --settings=wagtail_devtools.test_empty.settings
coverage report -m
coverage html
