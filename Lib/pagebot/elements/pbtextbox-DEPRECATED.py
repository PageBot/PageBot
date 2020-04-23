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
#     pbtext.py
#
#     Using the DrawBot textBox() instead of text() for better control
#     of alignment, position and leading (in case there are "\n" returns
#     in the string)
#
from pagebot.constants import MIDDLE, BOTTOM, CENTER, RIGHT, DEFAULT_LANGUAGE
from pagebot.elements.pbtextbox import TextBox
from pagebot.toolbox.units import pointOffset, point2D, pt, em, units, uRound, upt

class Text(TextBox):

    def _get_w(self):
        """Answer the calculate width of self.bs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', leading=em(1), fontSize=pt(100))
        >>> bs = context.newString('ABCDEFGH', style)
        >>> e = Text(bs) # Context is taken from bs
        >>> e.w, e.h
        (482.7pt, 100pt)
        >>> e.size
        (482.7pt, 100pt)

        """
        return self.getTextSize()[0]
    def _set_w(self, w):
        pass # Ignore, will aways be overwritten by the width of self.bs
    w = property(_get_w, _set_w)
   
    def _get_h(self):
        """Answer the calculate height of self.bs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', leading=em(1.4), fontSize=pt(100))
        >>> bs = context.newString('ABCDEFGH', style)
        >>> bs.context
        <DrawBotContext>
        >>> e = Text(bs) # Context to calculate size is bs.context
        >>> bs is e.bs # Using the same string as reference.
        True
        >>> e.h # Height includes the leading.
        140pt
        >>> bs.leading = em(1) # Set the leading of e.bs string.
        >>> e.bs.style['leading']
        1em
        >>> e.h # Dynamic calculation by the BabelString and context inside.
        100pt
        """
        return self.getTextSize()[1]
    def _set_h(self, h):
        pass # Ignore, will aways be overwritten by the height of self.bs
    h = property(_get_h, _set_h)
        
    def getTextSize(self, w=None):
        """Figure out what the width/height of the text self.pbs is. 
        Ignore w if it is defined.
        
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.document import Document
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=1000, h=1000, context=context)
        >>> style = dict(font='PageBot-Regular', leading=em(1.2), fontSize=pt(100))
        >>> bs = context.newString('ABCD', style)
        >>> e = Text(bs, parent=doc[1])
        >>> e.getTextSize(), e.size == e.getTextSize()
        ((250.9pt, 120pt), True)
        >>> bs.textSize == e.getTextSize()
        True
        >>> doc.export('_export/Text-getTextSize.pdf')
        """
        return self.bs.textSize

    def _get_xAlign(self): 
        """Answer the type of x-alignment. Since the orienation of the box is equivalent to the
        on the alignment of the text, it is stored as self.style, referring to the current run.
        That is why we redefine the default element.xAlign propety.

        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('ABCD', dict(xAlign=CENTER))
        """
        return self._validateXAlign(self.bs.xAlign)
    def _set_xAlign(self, xAlign):
        self.bs.aAlign = self._validateXAlign(xAlign) # Save locally, blocking CSS parent scope for this param.
    xAlign = property(_get_xAlign, _set_xAlign)

    #   B U I L D

    def build(self, view, origin, drawElements=True, **kwargs):
        """Draws the text on position (x, y). Draw background rectangle and /
        or frame if fill and / or stroke are defined.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt
        >>> context = getContext('DrawBot')
        >>> doc = Document(w=500, h=100, context=context)
        >>> view = doc.view
        >>> view.showOrigin = True
        >>> view.padding = pt(30)
        >>> view.showCropMarks = True
        >>> view.showFrame = True
        >>> style = dict(font='PageBot-Regular', fontSize=pt(18), textFill=(1, 0, 0), xAlign=CENTER)
        >>> txt = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit valim mecto trambor.'
        >>> bs = context.newString(txt, style) # Creates a BabelString with context reference.
        >>> bs.context is context
        True
        >>> tb = Text(bs, x=100, y=50, parent=doc[1])
        >>> tb.context is context
        True
        >>> doc.export('_export/Text-build.pdf')
        """
        context = view.context # Get current context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        self._applyRotation(view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True.
        view.drawElementFrame(self, p, **kwargs)
        # Draw optional background, frame or borders.
        self.buildFrame(view, (self.left, self.bottom, self.w, self.h))

        # Call if defined.
        if self.drawBefore is not None:
            self.drawBefore(self, view, p)

        # self has its own baseline drawing, derived from the text, instance of
        # self.baselineGrid.
        #self.drawBaselines(view, px, py, background=True) # In case there is a baseline at the back

        textShadow = self.textShadow

        if textShadow:
            context.saveGraphicState()
            context.setShadow(textShadow)

        box = clipPath = None

        if self.clipPath is not None: # Use the elements as clip path:
            clipPath = self.clipPath
            clipPath.translate((px, py))
            context.text(self.bs, clipPath=clipPath)

        elif clipPath is None:
            # If there are child elements, then these are used as layout for
            # the clipping path.
            if 0 and self.elements:
                # Construct the clip path, so we don't need to restore
                # translate.
                clipPath = self.childClipPath
                if clipPath is not None:
                    clipPath.translate((self.pl, self.pb))
                clipPath.translate((self.pl, self.pb))
                context.text(self.bs, clipPath=clipPath)
            else:
                # One of box or clipPath are now defined.
                context.text(self.bs, (px+self.pl, py+self.pb))

        if textShadow:
            context.restoreGraphicState()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if view.showTextOverflowMarker and self.isOverflow():
            # TODO: Make this work for FlatContext too
            self._drawOverflowMarker_drawBot(view, px, py)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'
        view.drawElementOrigin(self, p)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
