#!/bin/bash
cd ..
rm docs/source/*
sphinx-apidoc -o docs/source Lib/pagebot
git add docs/source/*
cd docs
make html
