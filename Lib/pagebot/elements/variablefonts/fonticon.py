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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#	  fonticon.py
#
#     Draw the icon with optional information of the included font.
#
from pagebot.elements import Element
from pagebot.toolbox.transformer import pointOffset

class FontIcon(Element): 
    u"""Showing the specified font(sub variable font) in the form of an icon 
    showing optional information in different sizes and styles.
    
    >>> from pagebot.fonttoolbox.objects.font import getFont
    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> path = getTestFontsPath() + '/google/roboto/Roboto-Regular.ttf' # We know this exists in the PageBot repository
    >>> font = getFont(path)
    >>> fi = FontIcon(font, w=120, h=160)
    >>> fi.title
    u'Roboto Regular'
    >>> fi.size
    (120, 160, 1)

    """
    W = 30
    H = 40
    L = 2
    E = 8
    LABEL_RTRACKING = 0.02
    LABEL_RLEADING = 1.3

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, line=None,
            labelFont=None, labelFontSize=None, titleFont=None, titleFontSize=None, show=True, **kwargs):
        u"""    
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Regular.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> fi = FontIcon(font, w=120, h=160, parent=page)
        >>> doc.export('_export/FontIconTest.png')
        """

        Element.__init__(self,  **kwargs)
        self.f = f # Font instance
        self.title = title or "%s %s" % (f.info.familyName, f.info.styleName) 
        self.titleFont = titleFont, labelFont or f 
        self.titleFontSize = 28
        self.labelFont = labelFont or f
        self.labelFontSize = labelFontSize or 10
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.scale = s
        self.show = show

    def _get_ih(self):
        u"""Answer scaled height of the plain icon without name label."""
        return self.H*self.scale
    ih = property(_get_ih)

    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 
        self.context.fill(0)
        self.context.rect(0, 0, 100, 100)
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def draw(self, orgX, orgY):
        if not self.show:
            return
        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY

        c.newPath()
        c.moveTo((0, 0))
        c.lineTo((0, h))
        c.lineTo((w-e, h))
        c.lineTo((w, h-e))
        c.lineTo((w, 0))
        c.lineTo((0, 0))
        c.closePath()
        c.moveTo((w-e, h))
        c.lineTo((w-e, h-e))
        c.lineTo((w, h-e))

        c.save()
        c.fill(1)
        c.stroke(0, self.line)
        c.translate(x, y)
        c.drawPath()
        labelSize = e
        bs = c.newString(self.c,
                               style=dict(font=self.f.path,
                                          textFill=0,
                                          fontSize=h*2/3))
        tw, th = bs.textSize()
        c.text(bs, (w/2-tw/2, h/2-th/3.2))

        if self.title:
            bs = c.newString(self.title,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, self.ih+th/2))

        y = -self.LABEL_RLEADING*labelSize
        if self.name:
            bs = c.newString(self.name,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, y))
            y -= self.LABEL_RLEADING*labelSize
        if self.label:
            bs = c.newString(self.label,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, y))
        c.restore()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
