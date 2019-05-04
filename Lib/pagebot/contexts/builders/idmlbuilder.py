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
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     idmlbuilder.py
#
import os
import codecs
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.toolbox.transformer import object2SpacedString
from pagebot.toolbox.units import asFormatted, pt
from pagebot.constants import A4Rounded
from pagebot.contexts.bezierpaths.commandbezierpath import CommandBezierPath as BezierPath

class IdmlBuilder(BaseBuilder):
    """TODO: Implement functions to make it work.
    """
    
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
