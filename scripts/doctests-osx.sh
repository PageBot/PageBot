#!/bin/bash
set -ev
python3 -m doctest -v tests/test-contexts-osx.txt
