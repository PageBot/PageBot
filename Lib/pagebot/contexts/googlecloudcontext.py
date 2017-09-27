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
#     googlecloudcontext.py
#
from basecontext import BaseContext
from pagebot.contexts.builders import WebBuilder
from pagebot.contexts.strings.htmlstring import HtmlString, newHtmlString

class GoogleCloudContext(BaseContext):
    u"""A GoogleCloudContext instance runs like a Google Cloud server, asnwering
    live pages."""

    def __init__(self):
        self.b = WebBuilder()

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new styles BabelString(HtmlString) instance from s, using e or style.
        Ignore and answer s if it is already an HtmlString."""
        if isinstance(s, basestring):
            s = newHtmlString(s, self, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        assert isinstance(s, HtmlString)
        return s

