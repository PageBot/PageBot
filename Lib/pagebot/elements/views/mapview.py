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
#     mapview.py
#
#     Show an overview of thumbnails for everypage in the document

import os
from random import random
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from pagebot.filepaths import getResourcesPath
from pagebot.toolbox.color import color, noColor, blackColor, registrationColor
from pagebot.elements.views.baseview import BaseView
from pagebot.constants import (ORIGIN, GRID_COL, GRID_ROW, GRID_SQR,
        GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG, BASE_LINE, BASE_LINE_BG,
        BASE_INDEX_LEFT, BASE_Y_LEFT, BASE_INDEX_RIGHT, BASE_Y_RIGHT,
        BASE_INSIDE, RIGHT, ECI_GrayConL, COLORBAR_LEFT, COLORBAR_RIGHT)
from pagebot.toolbox.units import pt, pointOffset, point2D, asFormatted
from pagebot.toolbox.transformer import *

class MapView(BaseView):
    """The MapView contains the set of Quire instances to export the pages
    as documents. A View is just another kind of container, kept by a Document
    to make a certain presentation of the page tree. The MapView typically
    holds Quire elements that make one-directional links to document pages in
    order to compose them in spreads or folding compositions."""
    viewId = 'Page'

    EXPORT_PATH = '_export/' # Default path for local document export, that does not commit documents to Github.

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """Draw the selected pages. pageSelection is an optional set of
        y-pageNumbers to draw.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BusinessCard, A4, QUIRE_QUARTO
        >>> doc = Document(size=A4, autoPages=4) # Make 4 pages to be composed as a Quire of 2 spreads
        >>> view = doc.view
        >>> q1 = view.newQuire(folds=QUIRE_QUARTO)
        >>> q2 = view.newQuire(folds=QUIRE_QUARTO)
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

        # Save the intended extension into the context, so it knows what we'll
        # be saving to.
        self.context.fileType = path.split('.')[-1]

        # Find the maximum document page size to this in all page sizes of the
        # document.
        w, h, _ = self.doc.getMaxPageSizes(pageSelection)

        # Make sure that canvas is empty, there may have been another document
        # building in this context.
        self.context.newPage(w=w, h=h, doc=self.doc)

        for pn, pages in self.doc.getSortedPages():
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue

            # Create a new DrawBot viewport page to draw template + page, if
            # not already done. In case the document is oversized, then make
            # all pages the size of the document, so the pages can draw their
            # crop-marks. Otherwise make DrawBot pages of the size of each
            # page. Size depends on the size of the larges pages + optional
            # decument padding.
            # TODO: make this work for pages that share the same page number.
            page = pages[0]
            # Copy from main (w, h), since they may be altered, from the
            # orgiinal document size.
            pw, ph = w, h

            if self.pl >= self.viewMinInfoPadding and \
               self.pt >= self.viewMinInfoPadding and \
               self.pb >= self.viewMinInfoPadding and \
               self.pr >= self.viewMinInfoPadding:
                pw += self.pl + self.pr
                ph += self.pt + self.pb
                origin = self.pl, self.pb, pt(0)
            else:
                pw = page.w # No padding defined, follow the size of the page.
                ph = page.h
                origin = ORIGIN

            #  Make page in context, actual page may be smaller if showing
            #  cropmarks.
            self.context.newPage(pw, ph)
            # If page['frameDuration'] is set and saving as movie or animated
            # gif, then set the global frame duration.
            # Set the duration of this page, in case exporting GIF.
            self.context.frameDuration(page.frameDuration)

            # View may have a background defined. Build with page bleed, if it
            # is defined.
            fillColor = self.style.get('fill', noColor)

            if fillColor is not noColor:
                bt, br, bb, bl = page.bleed
                self.context.fill(fillColor)
                self.context.rect(page.bleedLeft, page.bleedBottom, pw+br+bl, ph+bt+bb)

            self.drawPageMetaInfo(page, origin, background=True)

            # Because self already adjusts origin, scale, etc. we don't use the
            # page.build here. Instead we call the drawing of its elements as
            # well.
            page.buildChildElements(self, origin)

            self.drawPageMetaInfo(page, origin, background=False)

            # Self.infoElements now may have collected elements needed info to
            # be drawn after all drawing is done, so the info boxes don't get
            # covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo(e)

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

        self.context.saveDrawing(path, multiPage=multiPage)

    #   D R A W B O T  S U P P O R T

    # The context-methods are used in case the view itself is placed in a layout.

    def build_drawBot(self, view, origin, **kwargs):
        """This method is called if the view is used as a placable element
        inside another element, such as a Page or Template. """
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        self.drawElementFrame(view, p) # In case the view itself is used on a page.
        for page in self.elements:
            page.build(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        #view.drawElementInfo(self, origin)

    build_flat = build_drawBot

    def build_html(self, view, origin, **kwargs):
        """HTML page view to be implemented. Ignore for now."""


    #   D R A W I N G.

    def drawPageMetaInfo(self, page, origin, path=None, background=False):
        """Draws the foreground meta info of the page, depending on the settings
        of the flags.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> path = '_export/PageMetaInfo.pdf'
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=context)
        >>> page = doc[1]
        >>> view = doc.getView()
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawPageMetaInfo(page, (0, 0), path)
        """
        if not background:
            self.drawFrame(page, origin)
            self.drawPadding(page, origin)
            # Use path to show file name in page meta info.
            self.drawNameInfo(page, origin, path)
            # Color bars under registration marks?
            self.drawColorBars(page, origin)
            self.drawRegistrationMarks(page, origin)
            self.drawCropMarks(page, origin)
            self.drawElementOrigin(page, origin)
        self.drawGrid(page, origin, background=background)
        self.drawBaselines(page, origin, background=background)
        self.drawFlowConnections(page, origin)

    def drawFrame(self, e, origin):
        """Draws the page frame if the the flag is on and if there is enough
        padding to show other meta info. Otherwise the padding is truncated to
        0: no use to draw the frame.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showFrame = True
        >>> view.drawFrame(e, (0, 0))

        """
        if ((self.showFrame and e.isPage) or e.showFrame) and \
                self.pl >= self.viewMinInfoPadding and self.pr >= self.viewMinInfoPadding and \
                self.pt >= self.viewMinInfoPadding and self.pb >= self.viewMinInfoPadding:
            self.context.fill(noColor)
            self.context.stroke(color(0, 0, 1), pt(0.5))
            self.context.rect(origin[0], origin[1], e.w, e.h)

    def drawPadding(self, e, origin):
        """Draw the page frame of its current padding.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showFrame = True
        >>> view.drawFrame(e, (0, 0))
        """
        pt, pr, pb, pl = e.padding
        if ((self.showPadding and e.isPage) or e.showPadding) and (pt or pr or pb or pl):
            p = pointOffset(e.origin, origin)
            p = e._applyScale(self, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            self.context.fill(noColor)
            self.context.stroke(self.css('viewPaddingStroke', color(0.2, 0.2, 1)),
                                   self.css('viewPaddingStrokeWidth', 0.5))
            self.context.rect(px+pl, py+pb, e.w-pl-pr, e.h-pt-pb)
            e._restoreScale(self)

    def drawNameInfo(self, e, origin, path):
        """Draws additional document information, color markers, page number,
        date, version, etc. outside the page frame, if drawing crop marks.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> path = '_export/PageNameInfo.pdf'
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showNameInfo = True
        >>> view.drawNameInfo(e, (0, 0), path)
        """
        if (self.showNameInfo and e.isPage) or e.showNameInfo:
            # Position of text is based on crop mark size.
            cmDistance = self.css('viewCropMarkDistance')
            cmSize = self.css('viewCropMarkSize') - cmDistance
            fontSize = self.css('viewNameFontSize')
            dt = datetime.datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            # Test if there is a document.
            if e.isPage and e.parent is not None:
                pn = e.parent.getPageNumber(e)
                # First or only page on this page number, then just show pn[0].
                if pn[1] == 0:
                    pn = pn[0]

                # More than one page, then show total.
                if len(e.parent.pages) > 1:
                    pn = '%s/%d' % (pn, len(e.parent.pages))

                title = e.parent.title or 'Untitled'
                s = 'Page %s | %s | %s' % (pn, d, title)
            # Otherwise always page number #1.
            else:
                pn = 1
                title = 'Untitled'
                s = 'Element %s | %s' % (d, title)
            if e.name and e.name != 'default':
                s += ' | ' + e.name
            if path is not None:
                # We're only interested in the file name.
                s += ' | ' + path.split('/')[-1]
            bs = self.context.newString(s, style=dict(font=self.css('viewNameFont'),
                textFill=blackColor, fontSize=fontSize))
            # Draw on top of page.
            self.context.text(bs, (self.pl + cmDistance,
                self.pb + e.h + cmSize - fontSize*2))


    def drawFlowConnections(self, e, origin):
        """If rootStyle.showFlowConnections is True, draw the flow connections
        on the page, using their stroke / width settings of the style."""
        px, py, _ = pointOffset(self.point, origin) # Ignore z-axis for now.
        if (self.showFlowConnections and e.isPage) or e.showFlowConnections:
            for seq in e.getFlows().values():
                # For all the flow sequences found in the page, draw flow
                # arrows at offset (ox, oy).
                tbStart = e.getElement(seq[0].eId)
                startX = tbStart.x
                startY = tbStart.y
                for tbTarget in seq[1:]:
                    tbTarget = e.getElement(tbTarget.eId)
                    targetX = tbTarget.x
                    targetY = tbTarget.y
                    self.drawArrow(e, px+startX, py+startY+tbStart.h,
                            px+startX+tbStart.w, py+startY, -1)
                    self.drawArrow(e, px+startX+tbStart.w,
                            py+startY, px+targetX, py+targetY+tbTarget.h, 1)
                    tbStart = tbTarget
                    startX = targetX
                    startY = targetY
                self.drawArrow(e, px+startX, py+startY+tbStart.h,
                        px+startX+tbStart.w, py+startY, -1)

                if e != e.parent.getLastPage():
                    # Finalize with a line to the start, assuming it is on the
                    # next page.
                    tbTarget = e.getElement(seq[0].eId)
                    self.drawArrow(e, px+startX+tbStart.w, py+startY,
                            px+tbTarget.x, py+tbTarget.y+tbTarget.h-e.h, 1)

    def drawArrow(self, e, xs, ys, xt, yt, onText=1, startMarker=False,
            endMarker=False, fms=None, fmf=None, fill=noColor, stroke=noColor,
            strokeWidth=None):
        """Draw curved arrow marker between the two points.

        TODO: Add drawing of real arrow-heads, rotated in the right direction."""
        if fms is None:
            fms = self.css('viewFlowMarkerSize')
        if fmf is None:
            fmf = self.css('viewFlowCurvatureFactor')

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
        # Arrow head position.
        arrowSize = 12
        arrowAngle = 0.4
        angle = atan2(xt-xb2, yt-yb2)
        hookedAngle = radians(degrees(angle)-90)
        ax1 = xt - cos(hookedAngle+arrowAngle) * arrowSize
        ay1 = yt + sin(hookedAngle+arrowAngle) * arrowSize
        ax2 = xt - cos(hookedAngle-arrowAngle) * arrowSize
        ay2 = yt + sin(hookedAngle-arrowAngle) * arrowSize

        # FIXME: don't use builder, use context.
        b = self.context.b
        b.newPath()
        self.setFillColor(noColor)
        b.moveTo((xs, ys))
        # End in middle of arrow head.
        b.curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2))
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
        """If `self.showFrame` and `e` is a page, or if `e.showFrame == True`,
        then draw the frame of the element."""
        if (self.showFrame and e.isPage) or e.showFrame:
            x = origin[0]
            y = origin[1]
            mt, mr, mb, ml = e.margin
            context = self.context
            context.fill(color(random(), random(), random(), 0.3))
            context.rect(x-ml, y, max(2,ml), e.h)
            context.rect(x+e.w, y, max(1,mr), e.h)
            context.rect(x-ml, y-mb, ml+e.w+mr, max(1,mb))
            context.rect(x-ml, y+e.h, ml+e.w+mr, max(1,mt))

    def drawElementInfo(self, e, origin):
        """For debugging this will make the elements show their info. The css
        flag "showOrigin" defines if the origin marker of an element is
        drawn. Collect the (e, origin), so we can later draw all info, after
        the main drawing has been done."""
        if not e.eId in self.elementsNeedingInfo:
            self.elementsNeedingInfo[e.eId] = (e, origin)

        # Drawing outside rotation / scaling mode, so the origin of
        # the element is visible.
        self.drawElementOrigin(e, origin)

    def _drawElementsNeedingInfo(self, e):
        b = self.b
        context = self.context
        for e, origin in self.elementsNeedingInfo.values():
            #p = pointOffset(e.origin, origin)
            #p = e._applyScale(self, p)
            #px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            px, py, _ = pointOffset(e.origin, origin)
            if (self.showElementInfo or e.isPage) or e.showElementInfo:
                # Draw box with element info.
                bs = context.newString(e.getElementInfoString(), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=color(0.1)))
                tw, th = bs.textSize
                # Padding in box and shadow offset.
                Pd = 4
                # Make info box outdent the element. Keeping shadow on the
                # element top left corner..
                tpx = px - Pd/2
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

            if (self.showDimensions or e.isPage) or e.showDimensions:
                # TODO: Make separate arrow functio and better positions
                # Draw width and height measures
                context.fill(noColor)
                context.stroke(blackColor, w=pt(0.25))
                S = self.css('viewInfoOriginMarkerSize', pt(5))
                x1, y1, x2, y2 = px + e.left, py + e.bottom, e.right, e.top

                context.circle(x1, y1, 20)
                context.circle(x1, y2, 20)
                context.circle(x2, y1, 20)
                context.circle(x2, y2, 20)

                # Horizontal measure.
                context.line((x1, y1 - 0.5*S), (x1, y1 - 3.5*S))
                context.line((x2, y1 - 0.5*S), (x2, y1 - 3.5*S))
                context.line((x1, y1 - 2*S), (x2, y1 - 2*S))
                # Arrow heads.
                context.line((x1, y1 - 2*S), (x1+S, y1 - 1.5*S))
                context.line((x1, y1 - 2*S), (x1+S, y1 - 2.5*S))
                context.line((x2, y1 - 2*S), (x2-S, y1 - 1.5*S))
                context.line((x2, y1 - 2*S), (x2-S, y1 - 2.5*S))

                bs = context.newString(asFormatted(x2 - x1),
                                       style=dict(font=self.css('viewInfoFont'),
                                                  fontSize=self.css('viewInfoFontSize'),
                                                  leading=self.css('viewInfoLeading'),
                                                  textFill=color(0.1)))
                tw, th = bs.textSize
                context.text(bs, ((x2 + x1)/2 - tw/2, y1-1.5*S))

                # Vertical measure.
                context.line((x2+0.5*S, y1), (x2+3.5*S, y1))
                context.line((x2+0.5*S, y2), (x2+3.5*S, y2))
                context.line((x2+2*S, y1), (x2+2*S, y2))
                # Arrow heads.
                context.line((x2+2*S, y2), (x2+2.5*S, y2-S))
                context.line((x2+2*S, y2), (x2+1.5*S, y2-S))
                context.line((x2+2*S, y1), (x2+2.5*S, y1+S))
                context.line((x2+2*S, y1), (x2+1.5*S, y1+S))

                bs = context.newString(asFormatted(y2 - y1), style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=0.1))
                tw, th = bs.textSize
                context.text(bs, (x2+2*S-tw/2, (y2+y1)/2))

            e._restoreScale(self)

    def drawElementOrigin(self, e, origin):
        if not (self.showOrigin or e.showOrigin):
            return

        px, py, _ = pointOffset(e.origin, origin)

        S = e.css('viewInfoOriginMarkerSize', pt(5))
        # Draw origin of the element.
        fill = e.css('viewInfoOriginMarkerFill', noColor)
        stroke = e.css('viewInfoOriginMarkerStroke', blackColor)
        width = e.css('viewInfoOriginMarkerStrokeWidth', pt(0.25))
        # Transparent fill, so we can see the marker on dark backgrounds.
        self.context.fill(fill)
        self.context.stroke(stroke, width)
        self.context.oval(px-S, py-S, 2*S, 2*S)
        self.context.line((px-S, py), (px+S, py))
        self.context.line((px, py-S), (px, py+S))

        if (self.showDimensions and e.isPage) or e.showDimensions:
            bs = self.context.newString(e.xy, style=dict(font=self.css('viewInfoFont'),
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'),
                textFill=color(0.1)))
            w, h = bs.textSize
            self.context.text(bs, (px - w/2, py + S*1.5))

    def drawMissingElementRect(self, e, origin):
        """When designing templates and pages, this will draw a filled
        rectangle on the element bounding box (if self.css('missingElementFill'
        is defined) and a cross, indicating that this element has missing
        content (as in unused image frames). Only draw if the list
        self.showGrid contains proper types of grid names.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showMissingElement = True
        >>> view.drawMissingElementRect(e, (0, 0))
        """
        if (self.showMissingElement and e.isPage) or e.showMissingElement:
            context = self.context

            p = pointOffset(e.origin, origin)
            p = self._applyScale(e, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

            context.save()
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
            context.restore()
            e._restoreScale(self)

    #    G R I D

    def drawGrid(self, e, origin, background=False):
        """Draws grid of lines and / or rectangles if colors are set in the
        style.  Normally origin is ORIGIN `pt(0, 0, 0)`, but it's possible to
        give the grid a fixed offset.

        If types self.showGrid is set, display the type of grid in forground for
        `(GRID_COL, GRID_ROW, GRID_SQR)` and draw in background for `(GRID_COL_BG,
        GRID_ROW_BG, GRID_SQR_BG)`.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawGrid(e, (0, 0))
        >>> view.showGrid = [GRID_COL_BG]
        >>> view.drawGrid(e, (0, 0), background=True)
        """
        if (self.showGrid and e.isPage):
            showGrid = self.showGrid
        elif e.showGrid:
            showGrid = e.showGrid
        else:
            return

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        # Drawing the grid as vertical lines. Check on foreground/background flags.
        if (background and GRID_COL_BG in showGrid) or (not background and GRID_COL in showGrid):
            # Set color for vertical grid lines
            self.context.fill(noColor)
            gridStrokeColor = e.css('viewGridStrokeY', noColor)
            gridStrokeWidth = e.css('viewGridStrokeWidthY', blackColor)
            self.context.stroke(gridStrokeColor, gridStrokeWidth)

            gridX = e.gridX
            if gridX:
                x = px+e.pl # Position on left padding of page/e
                y1 = py+e.pb
                y2 = y1 + e.ph
                for cw in gridX:
                    if isinstance(cw, (tuple, list)):
                        cw, gx = cw
                    else:
                        gx = 0
                    self.context.line((x, y1), (x, y2))
                    if gx:
                        self.context.line((x+cw, y1), (x+cw, y2))
                    x += cw + gx

        # Drawing the grid as horizontal lines. Check on foreground/background flags.
        if (background and GRID_ROW_BG in showGrid) or (not background and GRID_ROW in showGrid):
            # Set color for vertical grid lines
            self.context.fill(noColor)
            gridStrokeColor = e.css('viewGridStrokeX', noColor)
            gridStrokeWidth = e.css('viewGridStrokeWidthX', blackColor)
            self.context.stroke(gridStrokeColor, gridStrokeWidth)

            gridY = e.gridY
            if gridY:
                x1 = px+e.pl
                x2 = x1 + e.pw
                y = py+e.pb # Position on bottom padding of page/e
                for ch in gridY:
                    if isinstance(ch, (tuple, list)):
                        ch, gy = ch
                    else:
                        gy = 0
                    self.context.line((x1, y), (x2, y))
                    if gy:
                        self.context.line((x1, y+ch), (x2, y+ch))
                    y += ch + gy

        # Drawing the grid as rectangles. Check on foreground/background flags.
        if (background and GRID_SQR_BG in showGrid) or (not background and GRID_SQR in showGrid):
            # Set color for grid rectangles
            self.context.fill(e.css('viewGridFill', noColor))
            self.context.stroke(e.css('viewGridStroke', noColor))

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
                        self.context.rect(px+x, py+y, cw, ch)
                        y += ch + gy
                    x += cw + gx

    def drawBaselines(self, e, origin, background=False):
        """Draws baseline grid if self.showBaselineGrid is True and there is a
        baseline defined > 0. Use the color from style values viewGridStrokeX
        and viewGridStrokeWidthX to make a difference with the baselines drawn
        by Text with style values baselineColor and baselineWidth.

        If this method is called by an element instead of self, the show
        attribute is a way to overwrite the setting of self.showBaselineGrid.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> style = getRootStyle() # Get default values
        >>> #style['font'] = 'PageBot-Regular'
        >>> #style = dict(font='PageBot-Regular', baselineGrid=1)
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showBaselineGrid = [BASE_LINE, BASE_INDEX_LEFT, BASE_Y_LEFT]
        >>> view.drawBaselines(e, pt(0, 0))
        """
        show = e.showBaselineGrid or self.showBaselineGrid

        # Sets the default, in case not drawing or show is True
        if not show:
            return

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        # Ignore z-axis for now.
        px, py, _ = e._applyAlignment(p)

        # Get the baseline grid of this element.
        baselineGrid = e.baselineGrid
        # Index size depends on baseline.
        indexFontSize = max(9, min(16, baselineGrid*0.5))
        # Gutter between index marker and element padding.
        indexGutter = baselineGrid/4

        startY = e.baselineGridStart
        if startY is None:
            # Otherwise use the top padding as start Y.
            startY = e.pt

        # Assumes origin at bottom for self.context drawing.
        oy = e.h - startY

        line = 0 # Line index
        baselineColor = e.css('baselineColor', color(0,7))
        baselineWidth = e.css('baselineWidth', 0.5)

        # Format of line numbers.
        style = dict(font=e.css('viewMarkerFont'), xTextAlign=RIGHT,
            fontSize=indexFontSize, stroke=noColor, textFill=baselineColor)
        self.context.fill(noColor)
        self.context.stroke(baselineColor, baselineWidth)

        # Run until the padding of the element is reached..
        while oy > e.pb:
            tl = tr = None
            if not background:
                # Shows line baseline index.
                if BASE_INDEX_LEFT in show:
                    tl = repr(line)
                # Show vertical position marker.
                elif BASE_Y_LEFT in show:
                    tl = repr(e.h - oy)

                # Shows line baseline index.
                if BASE_INDEX_RIGHT in show:
                    tr = repr(line)
                # Show vertical position marker.
                elif BASE_Y_RIGHT in show:
                    tr = repr(e.h - oy)

            bsl = self.context.newString(tl, style=style)
            bsr = self.context.newString(tr, style=style)

            twl, thl = bsl.size
            twr, thr = bsr.size
            if BASE_INSIDE in show:
                if tl:
                    self.context.text(bsl, (px + e.pl + indexGutter, py + oy - thl/5))
                if tr:
                    self.context.text(bsr, (px + e.pl + e.pw - twr - indexGutter, py + oy - thr/5))
                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    self.context.line((px + e.pl + 2*indexGutter + twl, py + oy), (px + e.pw - 2*indexGutter - twr, py + oy))
            else:
                if tl:
                    self.context.text(bsl, (px + e.pl - twl - indexGutter, py + oy - thl/5))
                if tr:
                    self.context.text(bsr, (px + e.pl + e.pw + indexGutter, py + oy - thr/5))
                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    self.context.line((px + e.pl, py + oy), (px + e.w - e.pr, py + oy))
            line += 1 # Increment line index.

            # Next vertical line position of baseline grid.
            oy -= baselineGrid

    #    M A R K E R S

    def _drawRegistrationMark(self, e, origin, cmSize, cmStrokeWidth, vertical):
        """Draw registration mark as position x, y."""
        x, y = origin
        if vertical:
            dx = cmSize/2
            dy = cmSize
        else:
            dx = cmSize
            dy = cmSize/2
        e.context.fill(noColor)
        # Draw CMYK all on, color(cmyk=1).
        e.context.stroke(registrationColor, w=cmStrokeWidth)
        # Registration circle
        e.context.circle(x, y, cmSize/4)
        # Registration cross, in length of direction.
        e.context.line((x - dx, y), (x + dx, y)) # Horizontal line.
        e.context.line((x, y + dy), (x, y - dy)) # Vertical line.

    def drawRegistrationMarks(self, e, origin):
        """Draw standard registration mark, to show registration of CMYK colors.

        https://en.wikipedia.org/wiki/Printing_registration.

        >>> from pagebot import getContext
        >>> from pagebot.elements.views.pageview import PageView
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element() # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showRegistrationMarks = True
        >>> view.drawRegistrationMarks(e, pt(0, 0))
        """
        if (self.showRegistrationMarks and e.isPage) or e.showRegistrationMarks:
            # TODO: Make cropmark go closer to page edge and disappear if too small.
            cmSize = min(self.pl/2, self.css('viewCropMarkSize'))
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')
            x, y = point2D(origin)
            w, h = e.size
            # Bottom registration mark.
            self._drawRegistrationMark(e, (x + w/2, y - cmSize), cmSize, cmStrokeWidth, False)
            # Left registration mark.
            self._drawRegistrationMark(e, (x - cmSize, y + h/2), cmSize, cmStrokeWidth, True)
            # Right registration mark.
            self._drawRegistrationMark(e, (x + w + cmSize, y + h/2), cmSize, cmStrokeWidth, True)
            # Top registration mark.
            self._drawRegistrationMark(e, (x + w/2, y + h + cmSize), cmSize, cmStrokeWidth, False)

    def drawCropMarks(self, e, origin):
        """If the show flag is set, then draw the cropmarks or page frame.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.elements.views.pageview import PageView
        >>> style = getRootStyle() # Get default values
        >>> e = Element()
        >>> view = PageView(context=context, style=style)
        >>> view.showCropMarks = True
        >>> view.folds = [(mm(40), mm(60)),]
        >>> view.drawCropMarks(e, pt(0, 0))
        """
        if (self.showCropMarks and e.isPage) or e.showCropMarks:
            x, y = point2D(origin) # Ignore z-axus for now.
            w, h = e.size
            folds = self.css('folds')
            cmDistance = self.css('viewCropMarkDistance') # From the side
            cmSize = min(self.css('viewCropMarkSize', pt(32)), self.pl)
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')

            self.context.fill(noColor)
            # For CMYK, draw all colors color(cmyk=1)).
            self.context.stroke(registrationColor, w=cmStrokeWidth)
            # Bottom left
            self.context.line((x - cmDistance, y), (x - cmSize, y))
            self.context.line((x, y - cmDistance), (x, y - cmSize))
            # Bottom right
            self.context.line((x + w + cmDistance, y), (x + w + cmSize, y))
            self.context.line((x + w, y - cmDistance), (x + w, y - cmSize))
            # Top left
            self.context.line((x - cmDistance, y + h), (x - cmSize, y + h))
            self.context.line((x, y + h + cmDistance), (x, y + h + cmSize))
            # Top right
            self.context.line((x + w + cmDistance, y + h), (x + w + cmSize, y + h))
            self.context.line((x + w, y + h + cmDistance), (x + w, y + h + cmSize))
            # Any fold lines to draw on the page?
            if folds is not None:
                for fx, fy in folds:
                    if fx is not None:
                        self.context.line((x + fx, y - cmDistance), (x + fx, y - cmSize))
                        self.context.line((x + fx, y + h + cmDistance), (x + fx, y + h + cmSize))
                    if fy is not None:
                        self.context.line((x - cmDistance, y + fy), (x - cmSize, y + fy))
                        self.context.line((x + w + cmDistance, y + fy), (x + w + cmSize, y + fy))

    def drawColorBars(self, e, origin):
        """Draw the color bars for offset printing color calibration.

        TODO: Add more types of color bars and switch from scaling PDF to
        drawing them by script
        TODO Get this to work for content of the parameter set.
        """

        showColorBars = e.showColorBars or (e.isPage and self.showColorBars)
        if not showColorBars:
            # Nothing to do.
            return

        ox, oy = point2D(origin)

        if ECI_GrayConL in showColorBars:
            path = getResourcesPath() + '/' + ECI_GrayConL
            if COLORBAR_LEFT in showColorBars:
                self.context.image(path, p=(ox-self.pl+pt(3), oy), h=e.h)

            # TODO: Does not generate the right position?
            if COLORBAR_RIGHT in showColorBars:
                self.context.image(path, p=(ox+e.w+self.pr*2/3, oy), h=e.h)

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
