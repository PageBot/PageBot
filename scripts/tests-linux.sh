#!/bin/bash
set -ev
export PY="python3"
$PY -m doctest tests/resources.txt
$PY -m doctest tests/context-linux.txt
$PY -m doctest tests/composer-linux.txt
$PY -m doctest tests/babelstring-linux.txt
$PY -m doctest tests/document-linux.txt
