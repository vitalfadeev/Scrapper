#!/usr/bin/env bash

SOURCE_CODE_PATH=$1
. venv/bin/activate
rm -Rf docs/build
rm -Rf docs/source/docstring
sphinx-apidoc -f -o docs/source/docstring/ $SOURCE_CODE_PATH ./test*.py */tests/*
cd docs && make html && cd ..
