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
from __future__ import division
from datetime import datetime
from math import atan2, radians, degrees, cos, sin

from drawBot import saveImage, newPage, rect, oval, line, newPath, moveTo, lineTo, drawPath, save, restore, scale, textSize, \
        FormattedString, cmykStroke, text, fill, strokeWidth, curveTo, closePath

from pagebot import setFillColor, setStrokeColor
from pagebot.elements.element import Element
from pagebot.style import makeStyle, getRootStyle, NO_COLOR, RIGHT
from pagebot.toolbox.transformer import pointOffset, obj2StyleId, point3D, point2S
from pagebot import getFormattedString, setStrokeColor, setFillColor

class View(Element):
    u"""A View is just another kind of container, kept by document to make a certain presentation of the page tree."""
    viewId = 'View'

    def __init__(self, w=None, h=None, parent=None, **kwargs):
        Element.__init__(self, parent=parent, **kwargs)
        if not w and self.parent:
            w = self.parent.w
        if not h and self.parent:
            h = self.parent.h
        self.w = w
        self.h = h
        self._initializeControls()
        self.setControls()

    def _initializeControls(self):
        self.showElementInfo = False
        self.showElementFrame = False
        self.showElementOrigin = False
        self.showElementDimensions = False
        self.showMissingElementRect = True
        # Grid stuff
        self.showGrid = False
        self.showGridColumns = False
        self.showBaselineGrid = False
        # Document/page stuff
        self.showPageCropMarks = False
        self.showPageRegistrationMarks = False
        self.showPageFrame = False
        self.showPageNameInfo = False
        self.showPageMetaInfo = False
        # TextBox stuff
        self.showTextBoxIndex = False # Show the line index number on the left side.
        self.showTextBoxY = False # Show the realtic y-position value if text lines on right side. 
        self.showTextBoxLeading = False # Show distance of leading on the right side.
        self.showTextBoxBaselines = False
        # Flow stuff
        self.showFlowConnections = False
        # Image stuff
        self.showImageReference = False      

    def setControls(self):
        u"""Inheriting views can redefine to alter showing parameters."""
        pass

    MIN_PADDING = 20 # Minimum padding needed to show meta info. Otherwise truncated to 0 and not showing meta info.

    def drawPages(self, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""
        doc = self.parent

        w, h, _ = doc.getMaxPageSizes(pageSelection)
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

            newPage(w, h) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
            # Let the page draw itself on the current DrawBot view port if self.writer is None.
            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            page.draw(origin, self) 

    def export(self, fileName, pageSelection=None, multiPage=True):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted. The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct the type of
        drawing and export that needs to be done.
        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in special cases, there is not 
        straighforward (or sequential) export of pages, e.g. when generating HTML/CSS. In that case use 
        MyBuilder(document).export(fileName), the builder is responsible to query the document, pages, elements and styles.
        """
        self.drawPages(pageSelection)

        # If rootStyle['frameDuration'] is set and saving as movie or animated gif, 
        # then set the global frame duration.
        frameDuration = self.css('frameDuration')
        if frameDuration is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
            frameDuration(frameDuration)

        # http://www.drawbot.com/content/canvas/saveImage.html
        saveImage(fileName, multipage=multiPage)

    #   D R A W I N G  P A G E  M E T A  I N F O

    def drawPageMetaInfo(self, page, origin):
        self.drawPageFrame(page, origin)
        self.drawPageNameInfo(page, origin)
        self.drawPageRegistrationMarks(page, origin)
        self.drawPageCropMarks(page, origin)
        self.drawGrid(page, origin)
        self.drawBaselineGrid(page, origin)

    def drawPageFrame(self, page, origin):
        u"""Draw the page frame if the the flag is on and  if there ie padding enough to show other meta info.
        Otherwise the padding is truncated to 0: no use to draw the frame."""
        if self.showPageFrame and \
                self.pl > self.MIN_PADDING and self.pr > self.MIN_PADDING and \
                self.pt > self.MIN_PADDING and self.pb > self.MIN_PADDING:
            self._drawElementFrame(page, origin)

    def drawPageNameInfo(self, page, origin):
        u"""Draw additional document information, color markers, page number, date, version, etc.
        outside the page frame, if drawing crop marks."""
        if self.showPageNameInfo:
            bleed = self.css('bleed')
            cms = self.css('viewCropMarkSize') - bleed
            fontSize = self.css('viewPageNameFontSize')
            dt = datetime.now()
            d = dt.strftime("%A, %d. %B %Y %I:%M%p")
            s = 'Page %s | %s | %s' % (page.parent.getPageNumber(page), d, page.parent.title or 'Untitled')
            if page.name:
                s += ' | ' + page.name
            fs = FormattedString(s, font=self.css('viewPageNameFont'), fill=0, fontSize=fontSize)
            text(fs, (self.pl + bleed, self.pb + page.h + cms - fontSize*2)) # Draw on top of page.

    #   D R A W I N G  F L O W S

    def drawFlowConnections(self, e, origin):
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
                stroke = self.css('viewFlowConnectionStroke2', NO_COLOR)
            else:
                stroke = self.css('viewFlowConnectionStroke1', NO_COLOR)
        if strokeWidth is None:
            strokeWidth = self.css('viewFlowConnectionStrokeWidth', 0.5)
        
        setStrokeColor(stroke, strokeWidth)
        if startMarker:
            if fill is None:
                fill = self.css('viewFlowMarkerFill', NO_COLOR)
            setFillColor(fill)
            oval(xs - fms, ys - fms, 2 * fms, 2 * fms)
        
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
        newPath()
        setFillColor(None)
        moveTo((xs, ys))
        curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
        drawPath()

        #  Draw the arrow head.
        newPath()
        setFillColor(stroke)
        setStrokeColor(None)
        moveTo((xt, yt))
        lineTo((ax1, ay1))
        lineTo((ax2, ay2))
        closePath()
        drawPath()

        if endMarker:
            setFillColor(self.css('viewFlowMarkerFill', NO_COLOR))
            oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

    #   D R A W I N G  E L E M E N T  

    def _drawElementFrame(self, e, origin):
        u"""When designing templates and pages, this will draw a rectangle on the element
        bounding box if self.css('showElementBox') is True."""
        p = pointOffset(e.oPoint, origin)
        p = self._applyScale(p)   
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        setFillColor(self.css('viewFrameFill', NO_COLOR))
        setStrokeColor(self.css('viewFrameStroke', NO_COLOR), self.css('viewFrameStrokeWidth'))
        rect(px, py, e.w, e.h)

        self._restoreScale()

    def drawElementFrame(self, e, origin):
        if self.showElementFrame:
            self._drawElementFrame(e, origin)

    def drawElementMetaInfo(self, e, origin):
        self.drawElementInfo(e, origin)
        self.drawElementOrigin(e, origin)
        
    def drawElementInfo(self, e, origin):
        u"""For debugging this will make the elements show their info. The css flag "showElementOrigin"
        defines if the origin marker of an element is drawn."""
        p = pointOffset(e.oPoint, origin)
        p = e._applyScale(p)    
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
        if self.showElementInfo:
            # Draw box with element info.
            fs = getFormattedString(e.getElementInfoString(), style=dict(font=self.css('viewInfoFont'), 
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=0.1))
            tw, th = textSize(fs)
            Pd = 4 # Padding in box and shadow offset.
            tpx = px - Pd/2 # Make info box outdent the element. Keeping shadow on the element top left corner.
            tpy = py + e.h - th - Pd
            # Tiny shadow
            setFillColor((0.3, 0.3, 0.3, 0.5))
            setStrokeColor(None)
            rect(tpx+Pd/2, tpy, tw+2*Pd, th+1.5*Pd)
            # Frame
            setFillColor(self.css('viewInfoFill'))
            setStrokeColor(0.3, 0.25)
            rect(tpx, tpy, tw+2.5*Pd, th+1.5*Pd)
            text(fs, (tpx+Pd, tpy+1.5*Pd))
            e._restoreScale()

        if 0 and self.showElementDimensions:
            # TODO: Make separate arrow functio and better positions
            # Draw width and height measures
            setFillColor(None)
            setStrokeColor(0, 0.25)
            S = self.css('viewInfoOriginMarkerSize', 4)
            opx, opy, _ = p
            x1, y1, x2, y2 = e.left, e.bottom, e.right, e.top
            line((opx + x1, opy + y1 - S), (opx + x1, opy + y1 - 3*S))
            self.drawArrow(e, opx + x1, opy + y1 - 2*S, opx + x2, opy + y1 - 2*S, True, True, fms=2, fmf=0, stroke=0, strokeWidth=0.25, fill=0)
            line((opx + x2, opy + y1 - S), (opx + x2, opy + y1 - 3*S))

    def drawElementOrigin(self, e, origin):
        px, py, _ = pointOffset(e.oPoint, origin)
        S = self.css('viewInfoOriginMarkerSize', 4)
        if self.showElementOrigin:
            # Draw origin of the element
            setFillColor((0.5,0.5,0.5,0.1)) # Transparant fill, so we can see the marker on dark backgrounds.
            setStrokeColor(0, 0.25)
            oval(px-S, py-S, 2*S, 2*S)
            line((px-S, py), (px+S, py))
            line((px, py-S), (px, py+S))

        if self.showElementDimensions:
            fs = getFormattedString(point2S(e.point3D), style=dict(font=self.css('viewInfoFont'), 
                fontSize=self.css('viewInfoFontSize'), leading=self.css('viewInfoLeading'), textFill=0.1))
            w, h = textSize(fs)
            text(fs, (px - w/2, py + S*1.5))

    def drawMissingElementRect(self, e, origin):
        u"""When designing templates and pages, this will draw a filled rectangle on the element
        bounding box (if self.css('missingElementFill' is defined) and a cross, indicating
        that this element has missing content (as in unused image frames).
        Only draw if self.css('showGrid') is True."""
        if self.showMissingElementRect:

            p = pointOffset(e.point, origin)
            p = e._applyOrigin(p)    
            p = e._applyScale(p)    
            px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.
            self.setShadow()

            sMissingElementFill = self.css('viewMissingElementFill', NO_COLOR)
            if sMissingElementFill is not NO_COLOR:
                setFillColor(sMissingElementFill)
                setStrokeColor(None)
                rect(px, py, self.w, self.h)
            # Draw crossed rectangle.
            setFillColor(None)
            setStrokeColor(0, 0.5)
            rect(px, py, self.w, self.h)
            newPath()
            moveTo((px, py))
            lineTo((px + self.w, py + self.h))
            moveTo((px + self.w, py))
            lineTo((px, py + self.h))
            drawPath()

            self.resetShadow()
            e._restoreScale()

    #   S H A D O W

    def setShadow(self, e):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        shadowOffset = e.css('shadowOffset') # Use DrawBot graphic state switch on shadow mode.
        if shadowOffset is not None:
            save() # DrawBot graphics state push
            shadowBlur = e.css('shadowBlur') # Should be integer.
            shadowFill = e.css('shadowFill') # Should be color, different from NO_COLOR
            shadow(shadowOffset, shadowBlur, shadowFill)

    def resetShadow(self, e):
        u"""Restore the shadow mode of DrawBot. Should be paired with call self._setShadow()."""
        if e.css('shadowOffset') is not None:
            restore() # DrawBot graphics state pop.

    #    G R I D

    def drawGrid(self, e, origin):
        u"""Draw grid of lines and/or rectangles if colors are set in the style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        # Drawing the grid as squares.
        if not self.showGridColumns or not self.self.showGrid:
            return
        p = pointOffset(e.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = e._applyAlignment(p) # Ignore z-axis for now.

        sGridFill = e.css('gridFill', NO_COLOR)
        gutterW = e.gw # Gutter width
        gutterH = e.gh # Gutter height
        columnWidth = e.cw # Column width
        columnHeight = e.ch # Column height
        padL = e.pl # Padding left
        padT = e.pt # Padding top
        padR = e.pr # padding right
        padB = e.pb # padding bottom
        w = e.w
        h = e.h
        if self.showGridColumns and sGridFill is not NO_COLOR:
            setFillColor(sGridFill)
            setStrokeColor(None)
            ox = px + padL
            while ox < w - padR - columnWidth:
                oy = h - padT - columnHeight - gutterH
                while oy >= 0:
                    rect(ox, oy + gutterH, columnWidth, columnHeight)
                    oy -= columnHeight + gutterH
                ox += columnWidth + gutterW
        # Drawing the grid as lines.
        if self.showGrid and self.css('gridStroke', NO_COLOR) is not NO_COLOR:
            setFillColor(None)
            setStrokeColor(self.css('gridStroke', NO_COLOR), self.css('gridStrokeWidth'))
            # TODO: DrawBot align and fill don't work properly now.
            M = 16
            fs = getFormattedString('', self, dict(font='Verdana', xAlign=RIGHT, fontSize=M/2,
                stroke=None, textFill=self.css('gridStroke')))
            ox = px + padL
            index = 0
            oy = h - padT - py
            while ox < px + w - padR:
                newPath()
                moveTo((ox, py))
                lineTo((ox, py + h))
                moveTo((ox + columnWidth, py))
                lineTo((ox + columnWidth, py + h))
                drawPath()
                text(fs+repr(index), (ox + M * 0.3, oy + M / 4))
                index += 1
                ox += columnWidth + gutterW
            index = 0
            while oy > py:
                newPath()
                moveTo((px, oy))
                lineTo((px + w, oy))
                moveTo((px, oy - columnHeight))
                lineTo((px+w, oy - columnHeight))
                drawPath()
                text(fs + repr(index), (px + padL - M / 2, oy - M * 0.6))
                index += 1
                oy -= columnHeight + gutterH

    def drawBaselineGrid(self, e, origin):
        u"""Draw baseline grid if line color is set in the style.
        TODO: Make fixed values part of calculation or part of grid style.
        Normally px and py will be 0, but it's possible to give them a fixed offset."""
        if not self.showBaselineGrid:
            return    
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        oy = self.h - self.css('pt') - py
        line = 0
        M = 16
        # Format of line numbers.
        # TODO: DrawBot align and fill don't work properly now.
        if self.horizontal:
            fs = getFormattedString('', self, dict(font=self.css('fallbackFont','Verdana'), xAlign=RIGHT, 
                fontSize=M/2, stroke=None, textFill=self.css('gridStroke')))
            while oy > self.css('pb', 0):
                setFillColor(None)
                setStrokeColor(self.css('baselineGridStroke', NO_COLOR), self.css('gridStrokeWidth'))
                newPath()
                moveTo((px + M, py + oy))
                lineTo((px + self.parent.w - M, py + oy))
                drawPath()
                text(fs + repr(line), (px + M - 2, py + oy - M * 0.6))
                text(fs + repr(line), (px + self.parent.w - M - 8, py + oy - M * 0.6))
                line += 1 # Increment line index.
                oy -= self.css('baselineGrid') # Next vertical line position of baseline grid.

    #    M A R K E R S

    def _drawPageRegistrationMark(self, page, origin, cmSize, cmStrokeWidth, vertical):
        u"""Draw registration mark as position x, y."""
        x, y = origin
        if vertical:
            dx = cmSize/2
            dy = cmSize
        else:
            dx = cmSize
            dy = cmSize/2
        fill(None)
        cmykStroke(1,1,1,1)
        strokeWidth(cmStrokeWidth)
        newPath()
        # Registration circle
        oval(x - cmSize/4, y - cmSize/4, cmSize/2, cmSize/2)
        # Registration cross, in length of direction.
        moveTo((x - dx, y)) # Horizontal line.
        lineTo((x + dx, y))
        moveTo((x, y + dy)) # Vertical line.
        lineTo((x, y - dy))
        drawPath()

    def drawPageRegistrationMarks(self, page, origin):
        u"""Draw standard registration mark, to show registration of CMYK colors.
        https://en.wikipedia.org/wiki/Printing_registration."""
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
        u"""If the show flag is set, then draw the cropmarks or page frame."""
        if self.showPageCropMarks:
            x, y, _ = point3D(origin) # Ignore z-axus for now.
            w, h = e.w, e.h
            folds = self.css('folds')
            bleed = self.css('bleed')
            cmSize = self.css('viewCropMarkSize')
            cmStrokeWidth = self.css('viewCropMarkStrokeWidth')

            fill(None)
            cmykStroke(1,1,1,1)
            strokeWidth(cmStrokeWidth)
            newPath()
            # Bottom left
            moveTo((x - bleed, y))
            lineTo((x - cmSize, y))
            moveTo((x, y - bleed))
            lineTo((x, y - cmSize))
            # Bottom right
            moveTo((x + w + bleed, y))
            lineTo((x + w + cmSize, y))
            moveTo((x + w, y - bleed))
            lineTo((x + w, y - cmSize))
            # Top left
            moveTo((x - bleed, y + h))
            lineTo((x - cmSize, y + h))
            moveTo((x, y + h + bleed))
            lineTo((x, y + h + cmSize))
            # Top right
            moveTo((x + w + bleed, y + h))
            lineTo((x + w + cmSize, y + h))
            moveTo((x + w, y + h + bleed))
            lineTo((x + w, y + h + cmSize))
            # Any fold lines to draw?
            if folds is not None:
                for fx, fy in folds:
                    if fx is not None:
                        moveTo((x + fx, y - bleed))
                        lineTo((x + fx, y - cmSize))
                        moveTo((x + fx, y + h + bleed))
                        lineTo((x + fx, y + h + cmSize))
                    if fy is not None:
                        moveTo((x - bleed, y + fy))
                        lineTo((x - cmSize, y + fy))
                        moveTo((x + w + bleed, y + fy))
                        lineTo((x + w + cmSize, y + fy))
            drawPath()



