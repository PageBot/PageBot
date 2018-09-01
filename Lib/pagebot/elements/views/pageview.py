#!/usr/bin/env python
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
#     pageview.py
#

import os
from random import random
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from pagebot.toolbox.color import color, noColor, grayColor, blackColor
from pagebot.elements.views.baseview import BaseView
from pagebot.elements.pbquire import Quire
from pagebot.style import RIGHT
from pagebot.constants import ORIGIN, GRID_COL, GRID_ROW, GRID_SQR, GRID_LINE, GRID_INDEX, GRID_Y
from pagebot.toolbox.units import pt, pointOffset, point2D, asFormatted
from pagebot.toolbox.transformer import *

class PageView(BaseView):
    """The PageView contains the set of Quire instances to export the pages as
    documents. A View is just another kind of container, kept by a Document to
    make a certain presentation of the page tree. The PageView typically holds
    Quire elements that make one-directional links to document pages in order
    to compose them in spreads or folding compositions."""
    viewId = 'Page'

    EXPORT_PATH = '_export/' # Default path for local document export, that does not commit documents to Github.

    def newQuire(self, folds=None, startPage=None):
        """Add a new Quire instance to self.elements."""
        Quire(folds=folds, startPage=startPage, parent=self)

    def build(self, path=None, pageSelection=None, multiPage=True):
        """Draw the selected pages. pageSelection is an optional set of
        y-pageNumbers to draw.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BusinessCard, A4, QUIRE_QUARTO
        >>> doc = Document(size=A4, autoPages=4) # Make 4 pages to be composed as a Quire of 2 spreads
        >>> view = doc.view
        >>> view.newQuire(folds=QUIRE_QUARTO)
        >>> view.newQuire(folds=QUIRE_QUARTO)
        >>> len(view.elements)
        2
        >>> len(view.elements[0])
        8
        """

        if not path:
            path = self.EXPORT_PATH + self.doc.name + '.pdf' # Default export as PDF.
        # If default _export directory does not exist, then create it.
        if path.startswith(self.EXPORT_PATH) and not os.path.exists(self.EXPORT_PATH):
            os.makedirs(self.EXPORT_PATH)

        context = self.context # Get current context and builder from doc. Can be DrawBot or Flat

        # Save the intended extension into the context, so it knows what we'll
        # be saving to.
        context.fileType = path.split('.')[-1]

        # Find the maximum document page size to this in all page sizes of the
        # document.
        w, h, _ = self.doc.getMaxPageSizes(pageSelection)

        # Make sure that canvas is empty, there may have been another document
        # building in this context.
        context.newDrawing()
        context.newDocument(w, h) # Allow the context to create a new document and page canvas.

        for pn, pages in self.doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue

            # TODO: Add some options for layout of the combined pages,
            # depending on the spread view option.
            # self.showSpreadPages # Show even/odd pages as spread, as well as pages that share the same pagenumber.
            # self.showSpreadMiddleAsGap # Show the spread with single crop marks. False glues pages togethers as in real spread.

            # Create a new DrawBot viewport page to draw template + page, if
            # not already done. In case the document is oversized, then make
            # all pages the size of the document, so the pages can draw their
            # crop-marks. Otherwise make DrawBot pages of the size of each
            # page. Size depends on the size of the larges pages + optional
            # decument padding.
            page = pages[0] # TODO: make this work for pages that share the same page number
            pw, ph = w, h  # Copy from main (w, h), since they may be altered, from the orgiinal document size..

            if self.pl > self.minPadding and \
               self.pt > self.minPadding and \
               self.pb > self.minPadding and \
               self.pr > self.minPadding:
                pw += self.pl + self.pr
                ph += self.pt + self.pb
                if self.originTop:
                    origin = self.pl, self.pt, pt(0)
                else:
                    origin = self.pl, self.pb, pt(0)
            else:
                pw = page.w # No padding defined, follow the size of the page.
                ph = page.h
                origin = ORIGIN

            context.newPage(pw, ph) #  Make page in context, actual page may be smaller if showing cropmarks.
            # If page['frameDuration'] is set and saving as movie or animated gif,
            # then set the global frame duration.
            context.frameDuration(page.frameDuration) # Set the duration of this page, in case exporting GIF

            # View may have defined a background. Build with page bleed, if it is defined.
            fillColor = self.style.get('fill', noColor)

            if fillColor is not noColor:
                bt, br, bb, bl = page.bleed
                context.fill(fillColor)
                context.rect(page.leftBleed, page.bottomBleed, pw+br+bl, ph+bt+bb)

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(page, self, origin)

            # If there is any page meta info defined to be drawn on the background
            # suchs as the grid, then draw that first.
            self.drawPageMetaInfoBackground(page, origin)

            # Use the (docW, docH) as offset, in case cropmarks need to be
            # displayed. Recursively call all elements in the tree to build
            # themselves. Note that is independent from the context. If there
            # is a difference, the elements should make the switch themselves.
            page.buildChildElements(self, origin)

            self.drawPageMetaInfo(page, origin, path) # Add path to show the file name in header.

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(page, self, origin)

            # Self.infoElements now may have collected elements needed info to be drawn, after all drawing is done.
            # So the info boxes don't get covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo()

        """Export the document to fileName for all pages in sequential order.
        If pageSelection is defined, it must be a list with page numbers to
        export. This allows the order to be changed and pages to be omitted.
        The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct
        the type of drawing and export that needs to be done.

        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in
        special cases, there is not straighforward (or sequential) export of
        pages, e.g. when generating HTML/CSS. In that case use
        MyBuilder(document).export(fileName), the builder is responsible to
        query the document, pages, elements and styles."""

        folder = path2ParentPath(path)

        if not os.path.exists(folder):
            os.mkdir(folder)

        # FIXME:
        #  - "fileName" is undefined
        #  - "frameDuration" is a method or a CSS value ?
        #if frameDuration is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
        #    frameDuration(frameDuration)

        context.saveDocument(path, multiPage=multiPage)


    #   D R A W I N G  P A G E  M E T A  I N F O

    def drawPageMetaInfoBackground(self, page, origin):
        """Draw the background meta info of the page, depending on the settings of the
        flags.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=context)
        >>> page = doc[1]
        >>> view = doc.getView()
        >>> view.showGridBackground = [GRID_COL, GRID_ROW]
        >>> view.drawPageMetaInfoBackground(page, (0, 0))
        """
        if self.showGridBackground: # Showing grid on foreground?
            self.drawGrid(page, origin, self.showGridBackground)

    def drawPageMetaInfo(self, page, origin, path=None):
        """Draw the foreground meta info of the page, depending on the settings of the
        flags.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> path = '_export/PageMetaInfo.pdf'
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=context)
        >>> page = doc[1]
        >>> view = doc.getView()
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawPageMetaInfo(page, (0, 0), path)
        """
        self.drawPageFrame(page, origin)
        self.drawPagePadding(page, origin)
        self.drawPageNameInfo(page, origin, path) # Use path to show file name in page meta info.
        self.drawPageRegistrationMarks(page, origin)
        self.drawPageCropMarks(page, origin)
        if self.showGrid: # Showing grid on foreground?
            self.drawGrid(page, origin, self.showGrid)
        self.drawBaselineGrid(page, origin)
        if self.showPageOrigin: # Test here, as same function is used for drawing origin on elements.
            self.drawElementOrigin(page, origin)

    def drawPageFrame(self, page, origin):
        """Draw the page frame if the the flag is on and  if there ie padding
        enough to show other meta info.  Otherwise the padding is truncated to
        0: no use to draw the frame.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPageFrame = True
        >>> view.drawPageFrame(e, (0, 0))

        """
        if self.showPageFrame and \
                self.pl > self.minPadding and self.pr > self.minPadding and \
                self.pt > self.minPadding and self.pb > self.minPadding:
            context = self.context
            context.fill(noColor)
            context.stroke(color(0, 0, 1), pt(0.5))
            context.rect(origin[0], origin[1], page.w, page.h)
            #page.drawFrame(origin, self)

    def drawPagePadding(self, page, origin):
        """Draw the page frame of its current padding.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPageFrame = True
        >>> view.drawPageFrame(e, (0, 0))
        """
        pt, pr, pb, pl = page.padding
        if self.showPagePadding and (pt or pr or pb or pl):
            context = self.context

            p = pointOffset(page.origin, origin)
            p = page._applyScale(self, p)
            px, py, _ = page._applyAlignment(p) # Ignore z-axis for now.

            context.fill(noColor)
            context.stroke(self.css('viewPagePaddingStroke', color(0.2, 0.2, 1)),
                                   self.css('viewPagePaddingStrokeWidth', 0.5))
            if page.originTop:
                context.rect(px+pl, py+pb, page.w-pl-pr, page.h-pt-pb)
                #context.rect(px+pl, py+page.h-pb, page.w-pl-pr, page.h-pt-pb)
            else:
                context.rect(px+pl, py+pb, page.w-pl-pr, page.h-pt-pb)
            page._restoreScale(self)

    def drawPageNameInfo(self, page, origin, path):
        """Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> path = '_export/PageNameInfo.pdf'
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPageNameInfo = True
        >>> view.drawPageNameInfo(e, (0, 0), path)
        """
        if self.showPageNameInfo:
            context = self.context
            cmDistance = self.css('viewCropMarkDistance')
            cmSize = self.css('viewCropMarkSize') - cmDistance
            fontSize = self.css('viewPageNameFontSize')
            dt = datetime.datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            if page.parent is not None: # Test if there is a document
                pn = page.parent.getPageNumber(page)
                title = page.parent.title or 'Untitled'
            else: # Otherwise always page number #1
                pn = 1
                title = 'Untitled'
            s = 'Page %s | %s | %s' % (pn, d, title)
            if page.name and page.name != 'default':
                s += ' | ' + page.name
            if path is not None:
                s += ' | ' + path.split('/')[-1]
            bs = context.newString(s, style=dict(font=self.css('viewPageNameFont'), textFill=blackColor, fontSize=fontSize))
            self.context.text(bs, (self.pl + cmDistance, self.pb + page.h + cmSize - fontSize*2)) # Draw on top of page.

    #   D R A W I N G  F L O W S

    def drawFlowConnections(self, e, origin, b):
        """If rootStyle.showFlowConnections is True, then draw the flow connections
        on the page, using their stroke/width settings of the style."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.

        if self.showFlowConnections:
            for seq in e.getFlows().values():
                # For all the flow sequences found in the page, draw flow arrows at offset (ox, oy)
                # This offset is defined by optional
                tbStart = e.getElement(seq[0].eId)
                startX = tbStart.x
                startY = tbStart.y
                for tbTarget in seq[1:]:
                    tbTarget = e.getElement(tbTarget.eId)
                    targetX = tbTarget.x
                    targetY = tbTarget.y
                    self.drawArrow(e, px+startX, py+startY+tbStart.h, px+startX+tbStart.w, py+startY, -1)
                    self.drawArrow(e, px+startX+tbStart.w, py+startY, px+targetX, py+targetY+tbTarget.h, 1)
                    tbStart = tbTarget
                    startX = targetX
                    startY = targetY
                self.drawArrow(e, px+startX, py+startY+tbStart.h, px+startX+tbStart.w, py+startY, -1)

                if e != e.parent.getLastPage():
                    # Finalize with a line to the start, assuming it is on the next page.
                    tbTarget = e.getElement(seq[0].eId)
                    self.drawArrow(e, px+startX+tbStart.w, py+startY, px+tbTarget.x, py+tbTarget.y+tbTarget.h-e.h, 1)

    def drawArrow(self, e, xs, ys, xt, yt, onText=1, startMarker=False, endMarker=False, fms=None, fmf=None,
            fill=noColor, stroke=noColor, strokeWidth=None):
        """Draw curved arrow marker between the two points.
        TODO: Add drawing of real arrow-heads, rotated in the right direction."""
        if fms is None:
            fms = self.css('viewFlowMarkerSize')
        if fmf is None:
            fmf or self.css('viewFlowCurvatureFactor')

        if stroke is None:
            if onText == 1:
                stroke = self.css('viewFlowConnectionStroke2', noColor)
            else:
                stroke = self.css('viewFlowConnectionStroke1', noColor)
        if strokeWidth is None:
            strokeWidth = self.css('viewFlowConnectionStrokeWidth', 0.5)

        self.setStrokeColor(stroke, strokeWidth)
        if startMarker:
            if fill is None:
                fill = self.css('viewFlowMarkerFill', noColor)
            self.setFillColor(fill)
            self.context.oval(xs - fms, ys - fms, 2 * fms, 2 * fms)

        xm = (xt + xs)/2
        ym = (yt + ys)/2
        xb1 = xm + onText * (yt - ys) * fmf
        yb1 = ym - onText * (xt - xs) * fmf
        xb2 = xm - onText * (yt - ys) * fmf
        yb2 = ym + onText * (xt - xs) * fmf
        # Arrow head position
        arrowSize = 12
        arrowAngle = 0.4
        angle = atan2(xt-xb2, yt-yb2)
        hookedAngle = radians(degrees(angle)-90)
        ax1 = xt - cos(hookedAngle+arrowAngle) * arrowSize
        ay1 = yt + sin(hookedAngle+arrowAngle) * arrowSize
        ax2 = xt - cos(hookedAngle-arrowAngle) * arrowSize
        ay2 = yt + sin(hookedAngle-arrowAngle) * arrowSize

        b = self.b
        b.newPath()
        self.setFillColor(noColor)
        b.moveTo((xs, ys))
        b.curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
        b.drawPath()

        #  Draw the arrow head.
        b.newPath()
        self.setFillColor(stroke)
        self.setStrokeColor(noColor)
        b.moveTo((xt, yt))
        b.lineTo((ax1, ay1))
        b.lineTo((ax2, ay2))
        b.closePath()
        b.drawPath()

        if endMarker:
            self.setFillColor(self.css('viewFlowMarkerFill', noColor))
            b.oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

    #   D R A W I N G  E L E M E N T

    def drawElementFrame(self, e, origin):
        """If e is not a page and the self.showElementFrame == True, then draw
        the frame of the element. If one or more margins > 0, then draw these as
        transparant rectangles instead of frame line."""
        if self.showElementFrame and not e.isPage:
            x = origin[0]
            y = origin[1]
            mt, mr, mb, ml = e.margin
            context = self.context
            context.fill(color(random(), random(), random(), 0.3))
            context.rect(x-ml, y, max(2,ml), e.h)
            context.rect(x+e.w, y, max(1,mr), e.h)
            context.rect(x-ml, y-mb, ml+e.w+mr, max(1,mb))
            context.rect(x-ml, y+e.h, ml+e.w+mr, max(1,mt))

    def drawElementMetaInfo(self, e, origin):
        self.drawElementInfo(e, origin)
        if self.showElementOrigin:
            self.drawElementOrigin(e, origin)

    def drawElementInfo(self, e, origin):
        """For debugging this will make the elements show their info. The css
        flag "showElementOrigin" defines if the origin marker of an element is
        drawn. Collect the (e, origin), so we can later draw all info, after
        the main drawing has been done."""
        if not e.eId in self.elementsNeedingInfo:
            self.elementsNeedingInfo[e.eId] = (e, origin)

    def _drawElementsNeedingInfo(self):
        b = self.b
        context = self.context
        for e, origin in self.elementsNeedingInfo.values():
            p = pointOffset(e.origin, origin)
            p = e._applyScale(self, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            if self.showElementInfo:
                # Draw box with element info.
                bs = context.newString(e.getElementInfoString(), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=color(0.1)))
                tw, th = bs.size
                Pd = 4 # Padding in box and shadow offset.
                tpx = px - Pd/2 # Make info box outdent the element. Keeping shadow on the element top left corner.
                tpy = py + e.h - th - Pd

                # Tiny shadow
                context.fill(color(0.3, 0.3, 0.3, 0.5))
                context.stroke(noColor)
                context.rect(tpx+Pd/2, tpy, tw+2*Pd, th+1.5*Pd)
                # Frame
                context.fill(self.css('viewInfoFill'))
                context.stroke(color(0.3), w=0.25)
                context.rect(tpx, tpy, tw+2.5*Pd, th+1.5*Pd)
                context.text(bs, (tpx+Pd, tpy+th))

            if self.showElementDimensions:
                # TODO: Make separate arrow functio and better positions
                # Draw width and height measures
                context.fill(noColor)
                context.stroke(blackColor, w=pt(0.25))
                S = self.css('viewInfoOriginMarkerSize', pt(5))
                x1, y1, x2, y2 = px + e.left, py + e.bottom, e.right, e.top

                # Horizontal measure
                context.line((x1, y1 - 0.5*S), (x1, y1 - 3.5*S))
                context.line((x2, y1 - 0.5*S), (x2, y1 - 3.5*S))
                context.line((x1, y1 - 2*S), (x2, y1 - 2*S))
                # Arrow heads
                context.line((x1, y1 - 2*S), (x1+S, y1 - 1.5*S))
                context.line((x1, y1 - 2*S), (x1+S, y1 - 2.5*S))
                context.line((x2, y1 - 2*S), (x2-S, y1 - 1.5*S))
                context.line((x2, y1 - 2*S), (x2-S, y1 - 2.5*S))

                bs = context.newString(asFormatted(x2 - x1),
                                       style=dict(font=self.css('viewInfoFont'),
                                                  fontSize=self.css('viewInfoFontSize'),
                                                  leading=self.css('viewInfoLeading'),
                                                  textFill=color(0.1)))
                tw, th = bs.size
                context.text(bs, ((x2 + x1)/2 - tw/2, y1-1.5*S))

                # Vertical measure
                context.line((x2+0.5*S, y1), (x2+3.5*S, y1))
                context.line((x2+0.5*S, y2), (x2+3.5*S, y2))
                context.line((x2+2*S, y1), (x2+2*S, y2))
                # Arrow heads
                context.line((x2+2*S, y2), (x2+2.5*S, y2-S))
                context.line((x2+2*S, y2), (x2+1.5*S, y2-S))
                context.line((x2+2*S, y1), (x2+2.5*S, y1+S))
                context.line((x2+2*S, y1), (x2+1.5*S, y1+S))

                bs = context.newString(asFormatted(y2 - y1), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=0.1))
                tw, th = bs.size
                context.text(bs, (x2+2*S-tw/2, (y2+y1)/2))

            e._restoreScale(self)

    def drawElementOrigin(self, e, origin):
        context = self.context
        px, py, _ = pointOffset(e.origin, origin)

        S = e.css('viewInfoOriginMarkerSize', pt(5))
        # Draw origin of the element
        fill = e.css('viewInfoOriginMarkerFill', noColor)
        stroke = e.css('viewInfoOriginMarkerStroke', blackColor)
        width = e.css('viewInfoOriginMarkerStrokeWidth', pt(0.25))
        context.fill(fill) # Transparant fill, so we can see the marker on dark backgrounds.
        context.stroke(stroke, width)
        context.oval(px-S, py-S, 2*S, 2*S)
        context.line((px-S, py), (px+S, py))
        context.line((px, py-S), (px, py+S))

        if self.showElementDimensions:
            bs = context.newString(e.xy, style=dict(font=self.css('viewInfoFont'),
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'),
                textFill=color(0.1)))
            w, h = bs.size
            context.text(bs, (px - w/2, py + S*1.5))

    def drawMissingElementRect(self, e, origin):
        """When designing templates and pages, this will draw a filled
        rectangle on the element bounding box (if self.css('missingElementFill'
        is defined) and a cross, indicating that this element has missing
        content (as in unused image frames). Only draw if the list self.showGrid
        contains proper types of grid names.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showMissingElementRect = True
        >>> view.drawMissingElementRect(e, (0, 0))
        """
        context = self.context

        if self.showMissingElementRect:

            p = pointOffset(e.origin, origin)
            p = self._applyScale(e, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

            context.saveGraphicState()
            context.setShadow(self.shadow)

            sMissingElementFill = self.css('viewMissingElementFill', noColor)
            if sMissingElementFill is not noColor:
                context.fill(sMissingElementFill)
                context.stroke(noColor)
                context.rect(px, py, self.w, self.h)
            # Draw crossed rectangle.
            context.fill(noColor)
            context.stroke(blackColor, pt(0.5))
            context.rect(px, py, self.w, self.h)
            context.newPath()
            context.moveTo((px, py))
            context.lineTo((px + self.w, py + self.h))
            context.moveTo((px + self.w, py))
            context.lineTo((px, py + self.h))
            context.drawPath()

            context.restoreGraphicState()
            e._restoreScale(self)

    #    G R I D

    def drawGrid(self, e, origin, showGrid):
        """Draw grid of lines and/or rectangles if colors are set in the style.
        Normally origin is ORIGIN pt(0, 0, 0), but it's possible to give the grid
        a fixed offset.
        If view flag self.showGrid is set, display the type of grid (GRID_COL, GRID_ROW, GRID_SQR)

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawGrid(e, (0, 0), view.showGrid)
        >>> view.showGridBackground = [GRID_COL]
        >>> view.drawGrid(e, (0, 0), view.showGridBackground)
        """
        context = self.context

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        # Drawing the grid as horizontal lines.
        if GRID_COL in showGrid:
            # Set color for vertical grid lines
            context.fill(noColor)
            gridStrokeColor = e.css('viewGridStrokeY', noColor)
            gridStrokeWidth = e.css('viewGridStrokeWidthY', blackColor)
            context.stroke(gridStrokeColor, gridStrokeWidth)

            x = e.pl # Position on right padding of page/e
            gridX = e.gridX
            if gridX:
                for cw in gridX:
                    if isinstance(cw, (tuple, list)):
                        cw, gx = cw
                    context.line((px+x, py), (px+x, py+e.h))
                    if gx:
                        context.line((px+x+cw, py), (px+x+cw, py+e.h))
                    x += cw + gx

        # Drawing the grid as vertical lines.
        if GRID_ROW in showGrid:
            # Set color for vertical grid lines
            context.fill(noColor)
            gridStrokeColor = e.css('viewGridStrokeX', noColor)
            gridStrokeWidth = e.css('viewGridStrokeWidthX', blackColor)
            context.stroke(gridStrokeColor, gridStrokeWidth)

            y = e.pb # Position on bottom padding of page/e
            gridY = e.gridY
            if gridY:
                for ch in gridY:
                    if isinstance(ch, (tuple, list)):
                        ch, gy = ch
                    context.line((px, py+y), (px+e.w, py+y))
                    if gy:
                        context.line((px, py+y+ch), (px+e.w, py+y+ch))
                    y += ch + gy

        # Drawing the grid as rectangles.
        if GRID_SQR in showGrid:
            # Set color for grid rectangles
            context.fill(e.css('viewGridFill', noColor))
            context.stroke(e.css('viewGridStroke', noColor))

            gridX = e.gridX
            gridY = e.gridY
            if gridX and gridY:
                x = e.pl # Position on right padding of page/e
                for cw in gridX:
                    if isinstance(cw, (tuple, list)):
                        cw, gx = cw
                    else:
                        gx = 0
                    y = e.pb # Position on bottom padding of page/e
                    for ch in gridY:
                        if isinstance(ch, (tuple, list)):
                            ch, gy = ch
                        else:
                            gy = 0
                        context.rect(px+x, py+y, cw, ch)
                        y += ch + gy
                    x += cw + gx

    def drawBaselineGrid(self, e, origin):
        """Draw baseline grid if self.showBaselineGrid is True and there is a
        baseline defined > 0. Use the color from style values viewGridStrokeX and 
        viewGridStrokeWidthX to make a difference with the baselines drawn by TextBox 
        with style values baselineColor and baselineWidth.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showBaselineGrid = [GRID_LINE, GRID_INDEX, GRID_Y]
        >>> view.drawBaselineGrid(e, pt(0, 0))
        """
        show = self.showBaselineGrid

        # Sets the default, in case not drawing or show is True
        if not show:
            return
        if not isinstance(show, (set, list, tuple)):
            show = [GRID_LINE, GRID_INDEX] # Default is to show all, if set to True
        elif not GRID_LINE in show:
            return # Not showing the grid

        context = self.context

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        baselineGrid = e.baselineGrid # Get the baseline grid of this element.
        indexFontSize = max(9, min(16, baselineGrid*0.5)) # Index size depends on baseline.
        indexGutter = baselineGrid/4 # Gutter between index marker and element padding

        startY = e.baselineGridStart
        if startY is None:
            startY = e.pt # Otherwise use the top padding as start Y.
        oy = e.h - startY # Assumes origin at bottom for context drawing.

        line = 0 # Line index
        baselineColor = e.css('viewBaselineGridStroke', color(0,7))
        baselineWidth = e.css('viewBaselineGridWidth', 0.5)

        # Format of line numbers.
        style = dict(font=e.css('fallbackFont','Arial'), xTextAlign=RIGHT,
            fontSize=indexFontSize, stroke=noColor, textFill=baselineColor)
        context.fill(noColor)
        context.stroke(baselineColor, baselineWidth)

        while oy > e.pb: # Run until the padding of the element is reached.
            context.line((px + e.pl, py + oy), (px + e.w - e.pr, py + oy))
            if GRID_INDEX or GRID_Y in show:
                if GRID_INDEX in show: # Shows line baseline index
                    t = repr(line)
                else: # GRID_Y show vertical position marker
                    t = repr(e.h - oy)
                bs = context.newString(t, style=style)
                tw, th = bs.size
                context.text(bs, (px + e.pl - tw - indexGutter, py + oy - th/4))
                context.text(bs, (px + e.pl + e.pw + indexGutter, py + oy - th/4))
                line += 1 # Increment line index.
            oy -= baselineGrid # Next vertical line position of baseline grid.

    #    M A R K E R S

    def _drawPageRegistrationMark(self, page, origin, cmSize, cmStrokeWidth, vertical):
        """Draw registration mark as position x, y."""
        context = page.context
        x, y = origin
        if vertical:
            dx = cmSize/2
            dy = cmSize
        else:
            dx = cmSize
            dy = cmSize/2
        context.fill(noColor)
        context.stroke(color(c=1, m=1, y=1, k=1), w=cmStrokeWidth)
        context.newPath()
        # Registration circle
        context.circle(x, y, cmSize/4)
        # Registration cross, in length of direction.
        context.moveTo((x - dx, y)) # Horizontal line.
        context.lineTo((x + dx, y))
        context.moveTo((x, y + dy)) # Vertical line.
        context.lineTo((x, y - dy))
        context.drawPath()

    def drawPageRegistrationMarks(self, page, origin):
        """Draw standard registration mark, to show registration of CMYK colors.
        https://en.wikipedia.org/wiki/Printing_registration.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element() # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPageRegistrationMarks = True
        >>> view.drawPageRegistrationMarks(e, pt(0, 0))
        """
        if self.showPageRegistrationMarks:
            cmSize = min(self.pl/2, self.css('viewCropMarkSize')) # TODO: Make cropmark go closer to page edge and disappear if too small.
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')
            x, y = point2D(origin)
            w, h = page.size
            self._drawPageRegistrationMark(page, (x + w/2, y - cmSize), cmSize, cmStrokeWidth, False) # Bottom registration mark
            self._drawPageRegistrationMark(page, (x - cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Left registration mark
            self._drawPageRegistrationMark(page, (x + w + cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Right registration mark
            self._drawPageRegistrationMark(page, (x + w/2, y + h + cmSize), cmSize, cmStrokeWidth, False) # Top registration mark

    def drawPageCropMarks(self, e, origin):
        """If the show flag is set, then draw the cropmarks or page frame.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element()
        >>> view = PageView(context=context, style=style)
        >>> view.showPageCropMarks = True
        >>> view.drawPageCropMarks(e, pt(0, 0))
        """
        if self.showPageCropMarks:
            context = self.context

            x, y = point2D(origin) # Ignore z-axus for now.
            w, h = e.size
            folds = self.css('folds')
            cmDistance = self.css('viewCropMarkDistance') # From the side
            cmSize = min(self.css('viewCropMarkSize', pt(32)), self.pl)
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')

            context.fill(noColor)
            context.stroke(color(cmyk=1), w=cmStrokeWidth)
            # Bottom left
            context.line((x - cmDistance, y), (x - cmSize, y))
            context.line((x, y - cmDistance), (x, y - cmSize))
            # Bottom right
            context.line((x + w + cmDistance, y), (x + w + cmSize, y))
            context.line((x + w, y - cmDistance), (x + w, y - cmSize))
            # Top left
            context.line((x - cmDistance, y + h), (x - cmSize, y + h))
            context.line((x, y + h + cmDistance), (x, y + h + cmSize))
            # Top right
            context.line((x + w + cmDistance, y + h), (x + w + cmSize, y + h))
            context.line((x + w, y + h + cmDistance), (x + w, y + h + cmSize))
            # Any fold lines to draw?
            if folds is not None:
                for fx, fy in folds:
                    if fx is not None:
                        context.line((x + fx, y - cmDistance), (x + fx, y - cmSize))
                        context.line((x + fx, y + h + cmDistance), (x + fx, y + h + cmSize))
                    if fy is not None:
                        context.line((x - cmDistance, y + fy), (x - cmSize, y + fy))
                        context.line((x + w + cmDistance, y + fy), (x + w + cmSize, y + fy))

    #   D R A W B O T  S U P P O R T

    # The context-methods are used, in case the view itself is placed in a layout.

    def build_drawBot(self, view, origin):
        """This method is called if the view is used as a placable element
        inside another element, such as a Page or Template. """
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        self.drawElementFrame(view, p)
        for page in self.elements:
            self.drawPageMetaInfo(page, p)
            page.build(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        #view.drawElementMetaInfo(self, origin)

    build_flat = build_drawBot

    def build_html(self, view, origin):
        """HTML page view to be implemented. Ignore for now."""
        pass

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
