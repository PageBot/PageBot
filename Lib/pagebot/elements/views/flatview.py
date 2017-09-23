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
#     flatview.py
#
import os
import shutil

from platforms import platform # Get the platform we are building for.
from pagebot.elements.views.baseview import BaseView
from pagebot.elements.views.strings import newFlatString, FlatString
from pagebot.builders.flatbuilder import flatBuilder

class FlatView(BaseView):
    u"""Support the flat library, so PageBot can run on non-OSX environments."""
    viewId = 'Flat'

    def build(self, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""
        doc = self.parent
        b = self.b
        
        w, h, _ = doc.getMaxPageSizes(pageSelection)
        for pn, pages in doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            page = pages[0] # TODO: make this work for pages that share the same page number
            pw, ph = w, h  # Copy from main (w, h), since they may be altered.
            
            if self.pl > self.MIN_PADDING and self.pt > self.MIN_PADDING and self.pb > self.MIN_PADDING and self.pr > self.MIN_PADDING:
                pw += self.pl + self.pr
                ph += self.pt + self.pb
                if self.originTop:
                    origin = self.pl, self.pt, 0
                else:
                    origin = self.pl, self.pb, 0
            else:
                pw = page.w # No padding defined, follow the size of the page.
                ph = page.h
                origin = (0, 0, 0)

            b.newPage(pw, ph) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
            # View may have defined a background
            if self.style.get('fill') is not None:
                setFillColor(self.style['fill'])
                b.rect(0, 0, pw, ph)

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(page, origin, self)

            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            page.drawFlat(origin, self)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(page, origin, self)

            # Self.infoElements now may have collected elements needed info to be drawn, after all drawing is done.
            # So the info boxes don't get covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo()

