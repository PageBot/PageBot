#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Testing unneccesary use of comprehension.

data = {}
contentdict = {'a': ['bla1', 'bla2'], 'b': ['bla3', 'bla4']}

for k, v in contentdict.items():
    bb = []

    for name in v:
        bb.append(name)

    #data[k] = [name for name in v]
    data[k] = v

print(bb)
print(data)
