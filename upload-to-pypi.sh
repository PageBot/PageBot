#!/bin/bash
rm dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
