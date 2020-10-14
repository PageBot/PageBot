#!/bin/bash
set -ev
export PY="python3"
$PY -m doctest doctests/resources.txt
$PY -m doctest doctests/context-linux.txt
$PY -m doctest doctests/composer-linux.txt
$PY -m doctest doctests/babelstring-linux.txt
