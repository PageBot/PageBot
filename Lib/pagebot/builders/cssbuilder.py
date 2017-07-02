# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     cssbuilder.py
#
import codecs
from basebuilder import BaseBuilder

class CssBuilder(BaseBuilder):

    def build(self, e, view):
        u"""
        Builds the CSS for Element e and downwards, using the view parent document 
        as reference for styles.
        """
        assert self.path is not None
        out = codecs.open(self.path, 'w', 'utf-8')
        f.write('@charset "UTF-8";\n\n')

        f.close()
