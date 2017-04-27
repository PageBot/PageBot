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
#     view.py
#
from drawBot import saveImage, newPage

from pagebot.elements.element import Element
from pagebot.style import makeStyle, getRootStyle
from pagebot.toolbox.transformer import pointOffset, obj2StyleId, point3D

class View(Element):
    u"""A View is just another kind of container, kept by document to make a certain presentation of the page tree."""
    viewId = 'View'

    def drawPages(self, document, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""

        w, h, _ = document.getMaxPageSizes(pageSelection)
        paddingX = self.pl + self.pr
        paddingY = self.pt + self.pb
        for page in document.getSortedPages():
            if pageSelection is not None and not page.y in pageSelection:
                continue
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            if paddingX or paddingY:
                w += paddingX
                h += paddingY
            else:
                w = page.w # No padding defined, follow the size of the page.
                h = page.h

            newPage(w, h) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
            # Let the page draw itself on the current DrawBot view port if self.writer is None.
            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            origin = point3D((self.pl, self.pt, self.pzf))
            page.draw(origin) 

    def export(self, document, fileName, pageSelection=None, multiPage=True):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted. The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct the type of
        drawing and export that needs to be done.
        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in special cases, there is not 
        straighforward (or sequential) export of pages, e.g. when generating HTML/CSS. In that case use 
        MyBuilder(document).export(fileName), the builder is responsible to query the document, pages, elements and styles.
        """
        self.drawPages(document, pageSelection)

        # If rootStyle['frameDuration'] is set and saving as movie or animated gif, 
        # then set the global frame duration.
        frameDuration = self.css('frameDuration')
        if frameDuration is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
            frameDuration(frameDuration)

        # http://www.drawbot.com/content/canvas/saveImage.html
        saveImage(fileName, multipage=multiPage)


class DefaultView(View):
    viewId = 'Default'

class SingleView(View):
    viewId = 'Single'

class ThumbView(View):
    viewId = 'Thumb'


