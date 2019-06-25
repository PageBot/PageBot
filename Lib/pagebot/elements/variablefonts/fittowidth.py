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
#	  fonticon.py
#
#     Draw the icon with optional information of the included font.
#
from pagebot.elements import Element
from pagebot.toolbox.units import pointOffset, em, upt
from pagebot.toolbox.color import noColor, blackColor

class FontIcon(Element): 
    """Showing the specified font(sub variable font) in the form of an icon 
    showing optional information in different sizes and styles.
    
    >>> from pagebot.fonttoolbox.objects.font import getFont
    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> path = getTestFontsPath() + '/google/roboto/Roboto-Regular.ttf' # We know this exists in the PageBot repository
    >>> font = getFont(path)
    >>> fi = FontIcon(font, w=120, h=160, title="Roboto Regular")
    >>> fi.title
    'Roboto Regular'
    >>> fi.size
    (120pt, 160pt)

    """
    LABEL_RTRACKING = em(0.02)
    LABEL_RLEADING = em(1.3)

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, strokeWidth=None, stroke=noColor,
            earSize=None, earLeft=True, earFill=None, cFill=0, cStroke=None, cStrokeWidth=None,
            labelFont=None, labelFontSize=None, titleFont=None, titleFontSize=None, show=True, **kwargs):
        """    
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.elements import newRect
        >>> from pagebot.document import Document
        >>> from pagebot.toolbox.color import color, whiteColor, blackColor
        >>> c = DrawBotContext()
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Regular.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> iw, ih = w/4, h/4
        >>> x, y = w/8, h/8
        >>> fi = FontIcon(font, x=x, y=y, w=iw, h=ih, name="40k", earSize=0.3, earLeft=True, parent=page, stroke=0, strokeWidth=3)
        >>> bg = newRect(x=w/2, w=w/2, h=h/2, fill=blackColor,parent=page)
        >>> fi = FontIcon(font, x=x, y=y, w=iw, h=ih, name="40k", c="H", cFill=0.5, earSize=0.3, earLeft=True, earFill=None, fill=color(1,0,0,0.5), parent=bg, stroke=whiteColor, strokeWidth=3)
        >>> doc.export('_export/FontIconTest.pdf')
        """

        Element.__init__(self,  **kwargs)
        self.f = f # Font instance
        if title is not None:
            self.title = title or "%s %s" % (f.info.familyName, f.info.styleName) 
        self.titleFont = titleFont, labelFont or f 
        self.titleFontSize = 28
        self.labelFont = labelFont or f
        self.labelFontSize = labelFontSize or 10
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.cFill = cFill
        self.cStroke = cStroke
        self.cStrokeWidth = cStrokeWidth
        self.scale = s
        self.show = show
        if stroke is not None:
            self.style["stroke"] = stroke
        if strokeWidth is not None:
            self.style["strokeWidth"] = strokeWidth
        self.earSize = earSize or 0.25 # 1/4 of width
        self.earLeft = earLeft
        if earFill is None:
            earFill = self.css("fill")
        self.earFill = earFill 


    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.draw(view, p)
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def draw(self, view, p):
        if not self.show:
            return
        w = self.w # Width of the icon
        h = self.h # Height of the icon
        e = self.earSize*w # Ear size fraction of the width

        x,y = p[0], p[1]
        c = self.context

        c.newPath()
        c.moveTo((0, 0))
        if self.earLeft: 
            c.lineTo((0, h-e))
            c.lineTo((e, h))
            c.lineTo((w, h))
            
        else:
            c.lineTo((0, h))
            c.lineTo((w-e, h))
            c.lineTo((w, h-e))
        c.lineTo((w, 0))
        c.lineTo((0, 0))
        c.closePath()
        c.save()
        c.fill(self.css("fill"))
        c.stroke(self.css("stroke"), self.css("strokeWidth"))
        c.translate(x, y)
        c.drawPath()

        c.newPath()
        if self.earLeft:
            #draw ear
            c.moveTo((e, h))
            c.lineTo((e, h-e))
            c.lineTo((0, h-e))
            c.lineTo((e, h))

        else:
            #draw ear
            c.moveTo((w-e, h))
            c.lineTo((w-e, h-e))
            c.lineTo((w, h-e))
            c.lineTo((w-e, h))
        c.closePath()
        c.fill(self.earFill)
        c.lineJoin("bevel")
        c.drawPath()

        labelSize = e
        bs = c.newString(self.c,
                               style=dict(font=self.f.path,
                                          textFill=self.cFill,
                                          textStroke=self.cStroke,
                                          textStrokeWidth=self.cStrokeWidth,
                                          fontSize=h*2/3))
        tw, th = bs.size
        c.text(bs, (w/2-tw/2, h/2-th/3.2))

        if self.title:
            bs = c.newString(self.title,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            c.text(bs, (w/2-tw/2, self.h+th/2))

        y -= upt(self.LABEL_RLEADING, base=labelSize)
        if self.name:
            bs = c.newString(self.name,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            c.text(bs, (w/2-tw/2, y))
            y -= upt(self.LABEL_RLEADING, base=labelSize)
        if self.label:
            bs = c.newString(self.label,
                                   style=dict(font=self.labelFont.path,
                                              textFill=blackColor,
                                              tracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.size
            c.text(bs, (w/2-tw/2, y))
        c.restore()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
