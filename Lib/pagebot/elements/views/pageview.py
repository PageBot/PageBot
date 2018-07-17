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
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     pageview.py
#
from __future__ import division

import os
from random import random
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from pagebot.toolbox.color import color, noColor, grayColor
from pagebot.elements.views.baseview import BaseView
from pagebot.style import RIGHT
from pagebot.constants import ORIGIN
from pagebot.toolbox.units import pt, pointOffset, point3D
from pagebot.toolbox.transformer import *

class PageView(BaseView):
    u"""The PageView is contains the parameters to export the pages as documents.
    A View is just another kind of container, kept by document to make a certain presentation
    of the page tree. Views use the current Context.b builder for export."""
    viewId = 'Page'

    MIN_PADDING = 20 # Minimum padding needed to show meta info. Otherwise truncated to 0 and not showing meta info.
    EXPORT_PATH = '_export/' # Default path for local document export, that does not commit documents to Github.

    def build(self, path=None, pageSelection=None, multiPage=True):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw.

        >>> view = PageView(name='MyPageView')
        >>> view.w, view.h, view.name # Size is initialze to default.
        (100pt, 100pt, 'MyPageView')
        >>> #str(view.context) in ('<DrawBotContext>' or '<FlatContext>')
        """
        if not path:
            path = self.EXPORT_PATH + self.doc.name + '.pdf' # Default export as PDF.
        # If default _export directory does not exist, then create it.
        if path.startswith(self.EXPORT_PATH) and not os.path.exists(self.EXPORT_PATH):
            os.makedirs(self.EXPORT_PATH)

        context = self.context # Get current context and builder from doc. Can be DrawBot or Flat

        # Save the intended extension into the context, so it knows what we'll be saving to.
        context.fileType = path.split('.')[-1]

        # Find the maximum document page size to this in all page sizes of the document.
        w, h, _ = self.doc.getMaxPageSizes(pageSelection)

        # Make sure that canvas is empty, there may have been another document building in this context.
        context.newDrawing()

        context.newDocument(w, h) # Allow the context to create a new document and page canvas.
        for pn, pages in self.doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue

            # TODO: Some options here for layout of the combined pages, depending on the spread view option.
            # self.showSpreadPages # Show even/odd pages as spread, as well as pages that share the same pagenumber.
            # self.showSpreadMiddleAsGap # Show the spread with single crop marks. False glues pages togethers as in real spread.

            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            page = pages[0] # TODO: make this work for pages that share the same page number
            pw, ph = w, h  # Copy from main (w, h), since they may be altered.

            if self.pl > self.MIN_PADDING and \
               self.pt > self.MIN_PADDING and \
               self.pb > self.MIN_PADDING and \
               self.pr > self.MIN_PADDING:
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

            # View may have defined a background
            fillColor = self.style.get('fill', noColor)
            if fillColor is not noColor:
                context.setFillColor(fillColor)
                context.rect(pt(0), pt(0), pw, ph)

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(page, self, origin)

            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            # Recursively call all elements in the tree to build themselves.
            # Note that is independent from the context. If there is a difference, the elements should
            # make the switch themselves.
            page.buildChildElements(self, origin)

            self.drawPageMetaInfo(page, origin)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(page, self, origin)

            # Self.infoElements now may have collected elements needed info to be drawn, after all drawing is done.
            # So the info boxes don't get covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo()

        u"""Export the document to fileName for all pages in sequential order.
        If pageSelection is defined, it must be a list with page numbers to
        export. This allows the order to be changed and pages to be omitted.
        The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct
        the type of drawing and export that needs to be done.

        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in
        special cases, there is not straighforward (or sequential) export of
        pages, e.g. when generating HTML/CSS. In that case use
        MyBuilder(document).export(fileName), the builder is responsible to
        query the document, pages, elements and styles.
        """

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

    def drawPageMetaInfo(self, page, origin):
        u"""Draw the meta info of the page, depending on the settings of the flags.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=context)
        >>> page = doc[1]
        >>> view = doc.getView()
        >>> view.showGrid = True
        >>> view.drawPageMetaInfo(page, (0, 0))
        """
        self.drawPageFrame(page, origin)
        self.drawPagePadding(page, origin)
        self.drawPageNameInfo(page, origin)
        self.drawPageRegistrationMarks(page, origin)
        self.drawPageCropMarks(page, origin)
        self.drawGrid(page, origin)
        self.drawBaselineGrid(page, origin)

    def drawPageFrame(self, page, origin):
        u"""Draw the page frame if the the flag is on and  if there ie padding enough to show other meta info.
        Otherwise the padding is truncated to 0: no use to draw the frame.

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
                self.pl > self.MIN_PADDING and self.pr > self.MIN_PADDING and \
                self.pt > self.MIN_PADDING and self.pb > self.MIN_PADDING:
            context = self.context
            context.setFillColor(noColor)
            context.setStrokeColor(color(0, 0, 1), 0.5)
            context.rect(origin[0], origin[1], page.w, page.h)
            #page.drawFrame(origin, self)

    def drawPagePadding(self, page, origin):
        u"""Draw the page frame of its current padding.

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

            p = pointOffset(page.oPoint, origin)
            p = page._applyScale(self, p)
            px, py, _ = page._applyAlignment(p) # Ignore z-axis for now.

            context.setFillColor(noColor)
            context.setStrokeColor(self.css('viewPagePaddingStroke', color(0.2, 0.2, 1)),
                                   self.css('viewPagePaddingStrokeWidth', 0.5))
            if page.originTop:
                pass
                #context.rect(px+pl, py+page.h-pb, page.w-pl-pr, page.h-pt-pb)
            else:
                context.rect(px+pl, py+pb, page.w-pl-pr, page.h-pt-pb)
            page._restoreScale(self)

    def drawPageNameInfo(self, page, origin):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPageNameInfo = True
        >>> view.drawPageNameInfo(e, (0, 0))
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
            if page.name:
                s += ' | ' + page.name
            bs = context.newString(s, style=dict(font=self.css('viewPageNameFont'), textFill=color(0), fontSize=fontSize))
            self.context.text(bs, (self.pl + cmDistance, self.pb + page.h + cmSize - fontSize*2)) # Draw on top of page.

    #   D R A W I N G  F L O W S

    def drawFlowConnections(self, e, origin, b):
        u"""If rootStyle.showFlowConnections is True, then draw the flow connections
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
            fill=None, stroke=None, strokeWidth=None):
        u"""Draw curved arrow marker between the two points.
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
        u"""If e is not a page and the self.showElementFrame == True, then draw
        the frame of the element. If one or more margins > 0, then draw these as
        transparant rectangles instead of frame line."""
        if self.showElementFrame and not e.isPage:
            x = origin[0]
            y = origin[1]
            mt, mr, mb, ml = e.margin
            context = self.context
            context.setFillColor(color(random(), random(), random(), 0.3))
            context.rect(x-ml, y, max(2,ml), e.h)
            context.rect(x+e.w, y, max(1,mr), e.h)
            context.rect(x-ml, y-mb, ml+e.w+mr, max(1,mb))
            context.rect(x-ml, y+e.h, ml+e.w+mr, max(1,mt))

    def drawElementMetaInfo(self, e, origin):
        self.drawElementInfo(e, origin)
        self.drawElementOrigin(e, origin)

    def drawElementInfo(self, e, origin):
        u"""For debugging this will make the elements show their info. The css flag "showElementOrigin"
        defines if the origin marker of an element is drawn. Collect the (e, origin), so we can later
        draw all info, after the main drawing has been done.
        """
        if not e.eId in self.elementsNeedingInfo:
            self.elementsNeedingInfo[e.eId] = (e, origin)

    def _drawElementsNeedingInfo(self):
        b = self.b
        context = self.context
        for e, origin in self.elementsNeedingInfo.values():
            p = pointOffset(e.oPoint, origin)
            p = e._applyScale(self, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            if self.showElementInfo:
                # Draw box with element info.
                bs = context.newString(e.getElementInfoString(), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=color(0.1)))
                tw, th = context.textSize(bs)
                Pd = 4 # Padding in box and shadow offset.
                tpx = px - Pd/2 # Make info box outdent the element. Keeping shadow on the element top left corner.
                tpy = py + e.h - th - Pd

                # Tiny shadow
                context.setFillColor(color(0.3, 0.3, 0.3, 0.5))
                context.setStrokeColor(noColor)
                b.rect(tpx+Pd/2, tpy, tw+2*Pd, th+1.5*Pd)
                # Frame
                context.setFillColor(self.css('viewInfoFill'))
                context.setStrokeColor(color(0.3), w=0.25)
                b.rect(tpx, tpy, tw+2.5*Pd, th+1.5*Pd)
                b.text(fs, (tpx+Pd, tpy+th))

            if self.showElementDimensions:
                # TODO: Make separate arrow functio and better positions
                # Draw width and height measures
                context.setFillColor(noColor)
                context.setStrokeColor(color(0), w=0.25)
                S = self.css('viewInfoOriginMarkerSize', 4)
                x1, y1, x2, y2 = px + e.left, py + e.bottom, e.right, e.top

                # Horizontal measure
                b.line((x1, y1 - 0.5*S), (x1, y1 - 3.5*S))
                b.line((x2, y1 - 0.5*S), (x2, y1 - 3.5*S))
                b.line((x1, y1 - 2*S), (x2, y1 - 2*S))
                # Arrow heads
                b.line((x1, y1 - 2*S), (x1+S, y1 - 1.5*S))
                b.line((x1, y1 - 2*S), (x1+S, y1 - 2.5*S))
                b.line((x2, y1 - 2*S), (x2-S, y1 - 1.5*S))
                b.line((x2, y1 - 2*S), (x2-S, y1 - 2.5*S))

                fs = context.newString(asFormatted(x2 - x1),
                                       style=dict(font=self.css('viewInfoFont'),
                                                  fontSize=self.css('viewInfoFontSize'),
                                                  leading=self.css('viewInfoLeading'),
                                                  textFill=color(0.1)))
                tw, th = b.textSize(fs.s)
                b.text(fs, ((x2 + x1)/2 - tw/2, y1-1.5*S))

                # Vertical measure
                b.line((x2+0.5*S, y1), (x2+3.5*S, y1))
                b.line((x2+0.5*S, y2), (x2+3.5*S, y2))
                b.line((x2+2*S, y1), (x2+2*S, y2))
                # Arrow heads
                b.line((x2+2*S, y2), (x2+2.5*S, y2-S))
                b.line((x2+2*S, y2), (x2+1.5*S, y2-S))
                b.line((x2+2*S, y1), (x2+2.5*S, y1+S))
                b.line((x2+2*S, y1), (x2+1.5*S, y1+S))

                bs = context.newString(asFormatted(y2 - y1), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=color(0.1)))
                tw, th = context.textSize(bs)
                b.text(fs, (x2+2*S-tw/2, (y2+y1)/2))

            e._restoreScale(self)

    def drawElementOrigin(self, e, origin):
        context = self.context
        px, py, _ = pointOffset(e.oPoint, origin)
        S = self.css('viewInfoOriginMarkerSize', 4)
        if self.showElementOrigin:
            # Draw origin of the element
            context.setFillColor(color(0.5, 0.5, 0.5, 0.1)) # Transparant fill, so we can see the marker on dark backgrounds.
            context.setStrokeColor(color(0), 0.25)
            context.oval(px-S, py-S, 2*S, 2*S)
            context.line((px-S, py), (px+S, py))
            context.line((px, py-S), (px, py+S))

        if self.showElementDimensions:
            bs = context.newString(point2S(e.point3D), style=dict(font=self.css('viewInfoFont'),
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=color(0.1)))
            w, h = context.textSize(bs)
            context.text(bs, (px - w/2, py + S*1.5))

    def drawMissingElementRect(self, e, origin):
        u"""When designing templates and pages, this will draw a filled rectangle on the element
        bounding box (if self.css('missingElementFill' is defined) and a cross, indicating
        that this element has missing content (as in unused image frames).
        Only draw if self.css('showGrid') is True.

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

            p = pointOffset(e.oPoint, origin)
            p = self._applyScale(e, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

            context.saveGraphicState()
            context.setShadow(self.shadow)

            sMissingElementFill = self.css('viewMissingElementFill', noColor)
            if sMissingElementFill is not noColor:
                context.setFillColor(sMissingElementFill)
                context.setStrokeColor(noColor)
                context.rect(px, py, self.w, self.h)
            # Draw crossed rectangle.
            context.setFillColor(noColor)
            context.setStrokeColor(color(0), pt(0.5))
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

    def drawGrid(self, e, origin):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showGrid = True
        >>> view.drawGrid(e, (0, 0))
        """
        return
        # TODO: Make grid work from grid style
        """
        # Drawing the grid as squares.
        if not self.showGrid:
            return
        #if not self.showGridColumns or not self.showGrid:
        #    return
        context = self.context

        p = pointOffset(e.oPoint, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        gridFillColor = e.css('viewGridFill', noColor)
        gutterW = e.gw # Gutter width
        gutterH = e.gh # Gutter height
        columnWidth = e.cw # Column width
        columnHeight = e.ch # Column height
        pt, pr, pb, pl = e.padding # Padding top, right, bottom, left
        pw = e.pw # Padding width, space between paddingLeft and paddingRight
        ph = e.ph # Padding height, space between paddingTop and paddingBottom

        w = e.w
        h = e.h

        if e.isRightPage():
            ox = px + pr
        else:
            ox = px + pl
        oy = py + pb

        if self.showGrid:
            if gridFillColor != noColor:
                context.fill(gridFillColor)
                context.stroke(noColor)
                for cx, cw in e.getGridColumns():
                    for cy, ch in e.getGridRows():
                        context.rect(ox+cx, oy+cy, cw, ch)

            gridStrokeColor = self.css('viewGridStroke', noColor)
            gridStrokeWidth = self.css('viewGridStrokeWidth', color(0))
            if gridStrokeColor != noColor and gridStrokeWidth:
                context.fill(noColor)
                context.stroke(gridStrokeColor, gridStrokeWidth)
                context.newPath()
                for cx, cw in e.getGridColumns():
                    context.moveTo((ox+cx, oy))
                    context.lineTo((ox+cx, oy + ph))
                    context.moveTo((ox+cx+cw, oy))
                    context.lineTo((ox+cx+cw, oy + ph))
                for cy, ch in e.getGridRows():
                    context.moveTo((ox, oy+cy))
                    context.lineTo((ox+pw, oy+cy))
                    context.moveTo((ox, oy+cy + ch))
                    context.lineTo((ox+pw, oy+cy + ch))
                context.drawPath()
                #text(fs+repr(index), (ox + M * 0.3, oy + M / 4))
        """
        
    def drawBaselineGrid(self, e, origin):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showBaselineGrid = True
        >>> view.drawBaselineGrid(e, pt(0, 0))
        """
        if not self.showBaselineGrid:
            return
        b = self.b
        context = self.context
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(e, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        M = pt(16)
        startY = e.css('baselineGridStart')
        if startY is None:
            startY = e.pt # Otherwise use the top padding as start Y.
        oy = e.h - startY#- py
        line = 0
        # Format of line numbers.
        # TODO: DrawBot align and fill don't work properly now.
        style = dict(font=e.css('fallbackFont','Verdana'), xTextAlign=RIGHT,
            fontSize=M/2, stroke=noColor, 
            textFill=e.css('viewGridStroke', grayColor))
        baselineGrid = e.css('baselineGrid', )
        while oy > e.pb or 0:
            context.setFillColor(noColor)
            context.setStrokeColor(e.css('baselineGridStroke', grayColor), e.css('gridStrokeWidth'))
            context.newPath()
            context.moveTo((px + e.pl, py + oy))
            context.lineTo((px + e.w - e.pr, py + oy))
            context.drawPath()
            bs = context.newString(repr(line), e=self, style=style)
            context.text(bs, (px + e.pl - 2, py + oy - e.pl * 0.6))
            context.text(bs, (px + e.w - e.pr - 8, py + oy - e.pr * 0.6))
            line += 1 # Increment line index.
            oy -= e.css('baselineGrid') # Next vertical line position of baseline grid.

    #    M A R K E R S

    def _drawPageRegistrationMark(self, page, origin, cmSize, cmStrokeWidth, vertical):
        u"""Draw registration mark as position x, y."""
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
        u"""Draw standard registration mark, to show registration of CMYK colors.
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
            x, y, _ = point3D(origin)
            w, h = page.w, page.h
            self._drawPageRegistrationMark(page, (x + w/2, y - cmSize), cmSize, cmStrokeWidth, False) # Bottom registration mark
            self._drawPageRegistrationMark(page, (x - cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Left registration mark
            self._drawPageRegistrationMark(page, (x + w + cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Right registration mark
            self._drawPageRegistrationMark(page, (x + w/2, y + h + cmSize), cmSize, cmStrokeWidth, False) # Top registration mark

    def drawPageCropMarks(self, e, origin):
        u"""If the show flag is set, then draw the cropmarks or page frame.

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

            x, y, _ = point3D(origin) # Ignore z-axus for now.
            w, h = e.w, e.h
            folds = self.css('folds')
            cmDistance = self.css('viewCropMarkDistance') # From the side
            cmSize = min(self.css('viewCropMarkSize', pt(32)), self.pl)
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')

            context.setFillColor(noColor)
            context.setStrokeColor(color(cmyk=1), w=cmStrokeWidth)
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
        u"""This method is called if the view is used as a placable element inside
        another element, such as a Page or Template. """
        p = pointOffset(self.oPoint, origin)
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
        u"""HTML page view to be implemented. Ignore for now."""
        pass

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
