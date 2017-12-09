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
#     mdblogbuilder.py
#
#	  Exporting MarkDown (MacDown) text with Wiki codes.
#	  TODO: To be implemented.
#
from pagebot.builders.basebuilder import BaseBuilder

class MDBlogBuilder(BaseBuilder):
    def __init__(self, document, ):
        self._document = document

    def build(self, fileName, format=None, pageSelection=None, multiPage=True):
        u"""Build simple HTML/CSS site of static code, interpreting the content of self.document."""
        pass
        

