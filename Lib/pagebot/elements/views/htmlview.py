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
#     htmlview.py
#
from pagebot.builders import WebBuilder
from pagebot.elements.views.baseview import BaseView
from pagebot.elements.views.strings import newHtmlString, HtmlString

class HtmlView(BaseView):
    u"""Abstract class for HTML/CSS generating views."""

    # Postfix for self.build_html method names. 
    buildType = 'html' 

    b = WebBuilder() # self.b builder for this view.

    #   T E X T

    @classmethod
    def newString(cls, s, view=None, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        if not isinstance(s, HtmlString):
            s = newHtmlString(s, view=view, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        return s
 
