#!/bin/bash
set -ev
python3 -m doctest doctests/resources.txt
python3 -m doctest doctests/context-linux.txt
python3 -m doctest doctests/composer-linux.txt
python3 -m doctest doctests/string-linux.txt
