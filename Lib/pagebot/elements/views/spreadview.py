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
#     spreadview.py
#
from view import View

class SpreadView(View):
    u"""A View is just another kind of container, kept by document to make a certain presentation of the page tree."""
    viewId = 'SpreadView'

    def drawPages(self, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""
        doc = self.parent

        w, h, _ = doc.getMaxPageSizes(pageSelection)
        w2 = 2*w # Make spread width
        for page in doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            if self.pl > self.MIN_PADDING and self.pt > self.MIN_PADDING and self.pb > self.MIN_PADDING and self.pr > self.MIN_PADDING:
                w += self.pl + self.pr
                h += self.pt + self.pb
                if self.originTop:
                    origin = self.pl, self.pt, 0
                else:
                    origin = self.pl, self.pb, 0
            else:
                w = page.w # No padding defined, follow the size of the page.
                h = page.h
                origin = (0, 0, 0)

            if math.even(page.pn):
                newPage(w2, h) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
                # View may have defined a background
                if self.style.get('fill') is not None:
                    setFillColor(self.style['fill'])
                    rect(0, 0, w2, h)
            else # Uneven, shift origin to right
                origin = origin[0]+w, origin[1], origin[2]
            # Let the page draw itself on the current DrawBot view port if self.writer is None.
            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            page.draw(origin, self)
            # Self.infoElements now may have collected elements needed info to be drawn, after all drawing is done.
            # So the info boxes don't get covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo()

