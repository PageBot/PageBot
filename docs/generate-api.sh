#!/bin/bash
rm source/*
sphinx-apidoc -o source ../Lib/pagebot
git add source/*
