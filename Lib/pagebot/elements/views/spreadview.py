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
#     spreadview.py
#
from drawBot import newPage, rect, fill, stroke, strokeWidth
from pagebot import setFillColor, setStrokeColor
from view import View

class SpreadView(View):
    u"""A View is just another kind of container, kept by document to make a certain presentation of the page tree."""
    viewId = 'SpreadView'

    def drawPageFrame(self, page, origin):
        u"""Draw the page frame if the the flag is on and  if there ie padding enough to show other meta info.
        Otherwise the padding is truncated to 0: no use to draw the frame."""
        if self.showPageFrame: # Different from base View, no check on padding.
            fill(None)
            stroke(0.5)
            strokeWidth(0.5)
            rect(origin[0], origin[1], page.w, page.h)
            #page.drawFrame(origin, self)

    def drawPages(self, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""
        doc = self.parent

        w, h, _ = doc.getMaxPageSizes(pageSelection)
        w2 = 2*w # Make spread width
        for pn, pages in doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            page = pages[0] # TODO: Make it work if there as multiple pages on the same page number.
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
            pw2 = 2*pw

            if (pn % 2 == 0): # Is even?
                newPage(pw2, ph) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
                # View may have defined a background
                if self.style.get('fill') is not None:
                    setFillColor(self.style['fill'])
                    rect(0, 0, pw2, ph)
            else: # Odd, shift origin to right
                origin = origin[0]+pw, origin[1], origin[2]

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(page, origin, self)

            self.drawPageFrame(page, origin)

            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            page.draw(origin, self)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(page, origin, self)

            # Self.infoElements now may have collected elements needed info to be drawn, after all drawing is done.
            # So the info boxes don't get covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo()

