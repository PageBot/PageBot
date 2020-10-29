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

from pagebot.filepaths import getResourcesPath
from pagebot.toolbox.color import color, noColor, blackColor, registrationColor
from pagebot.elements.views.baseview import BaseView
from pagebot.elements.quire import Quire
from pagebot.constants import (TOP, RIGHT, BOTTOM, LEFT, QUIRE_SPREAD,
    BOTTOM_FOLD, TOP_FOLD, LEFT_FOLD, RIGHT_FOLD,
    GRID_COL, GRID_ROW, GRID_SQR,
    GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG, BASE_LINE, BASE_LINE_BG,
    BASE_INDEX_LEFT, BASE_Y_LEFT, BASE_INDEX_RIGHT, BASE_Y_RIGHT,
    BASE_INSIDE, DEFAULT_BASELINE_COLOR, DEFAULT_BASELINE_WIDTH,
    ECI_GrayConL, COLORBAR_LEFT, COLORBAR_RIGHT)
from pagebot.toolbox.units import pt, upt, pointOffset, point2D
from pagebot.toolbox.transformer import *

class PageView(BaseView):
    """The PageView contains the set of Quire instances to export the pages as
    documents. A View is just another kind of container, kept by a Document to
    make a certain presentation of the page tree. The PageView typically holds
    Quire elements that make one-directional links to document pages in order
    to compose them in spreads or folding compositions."""

    viewId = 'Page'

    # Default path for local document export, that does not commit documents to
    # Github.
    EXPORT_PATH = '_export/'

    DEFAULT_STROKE_COLOR = color(0.2, 0.2, 1)
    DEFAULT_STROKE_WIDTH = pt(0.25)

    def __repr__(self):
        return '<PageView>'

    def newQuire(self, folds=None, startPage=None):
        """Add a new Quire instance to self.elements. A Quire is a container of
        pages, capable of grouping then in certains way, depending on the
        folding schema. The most simple one it a single fold, with spread pages
        on either side."""
        return Quire(folds=folds, startPage=startPage, parent=self)

    def getSortedPages(self):
        """Get the dictionary of sorted pages from the document. Depending on
        the self.showSpread flag, the answered dictionary is the plain
        self.doc.getSortedPages() result, or wrapped as Quire instances
        containing positioned spread pages."""
        sortedPages = self.doc.getSortedPages()

        if self.showSpread:
            # Key is uneven page number. Value is a Quire, holding spread
            # pages.
            spreads = {}

            '''
            If the flag is set, compose the page dictionary into a dictionary
            of larger pages, holding Quire instances that can compose various
            layouts of the pages, including spreads. page.ml and page.mr define
            the distance between the spread pages.
            '''
            sortedPages = Quire.pages2Spreads(QUIRE_SPREAD)

        return sortedPages

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """Draw the selected pages. pageSelection is an optional set of
        y-pageNumbers to draw.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import BusinessCard, A4, QUIRE_QUARTO
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> # Make 4 pages to be composed as a Quire of 2 spreads.
        >>> doc = Document(size=A4, autoPages=4, context=context)
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
        context = self.context
        assert context is not None
        context.fileType = path.split('.')[-1]

        # Find the maximum document page size to this in all page sizes of the
        # document.
        w, h, _ = self.doc.getMaxPageSizes(pageSelection)

        # Make sure that canvas is empty, there may have been another document
        # building in this context. Allow the context to create a new document
        # and page canvas.

        if self.pl >= self.viewMinInfoPadding and \
           self.pt >= self.viewMinInfoPadding and \
           self.pb >= self.viewMinInfoPadding and \
           self.pr >= self.viewMinInfoPadding:
            w += self.pl + self.pr
            h += self.pt + self.pb

        self.context.newDrawing(w=w, h=h)

        # Get dictionary of pages or spreads
        sortedPages = self.getSortedPages()

        # Recursively let all element prepare for the upcoming build, e.g. by
        # saving scaled images in cache if they do not already exists.  Note
        # that this is executed on a page-by-page level, not all at once.
        for pn, pages in sortedPages:
            for page in pages:
                page.prepare(self)

        for pn, pages in sortedPages:
            '''
            Creates a new DrawBot viewport page to draw template + page, if not
            already done. In case the document is oversized, then make all
            pages the size of the document, so the pages can draw their crop
            marks. Otherwise make DrawBot pages of the size of each page.  Size
            depends on the size of the larges pages + optional document
            padding.
            '''
            # TODO: make this work for pages that share the same page number
            page = pages[0]

            # Copy from main (w, h), since they may be altered, from the
            # orgiinal document size.
            pw, ph = w, h

            origin = self.pl, self.pb, pt(0)

            # Make page in context, actual page may be smaller if showing
            # cropmarks.
            self.context.newPage(w=pw, h=ph)

            # If page['frameDuration'] is set and saving as movie or animated
            # gif, then set the global frame duration. Set the duration of
            # this page, in case exporting GIF
            self.context.frameDuration(page.frameDuration)

            # View may have a background defined. Build with page bleed, if it
            # is defined.
            fillColor = self.style.get('fill', noColor)

            if fillColor is not noColor:
                bt, br, bb, bl = page.bleed
                self.context.fill(fillColor)
                self.context.rect(x=page.bleedLeft, y=page.bleedBottom,
                        w=pw+br+bl, h=ph+bt+bb)

            # If there is meta info requested for the background,
            # draw it.
            self.drawPageMetaInfoBackground(page, origin)

            # Because self already adjusts the origin, scale, etc. we don't use
            # the page.build, but we call its child elements build.
            page.buildChildElements(self, origin, **kwargs)

            # If there is meta info request for the foreground, draw it.
            self.drawPageMetaInfo(page, origin)

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
        if folder and not os.path.exists(folder):
            os.mkdir(folder)

        # FIXME:
        #  - "fileName" is undefined
        #  - "frameDuration" is a method or a CSS value ?
        #if frameDuration is not None and \
        #   (fileName.endswith('.mov') or fileName.endswith('.gif')):
        #    frameDuration(frameDuration)

        self.context.saveDrawing(path, multiPage=multiPage)

    #   D R A W I N G  P A G E  M E T A  I N F O

    def drawPageMetaInfo(self, page, origin, path=None):
        """Draw the foreground meta info of the page, depending on the
        settings.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> path = '_export/PageMetaInfo.pdf'
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=context)
        >>> #doc.view.padding # result is (0, 0, 0, 0), shouldn't be 30pt?
        >>> page = doc[1]
        >>> #page.view.padding
        >>> # result is (0, 0, 0, 0), shouldn't be 30pt?
        >>> view = doc.getView()
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawPageMetaInfo(page, (0, 0), path)
        """
        self.drawFrame(page, origin)
        self.drawMargin(page, origin)
        self.drawPadding(page, origin)

        # Use path to show file name in page meta info.
        self.drawNameInfo(page, origin, path)

        # Color bars under registration marks?
        self.drawColorBars(page, origin)
        self.drawRegistrationMarks(page, origin)
        self.drawCropMarks(page, origin)
        self.drawGrid(page, origin, background=False)
        self.drawBaselines(page, origin, background=False)

    def drawPageMetaInfoBackground(self, page, origin, path=None):
        """Draws the background meta info on the page, depending on the
        settings -- lets the view draw frame info for debugging, in case
        view.showFrame == True and self.isPage or if self.showFrame.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> path = '_export/PageMetaInfo.pdf'
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=context)
        >>> #doc.view.padding # result is (0, 0, 0, 0), shouldn't be 30pt?
        >>> page = doc[1]
        >>> #page.view.padding
        >>> # result is (0, 0, 0, 0), shouldn't be 30pt?
        >>> view = doc.getView()
        >>> view.showGrid = [GRID_COL, GRID_ROW]
        >>> view.drawPageMetaInfo(page, (0, 0), path)
        """
        self.drawGrid(page, origin, background=True)
        self.drawBaselines(page, origin, background=True)
        self.drawFlowConnections(page, origin)

    def drawFrame(self, e, origin):
        """Draws the page frame if the the flag is on and if there ie padding
        enough to show other meta info. Otherwise the padding is truncated to
        0: no use to draw the frame.

        Note that drawing a frame around a page or element here is for viewing
        purposes only. Actual frame (stroke) drawing of an element is done
        by the element itself.

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
                self.pl >= self.viewMinInfoPadding and \
                self.pr >= self.viewMinInfoPadding and \
                self.pt >= self.viewMinInfoPadding and \
                self.pb >= self.viewMinInfoPadding:

            # TODO: May need to be scaled, as self.drawPadding does.
            ox, oy = point2D(origin)
            context = self.context
            context.fill(noColor)

            viewFrameStroke = e.viewFrameStroke or \
                    self.viewFrameStroke or \
                    self.DEFAULT_STROKE_COLOR

            viewFrameStrokeWidth = e.viewFrameStrokeWidth or \
                    self.viewFrameStrokeWidth or \
                    self.DEFAULT_STROKE_WIDTH

            context.stroke(viewFrameStroke, viewFrameStrokeWidth)
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
        """Draws the page frame of its current padding.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showPadding = True
        >>> view.drawPadding(e, (0, 0))
        """
        e_pt, e_pr, e_pb, e_pl = e.padding

        if ((self.showPadding and e.isPage) or e.showPadding) and \
                (e_pt or e_pr or e_pb or e_pl):
            context = self.context
            p = origin
            px, py = point2D(e._applyScale(self, p))
            viewPaddingStroke = e.viewPaddingStroke or \
                    self.viewPaddingStroke or \
                    self.DEFAULT_STROKE_COLOR
            viewPaddingStrokeWidth = e.viewPaddingStrokeWidth or \
                    self.viewPaddingStrokeWidth or \
                    self.DEFAULT_STROKE_WIDTH
            context.fill(noColor)
            context.stroke(viewPaddingStroke, viewPaddingStrokeWidth)

            context.rect(px + e_pl, py + e_pb, e.w - e_pl - e_pr, e.h - e_pt - e_pb)
            e._restoreScale(self)

    def drawMargin(self, e, origin):
        """Draws the page frame of its current margin.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
        >>> view = PageView(context=context, style=style)
        >>> view.showMargin = True
        >>> view.drawMargin(e, (0, 0))
        """
        e_mt, e_mr, e_mb, e_ml = e.margin

        if ((self.showMargin and e.isPage) or e.showMargin) and \
                (e_mt or e_mr or e_mb or e_ml):
            context = self.context

            if e.isPage:
                p = pointOffset(e.origin, origin)
            else:
                p = origin

            px, py = point2D(e._applyScale(self, p))
            viewMarginStroke = e.viewMarginStroke or \
                    self.viewMarginStroke or \
                    self.DEFAULT_STROKE_COLOR
            viewMarginStrokeWidth = e.viewMarginStrokeWidth or \
                    self.viewMarginStrokeWidth or \
                    self.DEFAULT_STROKE_WIDTH

            context.fill(noColor)
            context.stroke(viewMarginStroke, viewMarginStrokeWidth)

            context.rect(px - e_ml, py - e_mb, e.w + e_ml + e_mr,
                        e.h + e_mt + e_mb)

            e._restoreScale(self)

    def drawNameInfo(self, e, origin, path):
        """Draws additional document information, color markers, page number,
        date, version, etc. outside the page frame, if drawing crop marks.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
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
            cmSize = self.css('viewCropMarkSize')
            cmSize -= cmDistance
            #cmSize = self.css('viewCropMarkSize') - cmDistance
            fontSize = self.css('viewNameFontSize')
            font = self.css('viewNameFont')
            s = self.getNameString(e, path)
            bs = self.context.newString(s, style=dict(font=font,
                textFill=blackColor, fontSize=fontSize))
            tw, th = bs.textSize

            # Draw on top of page.
            x = self.pl + cmDistance
            y = self.pb + e.h - cmDistance + th * 1.5
            #self.context.stroke(registrationColor, 0.5)
            #self.context.line((x, y), (x + tw, y))
            cropmarkDistance = self.css('viewCropMarkDistance', pt(12))
            self.context.drawString(bs, (x, y+cropmarkDistance))

    def getNameString(self, e, path):
        """
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> path = '_export/PageNameInfo.pdf'
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> e = Element(style=style)
        >>> e.name = 'ElementName'
        >>> view = PageView(context=context, style=style)
        >>> view.showNameInfo = True
        >>> s = view.getNameString(e, '/test/path')
        >>> s.endswith('path')
        True
        """
        dt = datetime.datetime.now()
        d = dt.strftime("%A, %d. %B %Y %I:%M%p")

        if e.isPage and e.parent is not None:
            # Test if there is a document.
            pn = e.parent.getPageNumber(e)

            # First or only page on this page number, then just show pn[0].
            if pn[1] == 0:
                pn = pn[0]

            # More than one page, then show total.
            if len(e.parent.pages) > 1:
                pn = '%s/%d' % (pn, len(e.parent.pages))

            title = e.parent.name or e.parent.title or 'Untitled'
            s = 'Page %s | %s | %s' % (pn, d, title)

        else:
            # Otherwise always page number #1.
            pn = 1
            title = 'Untitled'
            s = 'Element %s | %s' % (d, title)

        if e.name and e.name != 'default':
            s += ' | %s' % e.name

        if path is not None:
            # We're only interested in the file name.
             s += ' | %s' % path.split('/')[-1]

        return s


    #   D R A W I N G  F L O W S

    def drawFlowConnections(self, e, origin):
        """If rootStyle.showFlowConnections is True, draw the flow connections
        on the page, using their stroke / width settings of the style. Only
        works for nested elements"""
        context = self.context
        p = pointOffset(e.origin, origin)
        p = e._applyScale(self, p)

        # Ignore z-axis for now.
        px, py, _ = p = e._applyAlignment(p)

        if (self.showFlowConnections and e.isPage) or e.showFlowConnections:
            #self.css('viewFlowCurvatureFactor', 0.15)
            fmf = 0.15

            for startE in e.elements:
                nextE = startE.next
                print('drawFlow', nextE)

                if nextE is not None:
                    # For all the flow sequences found in the page, draw flow
                    # arrows at offset (ox, oy).
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
                    #print('moveto', sx, sy)
                    context.curveTo((xb1, yb1), (xb2, yb2), (nx, ny))
                    #((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
                    context.drawPath()

    def drawArrow(self, e, xs, ys, xt, yt, onText=1, startMarker=False,
            endMarker=False, fms=None, fmf=None, fill=noColor, stroke=noColor,
            strokeWidth=None):
        """Draw curved arrow marker between the two points.

        TODO: duplicate of pagebot.toolbox.drawing.drawArrow()?
        TODO: move to context for reuse.
        """
        context = self.context

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
        # End in middle of arrow head.
        context.curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2))
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
            self.context.fill(color(random(), random(), random(), 0.3))
            self.context.rect(x-ml, y, max(2,ml), e.h)
            self.context.rect(x+e.w, y, max(1,mr), e.h)
            self.context.rect(x-ml, y-mb, ml+e.w+mr, max(1,mb))
            self.context.rect(x-ml, y+e.h, ml+e.w+mr, max(1,mt))

    def drawElementInfo(self, e, origin):
        """For debugging this will make the elements show their info.
        Collect the (e, origin), so we can later draw all info, after the main
        drawing has been done.

        TODO: finish and test.
        """

        #if not e.eId in self.elementsNeedingInfo:
        if (self.showElementInfo and e.isPage) or e.showElementInfo:
            self.elementsNeedingInfo[e.eId] = (e, origin)
            self._drawElementsNeedingInfo(e)

    def _drawElementsNeedingInfo(self, e):
        for e, origin in self.elementsNeedingInfo.values():
            p = pointOffset(e.origin, origin)
            p = e._applyScale(self, p)
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            pw, ph = e.w, e.h

            if (self.showElementInfo and e.isPage) or e.showElementInfo:
                self.drawInfoBox(e, px, py, pw, ph)

            if (self.showDimensions and e.isPage) or e.showDimensions:
                self.drawDimensions(px, py, pw, ph)

            e._restoreScale(self)

    def drawInfoBox(self, e, px, py, pw, ph):
        """Draw box with element info."""
        style = dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'),
                    leading=self.css('viewInfoLeading'),
                    textFill=color(0.1))
        bs = self.context.newString(str(e), style=style)
        tw, th = bs.textSize

        # Padding in box and shadow offset.
        Pd = 4

        # Make info box outdent the element. Keeping shadow on the
        # element top left corner.
        tpx = px - Pd/2
        tpy = py + e.h - th - Pd

        # Tiny shadow
        self.context.fill(color(0.3, 0.3, 0.3, 0.5))
        self.context.stroke(noColor)
        self.context.rect(tpx+Pd/2, tpy, tw+2*Pd, th+1.5*Pd)
        # Frame
        self.context.fill(self.css('viewInfoFill'))
        self.context.stroke(color(0.3), w=pt(0.25))
        self.context.rect(tpx, tpy, tw+2.5*Pd, th+1.5*Pd)
        self.context.text(bs, (tpx+Pd, tpy+th))

    def drawDimensions(self, px, py, pw, ph):
        """Draws width and height measures."""
        # TODO: Make separate arrow function and improve positions.

        self.context.fill(noColor)
        self.context.stroke(blackColor, w=pt(0.25))
        S = self.css('viewInfoOriginMarkerSize', pt(5))

        # Horizontal measure
        self.context.line((px,    py - 0.5*S), (px,      py - 3.5*S))
        self.context.line((px+pw, py - 0.5*S), (px+pw,   py - 3.5*S))
        self.context.line((px,    py - 2*S),   (px+pw,   py - 2*S))

        # Arrow heads
        self.context.line((px,    py - 2*S),   (px+S,    py - 1.5*S))
        self.context.line((px,    py - 2*S),   (px+S,    py - 2.5*S))
        self.context.line((px+pw, py - 2*S),   (px+pw-S, py - 1.5*S))
        self.context.line((px+pw, py - 2*S),   (px+pw-S, py - 2.5*S))

        bs = self.context.newString(str(pw),
                style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'),
                    leading=self.css('viewInfoLeading'),
                    textFill=color(0.1)))
        tw, th = bs.textSize
        self.context.text(bs, (px + pw/2 - tw/2, py-1.5*S))

        # Vertical measure
        self.context.line((px+pw+0.5*S, py),    (px+pw+3.5*S, py))
        self.context.line((px+pw+0.5*S, py+ph), (px+pw+3.5*S, py+ph))
        self.context.line((px+pw+2*S,   py),    (px+pw+2*S,   py+ph))

        # Arrow heads
        self.context.line((px+pw+2*S, py+ph),   (px+pw+2.5*S, py+ph-S))
        self.context.line((px+pw+2*S, py+ph),   (px+pw+1.5*S, py+ph-S))
        self.context.line((px+pw+2*S, py),      (px+pw+2.5*S, py+S))
        self.context.line((px+pw+2*S, py),      (px+pw+1.5*S, py+S))

        bs = self.context.newString(str(ph),
                style=dict(font=self.css('viewInfoFont'),
                    fontSize=self.css('viewInfoFontSize'),
                    leading=self.css('viewInfoLeading'),
                    textFill=color(0.1)))
        tw, th = bs.textSize
        self.context.text(bs, (px+pw+2*S-tw/2, py+ph/2))

    def drawElementOrigin(self, e, origin):
        # Draw origin of the element
        if not (self.showOrigin or e.showOrigin):
            return

        context = self.context
        px, py, _ = pointOffset(e.origin, origin)
        S = e.css('viewInfoOriginMarkerSize', pt(3))
        fill = e.css('viewInfoOriginMarkerFill', noColor)
        stroke = e.css('viewInfoOriginMarkerStroke', blackColor)
        width = e.css('viewInfoOriginMarkerStrokeWidth', pt(0.25))

        # Transparent fill, so we can see the marker on dark backgrounds.
        context.fill(fill)
        context.stroke(stroke, width)
        context.oval(px-S, py-S, 2*S, 2*S)
        context.line((px-S, py), (px+S, py))
        context.line((px, py-S), (px, py+S))

        if (self.showDimensions and e.isPage) or e.showDimensions:
            msg = 'x: %s, y: %s, w: %s, h: %s' % (e.x, e.y, e.w, e.h)
            style = dict(font=self.css('viewInfoFont'),
                        fontSize=self.css('viewInfoFontSize'),
                        leading=self.css('viewInfoLeading'),
                        textFill=color(0.1))
            bs = context.newString(msg, style=style)

            w, h = bs.textSize
            context.drawString(bs, (px, py + S*1.5))

    def drawMissingElementRect(self, e, origin):
        """When designing templates and pages, this will draw a filled
        rectangle on the element bounding box (if self.css('missingElementFill'
        is defined) and a cross, indicating that this element has missing
        content, for example when an image is missing. Only draw if the list
        self.showGrid contains proper types of grid names.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element(style=style)
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
        """Draws a grid of lines and / or rectangles if colors are set in the
        style. Normally origin is ORIGIN pt(0, 0, 0), but it's possible to give
        the grid a fixed offset.

        If types self.showGrid is set, display the type of grid in forground
        for (GRID_COL, GRID_ROW, GRID_SQR) and draw in background for
        (GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG)

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
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

        context = self.context

        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        # Drawing the grid as vertical lines. Check on foreground / background
        # flags.
        if (background and GRID_COL_BG in showGrid) or \
                (not background and GRID_COL in showGrid):
            # Set color for vertical grid lines.
            context.fill(noColor)

            # Use local element color setting, otherwise find by view.css.
            gridStrokeColor = e.style.get('viewGridStrokeY',
                    self.css('viewGridStrokeY', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthY',
                    self.css('viewGridStrokeWidthY',
                        self.DEFAULT_STROKE_WIDTH))
            context.stroke(gridStrokeColor, gridStrokeWidth)
            gridX = e.gridX

            if gridX:
                x = px + e.pl # Position on left padding of page/e
                y1 = py + e.pb
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
                    else:
                        x += cw

        # Drawing the grid as horizontal lines. Check foreground / background
        # flags.
        if (background and GRID_ROW_BG in showGrid) or (not background and GRID_ROW in showGrid):
            # Set color for vertical grid lines
            context.fill(noColor)
            # Use local element color setting, otherwise find by view.css
            gridStrokeColor = e.style.get('viewGridStrokeX', self.css('viewGridStrokeX', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthX', self.css('viewGridStrokeWidthX', self.DEFAULT_STROKE_WIDTH))
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
                    else:
                        y += ch

        # Drawing the grid as rectangles. Check foreground / background flags.
        if (background and GRID_SQR_BG in showGrid) or (not background and GRID_SQR in showGrid):
            # Set color for grid rectangles
            # Use local element color setting, otherwise find by view.css
            gridFillColor = e.style.get('gridFillColor', self.css('gridFillColor', noColor))
            gridStrokeColor = e.style.get('viewGridStrokeX', self.css('viewGridStrokeX', noColor))
            gridStrokeWidth = e.style.get('viewGridStrokeWidthX', self.css('viewGridStrokeWidthX', self.DEFAULT_STROKE_WIDTH))
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
        by Text with style values baselineColor and baselineWidth.

        In this method is called by an element, instead of self, the show
        attribute is a way to overwrite the setting of self.showBaselineGrid

        NOTE: Text elements have their own baseline drawing method.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.elements.element import Element
        >>> from pagebot.style import getRootStyle
        >>> from pagebot.document import Document
        >>> style = getRootStyle() # Get default values
        >>> e = Element(style=style) # Works on generic elements as well as pages.
        >>> doc = Document(name='TestDoc', startPage=50, autoPages=100, context=context)
        >>> pages = doc.pages
        >>> len(pages)
        100
        >>> page = doc[50]
        >>> page
        <Page #50 default (1000pt, 1000pt)>
        >>> view = doc.view
        >>> view = PageView(context=context, style=style)
        >>> view.showBaselineGrid = [BASE_LINE, BASE_INDEX_LEFT, BASE_Y_LEFT]
        >>> #view.drawBaselines(e, pt(0, 0))
        >>> doc.build()
        """
        show = e.showBaselineGrid or self.showBaselineGrid

        # Sets the default, in case not drawing or show is True.
        if not show:
            return

        context = self.context
        p = pointOffset(e.origin, origin)
        p = self._applyScale(e, p)

        # Ignore z-axis for now.
        px, py, _ = e._applyAlignment(p)

        # Get the baseline grid of this element.
        baselineGrid = e.baselineGrid

        # Index size depends on baseline.
        indexFontSize = max(9, min(16, baselineGrid*0.5))

        # Gutter between index marker and element padding
        indexGutter = baselineGrid/4

        # Collect all baseline positions on e.
        baselineYs = []

        # Page origin is at the bottom.
        startY = e.h - (e.baselineGridStart or e.pt)
        # Assumes origin at bottom for context drawing.
        oy = yy = startY

        # Run over the the padding bottom until page side
        while yy > 0:
            baselineYs.append(yy)
            yy -= baselineGrid

        baselineColor = e.style.get('baselineColor', self.css('baselineColor', DEFAULT_BASELINE_COLOR))
        baselineWidth = e.style.get('baselineWidth', self.css('baselineWidth', DEFAULT_BASELINE_WIDTH))

        # Format of line numbers.
        style = dict(font=e.css('viewMarkerFont'), #xTextAlign=RIGHT,
            fontSize=indexFontSize, stroke=noColor, textFill=baselineColor)

        context.fill(noColor)
        context.stroke(baselineColor, baselineWidth)

        for lineIndex, oy in enumerate(baselineYs):
            tl = tr = None

            #if not background:
            if BASE_INDEX_LEFT in show:
                # Shows line baseline index.
                tl = repr(lineIndex)
            elif BASE_Y_LEFT in show:
                # Show vertical position marker.
                tl = repr(e.h - oy)

            if BASE_INDEX_RIGHT in show:
                # Shows line baseline index.
                tr = repr(lineIndex)
            elif BASE_Y_RIGHT in show:
                # Show vertical position marker.
                tr = repr(e.h - oy)

            bsl = context.newString(tl, style=style)
            bsr = context.newString(tr, style=style)

            twl, thl = bsl.textSize
            twr, thr = bsr.textSize

            if BASE_INSIDE in show:
                if tl:
                    x = px + e.pl + indexGutter - twl*2
                    y = py + oy - thl/5
                    w = twl*2
                    h = thl
                    context.textBox(bsl, (x, y, w, h))
                if tr:
                    context.textBox(bsr, (px + e.pl + e.pw - twr - indexGutter, py + oy - thr/5, twr*2, thr))
                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    context.line((px + e.pl + 2*indexGutter + twl*2, py + oy), (px + e.pw - 2*indexGutter - twr, py + oy))
            else:
                if tl:
                    x = px + e.pl - twl - indexGutter
                    y = py + oy - thl/5
                    w = twl * 2
                    h = thl
                    r = (x, y, w, h)
                    context.fill(None)
                    of = context.textBox(bsl, r)
                    context.stroke((1, 0, 0))
                    # For debugging.
                    context.rect(x, y, w, h)
                    #context.marker(x, y)

                if tr:
                    context.textBox(bsr, (px + e.pl + e.pw + indexGutter, py + oy - thr/5, twr*2, thr))

                if (background and BASE_LINE_BG in show) or (not background and BASE_LINE in show):
                    context.stroke((0, 1, 0))
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

        # Draws CMYK all on, color(cmyk=1).
        context.stroke(registrationColor, w=cmStrokeWidth)

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
        >>> # Get default values.
        >>> style = getRootStyle()
        >>> # Works on generic elements as well as pages.
        >>> e = Element()
        >>> view = PageView(context=context, style=style)
        >>> # Boolean expands into set.
        >>> view.showRegistrationMarks = True
        >>> sorted(view.showRegistrationMarks)
        ['bottom', 'left', 'right', 'top']
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
        >>> view.showCropMarks = True # Boolean expand into full set by property
        >>> sorted(view.showCropMarks)
        ['bottom', 'bottomFold', 'left', 'leftFold', 'right', 'rightFold', 'top', 'topFold']
        >>> view.folds = [(mm(40), mm(60))]
        >>> view.drawCropMarks(e, pt(0, 0))
        """
        # Answers a set of {TOP, RIGHT, BOTTOM, LEFT} flags.
        if e.isPage and self.showCropMarks:
            showCropMarks = self.showCropMarks
        else:
            showCropMarks = e.showCropMarks

        if showCropMarks:
            context = self.context

            x, y = point2D(origin) # Ignore z-axus for now.
            w, h = e.size
            folds = e.folds or self.css('folds')

            # From the side, compare with bleed.
            cmDistance = e.css('viewCropMarkDistance')
            if not cmDistance:
                cmDistance = self.css('viewCropMarkDistance', pt(12))

            cmSize = e.css('viewCropMarkSize')
            if not cmSize:
                cmSize = self.css('viewCropMarkSize', pt(32))

            cmStrokeWidth = e.css('viewCropMarkStrokeWidth')
            if not cmStrokeWidth:
                cmStrokeWidth = self.css('viewCropMarkStrokeWidth', pt(0.25))

            context.fill(noColor)
            # For CMYK, draw all colors color(cmyk=1)).
            context.stroke(registrationColor, w=cmStrokeWidth)

            # Calculate distances, comparing to bleeds.
            cmLeft = max(e.bleedLeft, self.bleedLeft, cmDistance)
            cmRight = max(e.bleedRight, self.bleedRight, cmDistance)
            cmBottom = max(e.bleedBottom, self.bleedBottom, cmDistance)
            cmTop = max(e.bleedTop, self.bleedTop, cmDistance)

            # Left.
            if LEFT in showCropMarks:
                x0  = x - cmLeft
                x1 = x - cmLeft - cmSize
                context.line((x0, y), (x1, y))
                context.line((x0, y + h), (x1, y + h))

            # Bottom.
            if BOTTOM in showCropMarks:
                context.line((x, y - cmBottom), (x, y - cmBottom - cmSize))
                context.line((x + w, y - cmBottom), (x + w, y - cmBottom - cmSize))

            # Right.
            if RIGHT in showCropMarks:
                x0 = x + w + cmRight
                x1 = x + w + cmRight + cmSize
                context.line((x0, y), (x1, y))
                context.line((x0, y + h), (x1, y + h))

            # Top.
            if TOP in showCropMarks:
                y0 = y + h + cmTop
                y1 = y + h + cmTop + cmSize
                context.line((x, y0), (x, y1))
                context.line((x + w, y0), (x + w, y1))

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
        """Draw the color bars for offset printing color calibration if there
        is less than self.viewMinInfoPadding of space in view left padding.
        """
        # TODO Get this to work for content of the parameter set.
        showColorBars = e.showColorBars or (e.isPage and self.showColorBars)
        if not showColorBars or self.pl < self.viewMinInfoPadding:
            return # Nothing to do.
        ox, oy = point2D(origin)

        # TODO: Add more types of color bars and switch from scaling PDF to
        # drawing them by script.
        if ECI_GrayConL in showColorBars:
            path = getResourcesPath() + '/' + ECI_GrayConL

            if COLORBAR_LEFT in showColorBars:
                x = ox - self.pl + pt(3)
                self.context.image(path, p=(x, oy), w=e.w, h=e.h)

            if COLORBAR_RIGHT in showColorBars: # TODO: Does not generate the right position?
                x = ox + e.w + self.pr * 2/3
                self.context.image(path, p=(x, oy), w=e.w, h=e.h)

    #   D R A W B O T  S U P P O R T

    # The context-methods are used, in case the view itself is placed in a layout.

    def build_drawBot(self, view, origin, **kwargs):
        """This method is called if the view is used as a placeable element
        inside another element, such as a Page or Template.

        TODO: check OS, check if DrawBot is installed.
        """
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

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
