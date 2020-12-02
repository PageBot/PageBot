#!/bin/bash
set -ev
export PY="python3"
$PY tests/baselineosx.py
$PY -m doctest tests/context-osx.txt
$PY -m doctest tests/composer-osx.txt
$PY -m doctest tests/babelstring-osx.txt
$PY -m doctest tests/image-osx.txt
$PY -m doctest tests/document-osx.txt
