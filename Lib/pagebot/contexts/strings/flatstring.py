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

    def _get_s(self):
        u"""Answer the embedded Flat equivalent of a OSX FormattedString by property, to enforce checking type of the string."""
        return self._s
    def _set_s(self, s):
        if isinstance(s, basestring):
            s = s # TODO: Change to Flat equivalent of FormattedString.
        self._s = s
    s = property(_get_s, _set_s)
  
    def asText(self):
        return self.s # TODO: To be changed to Flat string behavior.

    def textSize(self, w):
        u"""Answer the (w, h) size for a given width, with the current text."""
        return 0, 0
        # TODO: Make this work in Flat same as in DrawBot
        #return self.b.textSize(s)
 
    def textOverflow(self, w, h, align=LEFT):
        # TODO: Make this work in Flat same as in DrawBot
        # TODO: Some stuff needs to get here.
        return ''

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, fontSize=None, styleName=None, tagName=None):
        u"""Answer a FlatString instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""

        sUpperCase = css('uppercase', e, style)
        sLowercase = css('lowercase', e, style)
        sCapitalized = css('capitalized', e, style)
        if sUpperCase:
            s = s.upper()
        elif sLowercase:
            s = s.lower()
        elif sCapitalized:
            s = s.capitalize()

        # Since Flat does not do fetaure compile, we'll make the transformed string here,
        # using Tal's https://github.com/typesupply/compositor
        # This needs to be installed, in case PageBot is running outside of DrawBot.
        
        # TODO: Style stuff here.
        return cls(s, context) # Make real Flat string here.


