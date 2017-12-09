# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     basebuilder.py
#
import codecs

class BaseBuilder(object):
    u"""The BaseBuilder is the abstract builder class, for all builders that need
    to write files in a directory, besides the binary export formats that are already
    supported by DrawBot."""

    def __init__(self, path):
        self.path = path
        self._output = None
        self._initialize()

    def _initialize(self):
        pass

    def openOutput(self, path=None):
        u"""Open the output on the optional *path*, otherwise use *self.path*."""
        assert self._output is None
        self._output = codecs.open(path or self.path, 'w', 'utf-8')

    def closeOutput(self):
        self._output.close()
        self._output = None

    def write(self, s):
        u"""Write the string *s* to the output file."""
        self._output.write(s)
     
    def getPath(self):
        u"""Default behavior is to answer the value of self.path."""  
        return self.path
