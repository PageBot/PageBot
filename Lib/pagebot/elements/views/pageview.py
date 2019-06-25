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
#     pageview.py
#

import os
from random import random
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from pagebot import getResourcesPath
from pagebot.toolbox.color import color, noColor, blackColor, registrationColor
from pagebot.elements.views.baseview import BaseView
from pagebot.elements.pbquire import Quire
from pagebot.constants import (TOP, RIGHT, BOTTOM, LEFT, ORIGIN, QUIRE_SPREAD,
    BOTTOM_FOLD, TOP_FOLD, LEFT_FOLD, RIGHT_FOLD,
    GRID_COL, GRID_ROW, GRID_SQR,
    GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG, BASE_LINE, BASE_LINE_BG,
    BASE_INDEX_LEFT, BASE_Y_LEFT, BASE_INDEX_RIGHT, BASE_Y_RIGHT,
    BASE_INSIDE, DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH,
    ECI_GrayConL, COLORBAR_LEFT, COLORBAR_RIGHT)
from pagebot.toolbox.units import pt, upt, pointOffset, point2D, asFormatted
from pagebot.toolbox.transformer import *

class PageView(BaseView):
    """The PageView contains the set of Quire instances to export the pages as
    documents. A View is just another kind of container, kept by a Document to
    make a certain presentation of the page tree. The PageView typically holds
    Quire elements that make one-directional links to document pages in order
    to compose them in spreads or folding compositions."""
    viewId = 'Page'

    EXPORT_PATH = '_export/' # Default path for local document export, that does not commit documents to Github.

    def __repr__(self):
        return '<PageView>'

    def newQuire(self, folds=None, startPage=None):
        """Add a new Quire instance to self.elements. A Quire is a container of pages, capable of grouping
        then in certains way, depending on the folding schema. The most simple one it a single fold,
        with spread pages on either side.
        Quire instances are added as sequence to the """
        return Quire(folds=folds, startPage=startPage, parent=self)

    def getSortedPages(self):
        """Get the dictionary of sorted pages from the document. Depending on the self.showSpread
        flag, the answered dicitionary is the plain self.doc.getSortedPages() result, or wrapped 
        as Quire instances containing positioned spread pages."""
        sortedPages = self.doc.getSortedPages() 
        if self.showSpread:
            spreads = {} # Key is uneven page number. Value is a Quire, holding spread pages.

            # If flag is set, compose the page dictionary into a dictionary of larger pages, holding 
            # Quire instances that can compose vairous layouts of the pages, including spreads.
            # page.ml and page.mr define the distance between the spread pages.
            sortedPages = Quire.pages2Spreads(QUIRE_SPREAD)
        return sortedPages

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """Draw the selected pages. pageSelection is an optional set of
        y-pageNumbers to draw.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BusinessCard, A4, QUIRE_QUARTO
        >>> doc = Document(size=A4, autoPages=4) # Make 4 pages to be composed as a Quire of 2 spreads
        >>> view = doc.view
        >>> q = view.newQuire(folds=QUIRE_QUARTO)
        >>> len(view.elements)
        1
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
        self.context.newDocument(w, h) # Allow the context to create a new document and page canvas.
        self.context.newDrawing()
        
        # Get dictionary of pages or spreads
        sortedPages = self.getSortedPages()

        # Recursively let all element prepare for the upcoming build, e.g. by saving scaled images
        # into cache if that file does not already exists. Note that this is done on a page-by-page
        # level, not a preparation of all
        for pn, pages in sortedPages:
            for page in pages:
                page.prepare(self)

        for pn, pages in sortedPages:
            #if pageSelection is not None and not page.y in pageSelection:
            #    continue

            '''
            Create a new DrawBot viewport page to draw template + page, if not
            already done. In case the document is oversized, then make all
            pages the size of the document, so the pages can draw their
            crop marks. Otherwise make DrawBot pages of the size of each page.
            Size depends on the size of the larges pages + optional document
            padding.
            '''
            page = pages[0] # TODO: make this work for pages that share the same page number
            pw, ph = w, h  # Copy from main (w, h), since they may be altered, from the orgiinal document size..

            if self.pl >= self.viewMinInfoPadding and \
               self.pt >= self.viewMinInfoPadding and \
               self.pb >= self.viewMinInfoPadding and \
               self.pr >= self.viewMinInfoPadding:
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

            #  Make page in context, actual page may be smaller if showing cropmarks.
            self.context.newPage(pw, ph) 

            # If page['frameDuration'] is set and saving as movie or animated gif,
            # then set the global frame duration.
            # Set the duration of this page, in case exporting GIF
            self.context.frameDuration(page.frameDuration) 

            # View may have defined a background. Build with page bleed, if it is defined.
            fillColor = self.style.get('fill', noColor)

            if fillColor is not noColor:
                bt, br, bb, bl = page.bleed
                self.context.fill(fillColor)
                self.context.rect(page.leftBleed, page.bottomBleed, pw+br+bl, ph+bt+bb)

            if self.drawBefore is not None: # Call if defined
                self.drawBefore(page, self, origin)

            self.drawPageMetaInfo(page, origin, background=True)

            # Since self already adjust origin, scale, etc. we don't use the
            # page.build here. Instead we calle the drawing of its elements
            # too.
            page.buildChildElements(self, origin, **kwargs)
            self.drawPageMetaInfo(page, origin, background=False)

            if self.drawAfter is not None: # Call if defined
                self.drawAfter(page, self, origin)

            # Self.infoElements now may have collected elements needed info to
            # be drawn, after all drawing is done. So the info boxes don't get
            # covered by regular page content.
            for e in self.elementsNeedingInfo.values():
                self._drawElementsNeedingInfo(e)

        '''
        Export the document to fileName for all pages in sequential order. If
        pageSelection is defined, it must be a list with page numbers to
        export. This allows the order to be changed and pages to be omitted.
        The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct
        the type of drawing and export that needs to be done.

        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in
        special cases, there is not straighforward (or sequential) export of
        pages, e.g. when generating HTML/CSS. In that case use
        MyBuilder(document).export(fileName), the builder is responsible to
        query the document, pages, elements and styles.
        '''

        folder = path2ParentPath(path)

        if not os.path.exists(folder):
            os.mkdir(folder)

        # FIXME:
        #  - "fileName" is undefined
        #  - "frameDuration" is a method or a CSS value ?
        #if frameDuration is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
        #    frameDuration(frameDuration)

        self.context.saveDocument(path, multiPage=multiPage)

    #   D R A W I N G  P A G E  M E T A  I N F O

    def drawPageMetaInfo(self, page, origin, path=None, background=False):
        """Draw the foreground meta info of the page, depending on the settings of the flags.

        >>> from pagebot import getContext
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
        if not background:
            self.drawFrame(page, origin)
            self.drawMargin(page, origin)
            self.drawPadding(page, origin)
            self.drawNameInfo(page, origin, path) # Use path to show file name in page meta info.
            self.drawColorBars(page, origin) # Color bars under registration marks?
            self.drawRegistrationMarks(page, origin)
            self.drawCropMarks(page, origin)
            self.drawElementOrigin(page, origin)
        self.drawGrid(page, origin, background=background)
        self.drawBaselines(page, origin, background=background)
        self.drawFlowConnections(page, origin)

    def drawFrame(self, e, origin):
        """Draw the page frame if the the flag is on and  if there ie padding
        enough to show other meta info.  Otherwise the padding is truncated to
        0: no use to draw the frame.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showFrame = True
        >>> view.drawFrame(e, (0, 0))

        """
        if ((self.showFrame and e.isPage) or e.showFrame) and \
                self.pl >= self.viewMinInfoPadding and self.pr >= self.viewMinInfoPadding and \
                self.pt >= self.viewMinInfoPadding and self.pb >= self.viewMinInfoPadding:
            # TODO: May need to be scaled, as self.drawPadding does.
            ox, oy = point2D(origin)
            context = self.context
            context.fill(noColor)
            context.stroke(color(0, 0, 1), pt(0.5))
            context.rect(ox, oy, e.w, e.h)
            # If there are folds, draw them too in the same color.
            folds = e.folds or self.folds
            if folds:
                for (x, y) in folds:
                    if x is not None:
                        context.line((ox+x, oy), (ox+x, oy+e.h))
                    if y is not None:
                        context.line((ox, ox+y), (ox+e.w, ox+y))


    def drawPadding(self, e, origin):
        """Draw the page frame of its current padding.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showPadding = True
        >>> view.drawPadding(e, (0, 0))
        """
        pt, pr, pb, pl = e.padding
        if ((self.showPadding and e.isPage) or e.showPadding) and (pt or pr or pb or pl):
            context = self.context

            if e.isPage:
                p = pointOffset(e.origin, origin)
            else:
                p = origin
            px, py = point2D(e._applyScale(self, p))

            context.fill(noColor)
            context.stroke(self.css('viewPaddingStroke', color(0.2, 0.2, 1)),
                                   self.css('viewPaddingStrokeWidth', 0.5))
            if e.originTop:
                #context.rect(px+pl, py+pb, e.w-pl-pr, e.h-pt-pb)
                context.rect(px+pl, py-e.h+pb, e.w-pl-pr, e.h-pt-pb)
            else:
                context.rect(px+pl, py+pb, e.w-pl-pr, e.h-pt-pb)
            e._restoreScale(self)

    def drawMargin(self, e, origin):
        """Draw the page frame of its current margin.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showMargin = True
        >>> view.drawMargin(e, (0, 0))
        """
        mt, mr, mb, ml = e.margin
        if ((self.showMargin and e.isPage) or e.showMargin) and (mt or mr or mb or ml):
            context = self.context

            if e.isPage:
                p = pointOffset(e.origin, origin)
            else:
                p = origin
            px, py = point2D(e._applyScale(self, p))

            context.fill(noColor)
            context.stroke(self.css('viewMarginStroke', color(0.2, 0.2, 1)),
                                   self.css('viewMarginStrokeWidth', 0.5))
            if e.originTop:
                #context.rect(px+pl, py+pb, e.w-pl-pr, e.h-pt-pb)
                context.rect(px-ml, py-e.h-mb, e.w+ml+mr, e.h+mt+mb)
            else:
                context.rect(px-ml, py-mb, e.w+ml+mr, e.h+mt+mb)
            e._restoreScale(self)

    def drawNameInfo(self, e, origin, path):
        """Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> path = '_export/PageNameInfo.pdf'
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showNameInfo = True
        >>> view.drawNameInfo(e, (0, 0), path)
        """
        if (self.showNameInfo and e.isPage) or e.showNameInfo:
            context = self.context
            cmDistance = self.css('viewCropMarkDistance') # Position of text is based on crop mark size.
            cmSize = self.css('viewCropMarkSize') - cmDistance
            fontSize = self.css('viewNameFontSize')
            dt = datetime.datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            if e.isPage and e.parent is not None: # Test if there is a document
                pn = e.parent.getPageNumber(e)
                if pn[1] == 0: # First or only page on this page number, then just show pn[0]
                    pn = pn[0]
                if len(e.parent.pages) > 1: # More than one page, then show total
                    pn = '%s/%d' % (pn, len(e.parent.pages))
                title = e.parent.title or 'Untitled'
                s = 'Page %s | %s | %s' % (pn, d, title)
            else: # Otherwise always page number #1
                pn = 1
                title = 'Untitled'
                s = 'Element %s | %s' % (d, title)
            if e.name and e.name != 'default':
                s += ' | ' + e.name
            if path is not None:
                s += ' | ' + path.split('/')[-1] # We're only interested in the file name.
            bs = context.newString(s, style=dict(font=self.css('viewNameFont'), textFill=blackColor, fontSize=fontSize))
            tw, th = bs.size
            self.context.textBox(bs, (self.pl + cmDistance, self.pb + e.h + cmSize - fontSize*2, e.pw, th)) # Draw on top of page.

    #   D R A W I N G  F L O W S

    def drawFlowConnections(self, e, origin):
        """If rootStyle.showFlowConnections is True, then draw the flow connections
        on the page, using their stroke/width settings of the style."""

        context = self.context
        p = pointOffset(e.origin, origin)
        p = e._applyScale(self, p)
        px, py, _ = p = e._applyAlignment(p) # Ignore z-axis for now.

        if (self.showFlowConnections and e.isPage) or e.showFlowConnections:

            fmf = 0.15#self.css('viewFlowCurvatureFactor', 0.15)
            for startE in e.elements:
                nextE = startE.next
                if nextE is not None:
                    # For all the flow sequences found in the page, draw flow arrows at offset (ox, oy)
                    # This offset is defined by optional
                    sx = startE.right
                    sy = startE.bottom
                    nx = nextE.left
                    ny = nextE.top

                    xm = (nx + sx)/2
                    ym = (ny + sy)/2
                    xb1 = xm * upt(ny - sy) * fmf
                    yb1 = ym * upt(nx - sx) * fmf
                    xb2 = xm * upt(ny - sy) * fmf
                    yb2 = ym * upt(nx - sx) * fmf

                    context.fill(noColor)
                    context.stroke(color(0), 1)

                    context.newPath()
                    context.moveTo((sx, sy))
                    context.curveTo((xb1, yb1), (xb2, yb2), (nx, ny)) #((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
                    context.drawPath()

    def drawArrow(self, e, xs, ys, xt, yt, onText=1, startMarker=False, endMarker=False, fms=None, fmf=None,
            fill=noColor, stroke=noColor, strokeWidth=None):
        """Draw curved arrow marker between the two points."""
        context = self.context

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

        context.stroke(stroke, strokeWidth)
        if startMarker:
            if fill is None:
                fill = self.css('viewFlowMarkerFill', noColor)
            context.fill(fill)
            context.oval(xs - fms, ys - fms, 2 * fms, 2 * fms)

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

        context.newPath()
        context.fill(noColor)
        context.moveTo((xs, ys))
        context.curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
        context.drawPath()

        #  Draw the arrow head.
        context.newPath()
        context.fill(stroke)
        context.stroke(noColor)
        context.moveTo((xt, yt))
        context.lineTo((ax1, ay1))
        context.lineTo((ax2, ay2))
        context.closePath()
        context.drawPath()

        if endMarker:
            context.fill(self.css('viewFlowMarkerFill', noColor))
            context.oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

    #   D R A W I N G  E L E M E N T

    def drawElementFrame(self, e, origin):
        """If self.showFrame and e is a page, or if e.showFrame == True, then draw
        the frame of the element."""
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
        # Supposedly drawing outside rotation/scaling mode, so the origin of
        # the element is visible.
        self.drawElementOrigin(e, origin)

    def _drawElementsNeedingInfo(self, e):
        b = self.b
        context = self.context
        for e, origin in self.elementsNeedingInfo.values():
            p = pointOffset(e.origin, origin)
            p = e._applyScale(self, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            if (self.showElementInfo or e.isPage) or e.showElementInfo:
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

            if (self.showDimensions or e.isPage) or e.showDimensions:
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
        if not (self.showOrigin or e.showOrigin):
            return

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

        if (self.showDimensions and e.isPage) or e.showDimensions:
            bs = context.newString(e.xy, style=dict(font=self.css('viewInfoFont'),
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'),
                textFill=color(0.1)))
            w, h = bs.size
            context.text(bs, (px - w/2, py + S*1.5))

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

    def drawGrid(self, e, origin, background=False):
        """Draw grid of lines and/or rectangles if colors are set in the style.
        Normally origin is ORIGIN pt(0, 0, 0), but it's possible to give the grid
        a fixed offset.

        If types self.showGrid is set, display the type of grid in forground for
        (GRID_COL, GRID_ROW, GRID_SQR) and draw in background for (GRID_COL_BG,
        GRID_ROW_BG, GRID_SQR_BG)

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
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

        context = self.context

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        # Drawing the grid as vertical lines. Check on foreground/background flags.
        if (background and GRID_COL_BG in showGrid) or (not background and GRID_COL in showGrid):
            # Set color for vertical grid lines
            context.fill(noColor)
            # Use local element color setting, otherwise find by view.css
            gridStrokeColor = e.style.get('viewGridStrokeY', self.css('viewGridStrokeY', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthY', self.css('viewGridStrokeWidthY', pt(0.5)))
            context.stroke(gridStrokeColor, gridStrokeWidth)

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
                    context.line((x, y1), (x, y2))
                    if gx:
                        context.line((x+cw, y1), (x+cw, y2))
                    x += cw + gx

        # Drawing the grid as horizontal lines. Check on foreground/background flags.
        if (background and GRID_ROW_BG in showGrid) or (not background and GRID_ROW in showGrid):
            # Set color for vertical grid lines
            context.fill(noColor)
            # Use local element color setting, otherwise find by view.css
            gridStrokeColor = e.style.get('viewGridStrokeX', self.css('viewGridStrokeX', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthX', self.css('viewGridStrokeWidthX', pt(0.5)))
            context.stroke(gridStrokeColor, gridStrokeWidth)

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
                    context.line((x1, y), (x2, y))
                    if gy:
                        context.line((x1, y+ch), (x2, y+ch))
                    y += ch + gy

        # Drawing the grid as rectangles. Check on foreground/background flags.
        if (background and GRID_SQR_BG in showGrid) or (not background and GRID_SQR in showGrid):
            # Set color for grid rectangles
            # Use local element color setting, otherwise find by view.css
            gridFillColor = e.style.get('gridFillColor', self.css('gridFillColor', noColor))
            gridStrokeColor = e.style.get('viewGridStrokeX', self.css('viewGridStrokeX', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthX', self.css('viewGridStrokeWidthX', pt(0.5)))
            context.fill(gridFillColor)
            context.stroke(gridStrokeColor, gridStrokeWidth)

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

    def drawBaselines(self, e, origin, background=False):
        """Draw baseline grid if self.showBaselineGrid is True and there is a
        baseline defined > 0. Use the color from style values viewGridStrokeX
        and viewGridStrokeWidthX to make a difference with the baselines drawn
        by TextBox with style values baselineColor and baselineWidth.

        In this method is called by an element, instead of self, the show
        attribute is a way to overwrite the setting of self.showBaselineGrid

        == NOTE == TextBox elements have their own baseline drawing method

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showBaselineGrid = [BASE_LINE, BASE_INDEX_LEFT, BASE_Y_LEFT]
        >>> view.drawBaselines(e, pt(0, 0))
        """
        show = e.showBaselineGrid or self.showBaselineGrid

        # Sets the default, in case not drawing or show is True
        if not show:
            return

        context = self.context

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        baselineGrid = e.baselineGrid # Get the baseline grid of this element.
        indexFontSize = max(9, min(16, baselineGrid*0.5)) # Index size depends on baseline.
        indexGutter = baselineGrid/4 # Gutter between index marker and element padding

        baselineYs = [] # Collect all baseline positions on e
        if e.originTop:
            oy = yy = startY = (e.baselineGridStart or e.pt) # Assumes origin at top for context drawing
            while yy < e.h: # Run over the the padding bottom until page side
                baselineYs.append(yy)
                yy += baselineGrid
        else: # Page origin is at the bottom
            startY = e.h - (e.baselineGridStart or e.pt)
            oy = yy = startY # Assumes origin at bottom for context drawing.
            while yy > 0: # Run over the the padding bottom until page side
                baselineYs.append(yy)
                yy -= baselineGrid

        baselineColor = e.style.get('baselineColor', self.css('baselineColor', DEFAULT_BASELINE_COLOR))
        baselineWidth = e.style.get('baselineWidth', self.css('baselineWidth', DEFAULT_BASELINE_WIDTH))

        # Format of line numbers.
        style = dict(font=e.css('viewMarkerFont'), xTextAlign=RIGHT,
            fontSize=indexFontSize, stroke=noColor, textFill=baselineColor)
        context.fill(noColor)
        context.stroke(baselineColor, baselineWidth)

        for lineIndex, oy in enumerate(baselineYs): 
            tl = tr = None
            if not background:
                if BASE_INDEX_LEFT in show: # Shows line baseline index
                    tl = repr(lineIndex)
                elif BASE_Y_LEFT in show: # Show vertical position marker
                    tl = repr(e.h - oy)

                if BASE_INDEX_RIGHT in show: # Shows line baseline index
                    tr = repr(lineIndex)
                elif BASE_Y_RIGHT in show: # Show vertical position marker
                    tr = repr(e.h - oy)

            bsl = context.newString(tl, style=style)
            bsr = context.newString(tr, style=style)

            twl, thl = bsl.size
            twr, thr = bsr.size

            if BASE_INSIDE in show:
                if tl:
                    context.textBox(bsl, (px + e.pl + indexGutter - twl*2, py + oy - thl/5, twl*2, thl))
                if tr:
                    context.textBox(bsr, (px + e.pl + e.pw - twr - indexGutter, py + oy - thr/5, twr*2, thr))
                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    context.line((px + e.pl + 2*indexGutter + twl*2, py + oy), (px + e.pw - 2*indexGutter - twr, py + oy))
            else:
                if tl:
                    context.textBox(bsl, (px + e.pl - twl*2 - indexGutter, py + oy - thl/5, twl*2, thl))
                if tr:
                    context.textBox(bsr, (px + e.pl + e.pw + indexGutter, py + oy - thr/5, twr*2, thr))
                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    context.line((px + e.pl, py + oy), (px + e.w - e.pr, py + oy))

    #    M A R K E R S

    def _drawRegistrationMark(self, e, origin, cmSize, cmStrokeWidth, vertical):
        """Draw registration mark as position x, y."""
        context = e.context
        x, y = origin
        if vertical:
            dx = cmSize/2
            dy = cmSize
        else:
            dx = cmSize
            dy = cmSize/2
        context.fill(noColor)
        context.stroke(registrationColor, w=cmStrokeWidth) # Draw CMYK all on, color(cmyk=1)
        # Registration circle
        context.circle(x, y, cmSize/4)
        # Registration cross, in length of direction.
        context.line((x - dx, y), (x + dx, y)) # Horizontal line.
        context.line((x, y + dy), (x, y - dy)) # Vertical line.

    def drawRegistrationMarks(self, e, origin):
        """Draw standard registration mark, to show registration of CMYK colors.
        https://en.wikipedia.org/wiki/Printing_registration.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element() # Works on generic elements as well as pages.
        >>> view = PageView(context=context, style=style)
        >>> view.showRegistrationMarks = True
        >>> view.drawRegistrationMarks(e, pt(0, 0))
        """
        # Answers a set of {TOP, RIGHT, BOTTOM, LEFT} flags
        rms = self.css('viewRegistrationMarkSize')
        if e.isPage and self.showRegistrationMarks:
            showRegistrationMarks = self.showRegistrationMarks
            cmSizes = {
                LEFT: min(self.pl/2, rms), 
                BOTTOM: min(self.pb/2, rms), 
                RIGHT: min(self.pr/2, rms), 
                TOP: min(self.pt/2, rms)
            } 
        else:
            showRegistrationMarks = e.showRegistrationMarks 
            cmSizes = {
                LEFT: min(self.ml/2, rms), 
                BOTTOM: min(self.mb/2, rms), 
                RIGHT: min(self.mr/2, rms), 
                TOP: min(self.mt/2, rms)
            } 
        if showRegistrationMarks:
            # TODO: Make crop mark go closer to page edge and disappear if too small.
            cmStrokeWidth = self.css('viewRegistrationMarkStrokeWidth')
            x, y = point2D(origin)
            w, h = e.size
            if BOTTOM in showRegistrationMarks:
                cmSize = cmSizes[BOTTOM]
                self._drawRegistrationMark(e, (x + w/2, y - cmSize), cmSize, cmStrokeWidth, False) # Bottom registration mark
            if LEFT in showRegistrationMarks:
                cmSize = cmSizes[LEFT]
                self._drawRegistrationMark(e, (x - cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Left registration mark
            if RIGHT in showRegistrationMarks:
                cmSize = cmSizes[RIGHT]
                self._drawRegistrationMark(e, (x + w + cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Right registration mark
            if TOP in showRegistrationMarks:
                cmSize = cmSizes[TOP]
                self._drawRegistrationMark(e, (x + w/2, y + h + cmSize), cmSize, cmStrokeWidth, False) # Top registration mark

    def drawCropMarks(self, e, origin):
        """If the show flag is set, then draw the crop marks or page frame.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> style = getRootStyle() # Get default values
        >>> e = Element()
        >>> view = PageView(context=context, style=style)
        >>> view.showCropMarks = True
        >>> view.folds = [(mm(40), mm(60))]
        >>> view.drawCropMarks(e, pt(0, 0))
        """
        # Answers a set of {TOP, RIGHT, BOTTOM, LEFT} flags
        if e.isPage and self.showCropMarks:
            showCropMarks = self.showCropMarks
        else:
            showCropMarks = e.showCropMarks 
        if showCropMarks:
            context = self.context

            x, y = point2D(origin) # Ignore z-axus for now.
            w, h = e.size
            folds = e.folds or self.css('folds')
            cmDistance = self.css('viewCropMarkDistance') # From the side, compare with bleed.
            cmSize = min(self.css('viewCropMarkSize', pt(32)), self.pl)
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')

            context.fill(noColor)
            context.stroke(registrationColor, w=cmStrokeWidth) # For CMYK, draw all colors color(cmyk=1))

            # Calculate distances, comparing to bleeds
            cmLeft = max(e.bleedLeft, self.bleedLeft, cmDistance)
            cmRight = max(e.bleedRight, self.bleedRight, cmDistance)
            cmBottom = max(e.bleedBottom, self.bleedBottom, cmDistance)
            cmTop = max(e.bleedTop, self.bleedTop, cmDistance)

            # Left
            if LEFT in showCropMarks:
                context.line((x - cmLeft, y), (x - cmLeft - cmSize, y))
                context.line((x - cmLeft, y + h), (x - cmLeft - cmSize, y + h))
            # Bottom
            if BOTTOM in showCropMarks:
                context.line((x, y - cmBottom), (x, y - cmBottom - cmSize))
                context.line((x + w, y - cmBottom), (x + w, y - cmBottom - cmSize))
            # Right
            if RIGHT in showCropMarks:
                context.line((x + w + cmRight, y), (x + w + cmRight + cmSize, y))
                context.line((x + w + cmRight, y + h), (x + w + cmRight + cmSize, y + h))
            # Top
            if TOP in showCropMarks:
                context.line((x, y + h + cmTop), (x, y + h + cmTop + cmSize))
                context.line((x + w, y + h + cmTop), (x + w, y + h + cmTop + cmSize))

            # Any fold lines to draw on the page?
            if folds is not None:
                for fx, fy in folds:
                    if fx is not None:
                        if BOTTOM_FOLD in showCropMarks:
                            context.line((x + fx, y - cmBottom), (x + fx, y - cmBottom - cmSize))
                        if TOP_FOLD in showCropMarks:
                            context.line((x + fx, y + h + cmTop), (x + fx, y + h + cmTop + cmSize))
                    if fy is not None:
                        if LEFT_FOLD in showCropMarks:
                            context.line((x - cmLeft, y + fy), (x - cmLeft - cmSize, y + fy))
                        if RIGHT_FOLD in showCropMarks:
                            context.line((x + w + cmRight, y + fy), (x + w + cmRight + cmSize, y + fy))

    def drawColorBars(self, e, origin):
        """Draw the color bars for offset printing color calibration
        if there is at lest than self.viewMinInfoPadding of space 
        in view left padding..
        """
        # TODO Get this to work for content of the parameter set.
        showColorBars = e.showColorBars or (e.isPage and self.showColorBars)
        if not showColorBars or self.pl < self.viewMinInfoPadding:
            return # Nothing to do.
        context = self.context

        ox, oy = point2D(origin)

        # TODO: Add more types of color bars and switch from scaling PDF to drawing them by script
        if ECI_GrayConL in showColorBars:
            path = getResourcesPath() + '/' + ECI_GrayConL
            if COLORBAR_LEFT in showColorBars:
                context.image(path, p=(ox-self.pl+pt(3), oy), h=e.h)
            if COLORBAR_RIGHT in showColorBars: # TODO: Does not generate the right position?
                context.image(path, p=(ox+e.w+self.pr*2/3, oy), h=e.h)

    #   D R A W B O T  S U P P O R T

    # The context-methods are used, in case the view itself is placed in a layout.

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
        pass

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
