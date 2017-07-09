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
#     sitebuilder.py
#
from basebuilder import BaseBuilder
from htmlbuilder import HtmlBuilder
from cssbuilder import CssBuilder

class SiteBuilder(BaseBuilder):

    def build(self, path, format=None, pageSelection=None, multiPage=True, buildHead=True, buildBody=True, buildCss=True):
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

