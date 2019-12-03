#!/bin/bash
rm docs/source/*
sphinx-apidoc -o docs/source Lib/pagebot
git add docs/source/*
