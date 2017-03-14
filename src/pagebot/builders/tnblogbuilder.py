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
#     tnblogbuilder.py
#
from pagebot.builders.basebuilder import BaseBuilder

class TNBlogBuilder(BaseBuilder):
    def __init__(self, document, ):
        self._document = document

    def build(self, fileName, format=None, pageSelection=None, multiPage=True):
        u"""Build simple HTML/CSS site of static code, interpreting the content of self.document."""
        if buildCss:
            self.builsCss()
        if buildHead:
            self.buildHead()
        if buildBody:
            self.buildBody()

    def buildCss(self):
        pass

    def buildHead(self):
        pass

    def buildBody(self):
        pass

