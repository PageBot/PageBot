# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     basebuilder.py
#
class BaseBuilder(object):
    u"""The BaseBuilder is the abstract builder class, for all builders that need
    to write files in a directory, besides the binary export formats that are already
    supported by DrawBot."""

    def __init__(self, path):
        self.path = path

    def build(self, e, view):
        pass
        

