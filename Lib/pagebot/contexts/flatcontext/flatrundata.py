#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     flatrundata.py

class FlatRunData:
    """Class to store cached information in FlatBabelData.runs."""

    def __init__(self, st, pars):
        # Strike for this run.
        self.st = st
        # List of paragraphs that share the same strike.
        self.pars = pars

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
