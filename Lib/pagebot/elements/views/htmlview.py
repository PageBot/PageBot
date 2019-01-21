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
#     htmlview.py
#
from pagebot.elements.views.baseview import BaseView
from pagebot.contexts.htmlcontext import HtmlContext

class HtmlView(BaseView):
    """Abstract class for HTML/CSS generating views."""

    def _getContext(self):
        """Answers the default context for this type of view."""
        return HtmlContext()

    def XXXbuild_scss(self, view, origin=None):
        """Build the CSS for this document. Default behavior is to import the content of the file
        if there is a path reference, otherwise build the CSS from the available values and parameters
        in self.style and self.css()."""
        b = view.context.b
        if self.cssCode is not None:
            b.addHtml(self.cssCode)
        elif self.cssPath is not None:
            b.importCss(self.cssPath) # Add CSS content of file, if path is not None and the file exists.
        else:
            b.headerCss(self.into.title or self.name or self.title)
            b.resetCss() # Add CSS to reset specific default behavior of browsers.
            b.sectionCss('Document root style')
            b.css('body', e=view) # <body> selector and style output

    # Alternative view behavior.
    # Since HTML-pages don't really need or hangle print-view options
    # such as crop marks and registrations martk, we'll simply add them
    # ass comments in the output. So at least they are traceable.

    def drawFrame(self, page, origin):
        if self.showFrame:
            self.b.comment('%s.drawFrame on %s' % (self, page))

    def drawPadding(self, page, origin):
        if self.showPadding:
            self.b.comment('%s.drawPadding on %s' % (self, page))

    def drawNameInfo(self, page, origin):
        if self.showNameInfo:
            self.b.comment('%s.drawNameInfo on %s' % (self, page))

    def drawColorBars(self, page, origin):
        if self.showColorBars:
            self.b.comment('%s.drawColorBars on %s' % (self, page))

    def drawRegistrationMarks(self, page, origin):
        if self.showRegistrationMarks:
            self.b.comment('%s.drawRegistrationMarks on %s' % (self, page))

    def drawCropMarks(self, page, origin):
        if self.showCropMarks:
            self.b.comment('%s.drawCropMarks on %s' % (self, page))

    def drawElementOrigin(self, page, origin):
        if self.showCropMarks:
            self.b.comment('%s.drawElementOrigin on %s' % (self, page))

    def drawGrid(self, page, origin, background=False):
        if self.showCropMarks:
            self.b.comment('%s.drawGrid on %s' % (self, page))

    def drawBaselines(self, page, origin, background=False):
        if self.showCropMarks:
            self.b.comment('%s.drawBaselines on %s' % (self, page))

    def drawFlowConnections(self, page, origin):
        if self.showCropMarks:
            self.b.comment('%s.drawFlowConnections on %s' % (self, page))


