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

import copy
from pagebot.style import getRootStyle
from pagebot.toolbox.color import spot, rgb

class Palette:

    def __init__(self, **kwargs):
        self.attrNames = kwargs.keys()
        for attrName, value in kwargs.items():
            setattr(self, attrName, value)

    def __repr__(self):
        return '<%s attrs=%d>' % (self.__class__.__name__, len(self))

    def __getitem__(self, attrName):
        return self.get(attrName)

    def __len__(self):
        return len(self.attrNames)
    
    def get(self, name, default=None):
        if name in self.attrNames:
            return getattr(self, name)
        return default

class Style:
    """HOlds CSS-style values, accessable as key and as attrName.

    >>> from pagebot.themes.freshandshiny import FreshAndShiny
    >>> palette = FreshAndShiny.PALETTE
    >>> style = Style(palette, fill='c1', stroke='c2')
    >>> style.fill
    'c1'
    >>> style.stroke
    'c2'
    """
    def __init__(self, palette, name=None, **kwargs):
        #assert isinstance(palette, Palette), 'Palette not right type "%s"' % palette
        self.palette = palette
        self.name = name or 'Untitled'
        for attrName, value in kwargs.items():
            self[attrName] = value

    def __getitem__(self, name):
        v = self.get(name)
        return self.palette.get(v, v) # If reference in self.palette, then translate the value.

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

class Mood:
    """Mood hold a set of style values. If the value exists as key in the self.palette,
    then answer that value instead.

    >>> from pagebot.themes.freshandshiny import FreshAndShiny
    >>> palette = FreshAndShiny.PALETTE
    >>> styles = dict(h1_0=Style(palette, fill='c1', stroke='c2'))
    >>> mood = Mood('Dark', styles)
    >>> mood.h1_0.fill
    'c1'
    """
    # Predefined styles
    IDS = ('body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'a', 'body', 
        'p', 'li', 'div', 'banner', 'intro', 'logo', 'hr', 'group', 'menu')
    COLORS = ('color', 'stroke', 'bgcolor', 'link', 'hover',
        'diapcolor', 'diapbgcolor', 'diaplink', 'diaphover',
        )
    UNITS = ('leading', 'fontSize', 'width')
    NAMES = ('font',)
    
    def __init__(self, name, styles):
        self.name = name
        for styleName, style in styles.items():
            self.addStyle(styleName, style)

    def __getitem__(self, styleName):
        return self.get(styleName)

    def __setitem__(self, styleName, value):
        self.set(styleName, value)

    def get(self, styleCssName):
        if not '.' in styleCssName:
            styleName = styleCssName
            funcName = 'fill'
        else:
            styleName, funcName = styleCssName.split('.')
        assert styleName.split('_')[0] in self.IDS, 'Style name not valid "%s"' % styleName

        v = self.getStyle(styleName)[funcName]
        if funcName in self.COLORS:
            try:
                v = v.hex
            except AttributeError:
                print('Bad color "%s" for "%s"' % (v, styleCssName))
        return v

    def getStyle(self, styleName):
        style = getattr(self, styleName)
        assert isinstance(style, Style)
        return style
        v = self.styles.get(styleName)
        return self.palette.get(v, v)

    def addStyle(self, styleName, style):
        assert not hasattr(self, styleName) # Prevent overwriting existing attributes.
        assert isinstance(style, Style)
        setattr(self, styleName, style)

class BaseTheme:
    u"""The Theme instances combines a number of style dictionaries (property
    values), in relation to a selector path for their usage. In Html/Css terms,
    a theme could describe the entire CSS file where the keys are used as CSS
    selector and the connected styles are used as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be
    copied in a document and then modified. Thet CSS behavior of elements will
    comply to the selected theme of a document, unless they have their own
    style defined.

    >>> from pagebot.themes.freshandshiny import FreshAndShiny
    >>> theme = FreshAndShiny()
    >>> theme.mood.h1_0.palette.c2
    Color(spot=coolgray6u)
    >>> theme.mood.h1_0.palette['c3']
    Color(spot=165)
    """
    MOODS = None # To be redefined by inheriting Them classes
    COLORS = None # To redefined by inheriting Theme classes.

    def __init__(self, mood=None):
        self.name = self.NAME
        self.moods = self.MOODS
        self.selectMood(mood)

    def selectMood(self, name):
        self.mood = self.moods.get(name) or self.moods['normal']

    def __repr__(self):
        return '<Theme %s styles:%d>' % (self.name, len(self.styles))

    def __getitem__(self, selector):
        return self.mood[selector]


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

