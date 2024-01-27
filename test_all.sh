#!/bin/bash

coverage run testmanage.py test wagtail_devtools.test --settings=wagtail_devtools.test.settings
coverage report -m
coverage html
