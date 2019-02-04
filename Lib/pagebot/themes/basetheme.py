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
from pagebot.toolbox.color import spot, rgb, whiteColor, blackColor, grayColor

class Palette:
    """A theme Palette instance holds a limited set of base colors, and from there
    is capable to generate others, based on value recipes.

    >>> p = Palette()
    >>> p.black
    Color(r=0, g=0, b=0)
    >>> p.base1
    Color(r=0.5, g=0.5, b=0.5)
    >>> p.dark5.hex
    '595959'
    >>> p.base1  
    Color(r=0.5, g=0.5, b=0.5)
    """
    NUM_BASE = 6 # $ base and 2 supporters
    BASE_COLOR = grayColor
    BASE_COLORS = dict(
        black=blackColor,
        gray=BASE_COLOR,
        white=whiteColor,
        background=rgb('yellow'), # Safe light text and photo background
        logo=spot(165),
        # Base colors
        base0=BASE_COLOR.darker(0.75),
        base1=BASE_COLOR,
        base2=BASE_COLOR.lighter(0.35),
        base3=BASE_COLOR.lighter(0.75),
        base4=BASE_COLOR.darker(0.75), # Supporter 1
        base5=BASE_COLOR.lighter(0.75), # Supporter 2
    )
    def __init__(self, colors=None):
        self.colorNames = set() # Collect the total set of installed color names.
        # Install default colors
        self.addColors(self.BASE_COLORS)
        if colors is not None:
            self.addColors(colors)
        relatedColors = dict(
            logoLight=self.logo.lighter(),
            logodark=self.logo.darker(),
            supporter1=self.base4,
            supporter2=self.base5
        )
        for n in range(self.NUM_BASE):
            base = self['base%d' % n]
            relatedColors['darker%d' % n] = base.darker(0.7)
            relatedColors['dark%d' % n] = base.darker(0.4)
            relatedColors['darkest%d' % n] = base.darker(0.15)

            relatedColors['lighter%d' % n] = base.lighter(0.3)
            relatedColors['light%d' % n] = base.lighter(0.6)
            relatedColors['lightest%d' % n] = base.lighter(0.85)

            #relatedColors['warmer%d' % n] = base.warmer(self.LEAST)
            #relatedColors['warm%d' % n] = base.warmer(self.MIDDLE)
            #relatedColors['warmest%d' % n] = base.warmer(self.MOST)

            #relatedColors['cooler%d' % n] = base.cooler(self.LEAST)
            #relatedColors['cool%d' % n] = base.cooler(self.MIDDLE)
            #relatedColors['coolest%d' % n] = base.cooler(self.MOST)


        self.addColors(relatedColors, overwrite=False)

    def addColors(self, colors, overwrite=True):
        # Add/overwrite custom base colors and recipes for this palette
        for colorName, c in colors.items():
            if overwrite or not hasattr(self, colorName):
                self.colorNames.add(colorName) # Called can overwrite any color recipe.
                setattr(self, colorName, c)

    def __repr__(self):
        return '<%s colors=%d>' % (self.__class__.__name__, len(self))

    def __getitem__(self, colorName):
        return self.get(colorName)

    def __len__(self):
        return len(self.colorNames)
    
    def get(self, colorName, default=None):
        """Interpret the name, and try to match/construct a color based on the recipe.
        """
        if colorName in self.colorNames:
            return getattr(self, colorName)
        return default

class Style:
    """Holds CSS-style values, accessable as key and as attrName.

    """
    def __init__(self, name, palette, styleDict):
        #assert isinstance(palette, Palette), 'Palette not right type "%s"' % palette
        self.name = name or 'Untitled'
        self.palette = palette
        for attrName, value in styleDict.items():
            self[attrName] = palette[value]

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

class Mood:
    """Mood hold a set of style values. If the value exists as key in the self.palette,
    then answer that value instead.

    """
    # Predefined styles
    IDS = ('body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'a', 'body', 'page',
        'p', 'li', 'div', 'banner', 'intro', 'logo', 'hr', 'group', 'menu', 
        'main', 'side')
    COLORS = ('color', 'stroke', 'bgcolor', 'link', 'hover',
        'diapcolor', 'diapbgcolor', 'diaplink', 'diaphover',
        )
    UNITS = ('leading', 'fontSize', 'width', 'padding', 'margin')
    NAMES = ('font',)
    
    def __init__(self, name, styles, palette):
        self.name = name
        self.palette = palette
        for styleName, styleDict in styles.items():
            self[styleName] = Style(styleName, palette, styleDict)

    def __getitem__(self, styleName):
        return getattr(self, styleName)

    def __setitem__(self, styleName, style):
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

    >>> theme = BaseTheme() # Using default mood and default palette
    >>> theme.mood.page.color, theme.mood.page.bgcolor # Access by attribute
    (Color(r=0, g=0, b=0), Color(r=1, g=1, b=1))
    >>> theme.mood.h1.color, theme.mood.h1.bgcolor
    (Color(r=1, g=1, b=1), Color(r=0, g=0, b=0))
    >>> theme.mood['li']['color'], theme.mood['li']['bgcolor'] # Access by key
    (Color(r=0, g=0, b=0), Color(r=1, g=1, b=1))
    """

    STYLES_LIGHT = dict(
        # Base 0
        body=dict(color='dark0', bgcolor='lighest0'),
        page=dict(color='dark0', bgcolor='white'),
        logo=dict(color='logo', bgcolor='white'),
        hr=dict(color='darker0'), # <hr> Horizontal ruler
        h1=dict(color='darker0', bgcolor='white', 
            diapcolor='light0', diapbgcolor='dark0',
            link='base0', hover='dark0',
            diaplink='lightest0', diaphover='lighter0'),
        h2=dict(color='darker0', bgcolor='white', 
            diapcolor='light0', diapbgcolor='dark0',
            link='base0', hover='dark0',
            diaplink='lightest0', diaphover='lighter0'),
        h3=dict(color='darker0', bgcolor='white', 
            diapcolor='light0', diapbgcolor='dark0',
            link='base0', hover='dark0',
            diaplink='lightest0', diaphover='lighter0'),
        h4=dict(color='darker0', bgcolor='white', 
            diapcolor='light0', diapbgcolor='dark0',
            link='base0', hover='dark0',
            diaplink='lightest0', diaphover='lighter0'),
        h5=dict(color='darker0', bgcolor='white', 
            diapcolor='light0', diapbgcolor='dark0',
            link='base0', hover='dark0',
            diaplink='lightest0', diaphover='lighter0'),
        # Base 1
        banner=dict(color='base1', bgcolor='white'),
        intro=dict(color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=dict(color='black', bgcolor='hilite1',
            diapcolor='white', diapbgcolor='dark'),
        menu=dict(color='black', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='black',
            link='hilite2', hover='supporter2'),
        # Base 2
        p=dict(color='darkest2', bgcolor='white',
            diapcolor='lightest2', diapbgcolor='dark2',
            link='darker2', hover='dark2',
            diaplink='light2', diaphover='lighter2'),
        li=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='dark2', hover='darker2',
            diaplink='light2', hover='lightest2'),
        # Base 3
        side=dict(color='black', bgcolor='white',
            padding=12, 
            link='dark3', hover='darkest3'),
    )
    STYLES_NORMAL = dict(
        body=dict(color='black', bgcolor='black'),
        page=dict(color='black', bgcolor='white'),
        logo=dict(color='logo1', bgcolor='supporter1'),
        hr=dict(color='supporter3'), # <hr> Horizontal ruler
        h1=dict(color='white', bgcolor='black', 
            link='middle', hover='light'),
        h2=dict(color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        h3=dict(color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        banner=dict(color='middle', bgcolor='white'),
        intro=dict(color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=dict(color='black', bgcolor='hilite1',
            diapcolor='white', diapbgcolor='dark'),
        menu=dict(color='black', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='black',
            link='hilite2', hover='supporter2'),
        p=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        li=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        side=dict(color='black', bgcolor='hilite3',
            padding=12, 
            link='middle', hover='black'),
    )
    STYLES_DARK = dict(
        body=dict(color='white', bgcolor='black'),
        page=dict(color='white', bgcolor='black'),
        logo=dict(color='logo1', bgcolor='supporter1'),
        hr=dict(color='supporter3'), # <hr> Horizontal ruler
        h1=dict(color='black', bgcolor='white', 
            link='middle', hover='dark'),
        h2=dict(color='white', bgcolor='hilite3',
            diapcolor='hilite3', diapbgcolor='white'),
        h3=dict(color='white', bgcolor='hilite3',
            diapcolor='hilite3', diapbgcolor='white'),
        banner=dict(color='white', bgcolor='middle'),
        intro=dict(color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=dict(color='hilite1', bgcolor='black',
            diapcolor='dark', diapbgcolor='white'),
        menu=dict(color='hilite1', bgcolor='black',
            diapcolor='black', diapbgcolor='hilite1',
            link='hilite2', hover='supporter2'),
        p=dict(color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='cold', hover='warm'),
        li=dict(color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='warm', hover='cold'),
        side=dict(color='hilite3', bgcolor='black',
            padding=12, 
            link='middle', hover='light'),
    )
    # To be redefined by inheriting Them classes if necessary
    MOODS = {
        'light': STYLES_LIGHT,
        'normal': STYLES_NORMAL,
        'dark': STYLES_DARK,
        #'smooth': Mood('Smooth', STYLES_SMOOTH),
        #'contrast': Mood('Contrast', STYLES_CONTRAST),
    }
    NAME = "BaseTheme"
    COLORS = None # To redefined by inheriting Theme classes.
    BASE_COLORS = {}


    def __init__(self, mood=None):
        self.palette = Palette(self.BASE_COLORS)
        self.name = self.NAME
        self.selectMood(mood)

    def selectMood(self, name):
        name = name or 'normal'
        self.mood = Mood(name, self.MOODS[name], self.palette)
        return self.mood

    def __repr__(self):
        return '<Theme %s styles:%d>' % (self.name, len(self.styles))

    def __getitem__(self, selector):
        return self.selectMood(selector)


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

