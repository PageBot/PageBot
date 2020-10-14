#!/bin/bash
set -ev
export PY="python3.8"
$PY -m doctest doctests/context-osx.txt
$PY -m doctest doctests/composer-osx.txt
$PY -m doctest doctests/babelstring-osx.txt
$PY -m doctest doctests/image-osx.txt
