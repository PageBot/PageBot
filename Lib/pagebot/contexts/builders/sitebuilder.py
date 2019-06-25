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
#     sitebuilder.py
#
from pagebot.contexts.builders.htmlbuilder import HtmlBuilder

class SiteBuilder(HtmlBuilder):
    """Generic output builder container, used of collecting html, css, js,
    include paths and other data needed to export the website, e.g. by the
    GitView or MampView."""

    def frameDuration(self, frameDurection):
    	pass