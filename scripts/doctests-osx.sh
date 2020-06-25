#!/bin/bash
set -ev
python3 -m doctest doctests/context-osx.txt
python3 -m doctest doctests/composer-osx.txt
python3 -m doctest doctests/babelstring-osx.txt
python3 -m doctest doctests/image-osx.txt
