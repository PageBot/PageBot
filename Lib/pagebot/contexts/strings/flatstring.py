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
#     fsstring.py
#
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css, LEFT

class FlatString(BabelString):

    BABEL_STRING_TYPE = 'flat'

    u"""FlatString is a wrapper around the Flat string."""
    def __init__(self, s, b):
        self.b = b # Store the builder, in case we need it.
        self.s = s # Enclose the Flat string

    def _get_flat(self):
        u"""Answer the embedded Flat string by property, to enforce checking type of the string."""
        return self.s
    def _set_flat(self, flatString):
        #if isinstance(fs, basestring):
        #    fs = Style(s)
        self.s = flatString
    flat = property(_get_flat, _set_flat)
    
    def asText(self):
        return self.s # TODO: To be changed to Flat string behavior.

    def textSize(self, w):
        u"""Answer the (w, h) size for a given width, with the current text."""
        return 0, 0
        # TODO: Make this work in Flat
        #return self.b.textSize(s)
 
    def textOverflow(self, w, h, align=LEFT):
        # TODO: Some stuff needs to get here.
        return ''

def newFlatString(s, b=None, e=None, style=None, w=None, h=None, fontSize=None, styleName=None, tagName=None):
    u"""Answer a FlatString instance from valid attributes in *style*. Set all values after testing
    their existence, so they can inherit from previous style formats.
    If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""
    if b is None:
        from pagebot.builders.flatbuilder import flatBuilder as b

    sUpperCase = css('uppercase', e, style)
    sLowercase = css('lowercase', e, style)
    sCapitalized = css('capitalized', e, style)
    if sUpperCase:
        s = s.upper()
    elif sLowercase:
        s = s.lower()
    elif sCapitalized:
        s = s.capitalize()

    # TODO: Style stuff here.
    return FlatString(s, b) # Make real Flat string here.


