#!/usr/bin/env python
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
from pagebot.elements.views.baseview import BaseView
from pagebot.contexts.htmlcontext import HtmlContext

class HtmlView(BaseView):
    u"""Abstract class for HTML/CSS generating views."""

    def _getContext(self):
        u"""Answer the default context for this type of view."""
        return HtmlContext()

    def build_css(self, view):
        u"""Build the CSS for this document. Default behavior is to import the content of the file
        if there is a path reference, otherwise build the CSS from the available values and parameters
        in self.style and self.css()."""
        b = view.context.b
        if self.cssCode is not None:
            b.addHtml(self.cssCode)
        elif self.info.cssPath is not None:
            b.importCss(self.cssPath) # Add CSS content of file, if path is not None and the file exists.
        else:
            b.headerCss(self.name or self.title)
            b.resetCss() # Add CSS to reset specific default behavior of browsers.
            b.sectionCss('Document root style')
            b.css('body', self.rootStyle) # <body> selector and style output
