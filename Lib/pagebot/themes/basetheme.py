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

from random import choice

from pagebot.toolbox.units import pt
from pagebot.toolbox.color import spotColor, rgbColor, whiteColor, blackColor, grayColor

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
        background=rgbColor('yellow'), # Safe light text and photo background
        logo=spotColor(165),
        # Base colors
        base0=BASE_COLOR.darker(0.75),
        base1=BASE_COLOR,
        base2=BASE_COLOR.lighter(0.35),
        base3=BASE_COLOR.lighter(0.75),
        base4=BASE_COLOR.darker(0.75), # Supporter 1
        base5=BASE_COLOR.lighter(0.75), # Supporter 2
    )
    FACTOR_DARKEST = 0.15
    FACTOR_DARK = 0.4
    FACTOR_DARKER = 0.7

    FACTOR_LIGHTER = 0.3
    FACTOR_LIGHT = 0.6
    FACTOR_LIGHTEST = 0.85

    def __init__(self, colors=None, **kwargs):
        self.colorNames = set() # Collect the total set of installed color names.

        # Set lighter/darker factors from arguments or default
        self.factorDarkest = kwargs.get('darkest', self.FACTOR_DARKEST)
        self.factorDark = kwargs.get('dark', self.FACTOR_DARK)
        self.factorDarker = kwargs.get('darker', self.FACTOR_DARKER)

        self.factorLightest = kwargs.get('lightest', self.FACTOR_LIGHTEST)
        self.factorLight = kwargs.get('light', self.FACTOR_LIGHT)
        self.factorLighter = kwargs.get('lighter', self.FACTOR_LIGHTER)

        # Install default colors
        self.addColors(self.BASE_COLORS)
        if colors is not None:
            self.addColors(colors)

        relatedColors = dict(
            logoLight=self.logo.lighter(),
            logoDark=self.logo.darker(),
            supporter1=self.base4,
            supporter2=self.base5
        )
        for n in range(self.NUM_BASE):
            base = self['base%d' % n]
            relatedColors['darker%d' % n] = base.darker(self.factorDarker)
            relatedColors['dark%d' % n] = base.darker(self.factorDark)
            relatedColors['darkest%d' % n] = base.darker(self.factorDarkest)

            relatedColors['lighter%d' % n] = base.lighter(self.factorLighter)
            relatedColors['light%d' % n] = base.lighter(self.factorLight)
            relatedColors['lightest%d' % n] = base.lighter(self.factorLightest)

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

    def _get_random(self):
        return self.get(choice(list(self.colorNames)))
    random = property(_get_random)

    def __repr__(self):
        return '<%s colors=%d>' % (self.__class__.__name__, len(self))

    def __getitem__(self, colorName):
        return self.get(colorName)

    def __len__(self):
        return len(self.colorNames)

    def get(self, colorName):
        """Interpret the name, and try to match/construct a color based on the recipe.
        """
        assert colorName in self.colorNames, ('%s.get: Unknown color  name "%s"' % (self.__class__.__name__, colorName))
        return getattr(self, colorName)

class Mood:
    """Mood hold a set of style values. If the value exists as key in the self.palette,
    then answer that value instead.
    """
    # Predefined styles
    IDS = ('body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'a', 'body', 'page',
        'p', 'li', 'div', 'banner', 'intro', 'logo', 'hr', 'group', 'menu',
        'main', 'side')
    COLORS = ('black', 'gray', 'white', 'background', 'logoLight', 'logo', 'logoDark',
        'lightest0', 'light0', 'lighter0', 'base0', 'darker0', 'dark0', 'darkest0',
        'lightest1', 'light1', 'lighter1', 'base1', 'darker1', 'dark1', 'darkest1',
        'lightest2', 'light2', 'lighter2', 'base2', 'darker2', 'dark2', 'darkest2',
        'lightest3', 'light3', 'lighter3', 'base3', 'darker3', 'dark3', 'darkest3',
        'lightest4', 'light4', 'lighter4', 'base4', 'darker4', 'dark4', 'darkest4',
        'lightest5', 'light5', 'lighter5', 'base5', 'darker5', 'dark5', 'darkest5',
    )
    ATTRS = ('color', 'stroke', 'bgcolor', 'link', 'hover',
        'diapcolor', 'diapbgcolor', 'diaplink', 'diaphover',
        )
    UNITS = ('leading', 'fontSize', 'width', 'padding', 'margin')
    NAMES = ('font',)

    def __init__(self, name, styles, palette):
        self.name = name
        self.palette = palette
        self.attributes = {}
        # Set colors from combined "IDS.COLOR" names
        for styleName, styleDict in styles.items():
            for attrName, value in styleDict.items():
                if value in self.COLORS:
                    value = palette.get(value)
                    keyValue = value.hex
                else:
                    keyValue = value
                self.attributes['%s.%s' % (styleName, attrName)] = keyValue # Key value is hex color
                setattr(self, '%s_%s' % (styleName, attrName), value) # Attr value is origina value object
        # Set all colors as separate entries too, do they can be referred to, ignoring the mood.
        for colorName in self.COLORS:
            value = palette.get(colorName)
            keyValue = value.hex
            self.attributes[colorName] = keyValue # E.g. mood['light0'] answers "0E0D0F"
            setattr(self, colorName, value) # E.g. mood.light0 answers Color instsance.

    def __getitem__(self, attrName):
        return self.attributes[attrName]

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

class BaseTheme:
    u"""The Theme instances combines a number of style dictionaries (property
    values), in relation to a selector path for their usage. In Html/Css terms,
    a theme could describe the entire CSS file where the keys are used as CSS
    selector and the connected styles are used as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be
    copied in a document and then modified. Thet CSS behavior of elements will
    comply to the selected theme of a document, unless they have their own
    style defined.

    >>> theme = BaseTheme('dark') # Using default mood and default palette
    >>> theme.mood
    <Mood dark>
    >>> theme = BaseTheme()
    >>> theme.mood
    <Mood normal>
    >>> theme.mood['page.bgcolor'] # Access by key
    'FFFFFF'
    >>> theme.mood.page_bgcolor # Access by attribute
    Color(r=1, g=1, b=1)
    >>> theme.mood['h1.bgcolor']
    'FFFFFF'
    >>> theme.mood['body.bgcolor'], theme.mood.body_bgcolor
    ('E7E7E7', Color(r=0.90625, g=0.90625, b=0.90625))
    >>> theme.mood['p.hover'], theme.mood.p_hover # Both access by key and by attribute syntax work
    ('DFDFDF', Color(r=0.875, g=0.875, b=0.875))
    """
    def DEFAULT_H_COLORS_NORMAL(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            color='darkest%d'%c, bgcolor='white',
            diapcolor='lightest%d'%c, diapbgcolor='black',
            link='darker%d'%c, hover='dark%d'%c,
            diaplink='lightest%d'%c, diaphover='lighter%d'%c)

    def DEFAULT_MENU_NORMAL(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            color='darkest%d'%c, bgcolor='lightest%d'%c,
            diapcolor='lightest%d'%c, diapbgcolor='dark%d'%c,
            link='darkest%d'%c, hover='dark%d'%c, bghover='lightest%d'%c,
            diaplink='lightest%d'%c, diaphover='lighter%d'%c,
            sublink='darker%d'%c, subhover='dark%d'%c,
            diapsublink='lightest%d'%c, diapsubhover='lighter%d'%c)

    STYLES_NORMAL = dict(
        # white <-- lighest <-- light <-- lighter <-- base
        # base --> darker --> dark --> darkest --> black
        # Normal.Base 0
        body=dict(color='dark0', bgcolor='lightest0'),
        page=dict(color='dark0', bgcolor='white'),
        logo=dict(color='logo', bgcolor='white'),
        h1=DEFAULT_H_COLORS_NORMAL(0),
        h2=DEFAULT_H_COLORS_NORMAL(0),
        h3=DEFAULT_H_COLORS_NORMAL(0),
        h4=DEFAULT_H_COLORS_NORMAL(0),
        h5=DEFAULT_H_COLORS_NORMAL(0),
        # Default menu and navigation with base0
        menu=DEFAULT_MENU_NORMAL(0), # Default base0 if no index used
        mobilemenu=DEFAULT_MENU_NORMAL(0), # Default base0 if no index used
        menu0=DEFAULT_MENU_NORMAL(0),
        mobilemenu0=DEFAULT_MENU_NORMAL(0),
        hr0=dict(color='darker0'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro0=dict(color='light0', bgcolor='dark0', # .introduction h1
            link='light0', hover='darker0'), # .introduciton h1 a

        # Base 1
        menu1=DEFAULT_MENU_NORMAL(1),
        mobilemenu1=DEFAULT_MENU_NORMAL(1),
        hr=dict(color='darker1'), # Default ruler color
        hr1=dict(color='darker1'), # <hr> Horizontal ruler color by index
        banner=dict(color='base1', bgcolor='white'),
        # Introduction default is base1
        intro=dict(color='lightest1', bgcolor='dark1', # .introduction h1
            link='light1', hover='lighter1'), # .introduciton h1 a
        intro1=dict(color='lightest1', bgcolor='dark1', # .introduction h1
            link='light1', hover='lighter1'), # .introduciton h1 a

        group=dict(color='black', bgcolor='light1',
            diapcolor='white', diapbgcolor='dark1'),
        collection=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='dark1'),

        # Base 2
        menu2=DEFAULT_MENU_NORMAL(2),
        mobilemenu2=DEFAULT_MENU_NORMAL(2),
        hr2=dict(color='darker2'), # <hr> Horizontal ruler color by index
        p=dict(color='darkest2', bgcolor='white',
            diapcolor='lightest2', diapbgcolor='dark2',
            link='dark2', hover='base3', # Hover uses base3
            diaplink='light2', diaphover='lighter2'),
        li=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='dark2', hover='darker2',
            diaplink='light2', hoverlink='lightest2'),
        # Introduction default is base1
        intro2=dict(color='lightest2', bgcolor='dark2', # .introduction h1
            link='light2', hover='lighter2'), # .introduciton h1 a

        # Base 3
        menu3=DEFAULT_MENU_NORMAL(3),
        mobilemenu3=DEFAULT_MENU_NORMAL(3),
        hr3=dict(color='darker3'), # <hr> Horizontal ruler color by index
        side=dict(color='black', bgcolor='white',
            padding=pt(12), link='dark3', hover='darkest3'),
        # Introduction default is base1
        intro3=dict(color='lightest3', bgcolor='dark3', # .introduction h1
            link='light3', hover='lighter3'), # .introduciton h1 a

        # Base 4 (supporting color)
        menu4=DEFAULT_MENU_NORMAL(4),
        mobilemenu4=DEFAULT_MENU_NORMAL(4),
        hr4=dict(color='darker4'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro4=dict(color='lightest4', bgcolor='dark4', # .introduction h1
            link='light4', hover='lighter4'), # .introduciton h1 a

        # Base 5 (supporting color)
        menu5=DEFAULT_MENU_NORMAL(5),
        mobilemenu5=DEFAULT_MENU_NORMAL(5),
        hr5=dict(color='darker5'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro5=dict(color='lightest5', bgcolor='dark5', # .introduction h1
            link='light5', hover='lighter5'), # .introduciton h1 a

        # Functional
        feature=dict(hed='darkest0', deck='darker1',
            subhead='dark2', byline='darkest0',
            text='darkest0', support='darkest4',
            shadow='black',
            front='lightest0', middle='base0', back='darkest0'),
        # Relative to base
        # Plain base0, base1, base2, base3, base4, base5 are available too
        base0=dict(
            backer='lighter0', back='light0', backest='lightest0',
            fronter='darker0', front='dark0', frontest='darkest0',
        ),
        base1=dict(
            backer='lighter1', back='light1', backest='lightest1',
            fronter='darker1', front='dark1', frontest='darkest1',
        ),
        base2=dict(
            backer='lighter2', back='light2', backest='lightest2',
            fronter='darker2', front='dark2', frontest='darkest2',
        ),
        base3=dict(
            backer='lighter3', back='light3', backest='lightest3',
            fronter='darker3', front='dark3', frontest='darkest3',
        ),
        base4=dict(
            backer='lighter4', back='light4', backest='lightest4',
            fronter='darker4', front='dark4', frontest='darkest4',
        ),
        base5=dict(
            backer='lighter5', back='light5', backest='lightest5',
            fronter='darker5', front='dark5', frontest='darkest5',
        ),
    )
    STYLES_LIGHT = STYLES_NORMAL

    def DEFAULT_H_COLORS_DARK(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            color='lightest%d'%c, bgcolor='black',
            diapcolor='darkest%d'%c, diapbgcolor='white',
            link='lighter%d'%c, hover='light%d'%c,
            diaplink='darkest%d'%c, diaphover='dark%d'%c)

    def DEFAULT_MENU_DARK(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            color='lightest%d'%c, bgcolor='black',
            diapcolor='darkest%d'%c, diapbgcolor='white',
            link='lightest%d'%c, hover='lighter%d'%c, bghover='darkest%d'%c,
            diaplink='darkest%d'%c, diaphover='dark%d'%c,
            sublink='lighter%d'%c, subhover='light%d'%c,
            diapsublink='darkest%d'%c, diapsubhover='darker%d'%c)

    STYLES_DARK = dict(
        # white <-- lighest <-- light <-- lighter <-- base
        # base --> darker --> dark --> darkest --> black
        # Base 0
        body=dict(color='lightest0', bgcolor='dark0'),
        page=dict(color='white', bgcolor='dark0'),
        logo=dict(color='logo', bgcolor='black'),
        h1=DEFAULT_H_COLORS_DARK(0),
        h2=DEFAULT_H_COLORS_DARK(0),
        h3=DEFAULT_H_COLORS_DARK(0),
        h4=DEFAULT_H_COLORS_DARK(0),
        h5=DEFAULT_H_COLORS_DARK(0),
        # Default menu and navigation with base0
        menu=DEFAULT_MENU_DARK(0), # Default base0 if no index used
        mobilemenu=DEFAULT_MENU_DARK(0), # Default base0 if no index used
        menu0=DEFAULT_MENU_DARK(0),
        mobilemenu0=DEFAULT_MENU_DARK(0),
        hr=dict(color='base0'), # Default ruler color
        hr0=dict(color='base0'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro0=dict(color='darkest0', bgcolor='lightest0', # .introduction h1
            link='dark0', hover='darker0'), # .introduction h1 a

        # Base 1
        menu1=DEFAULT_MENU_DARK(1),
        mobilemenu1=DEFAULT_MENU_DARK(1),
        hr1=dict(color='base1'), # <hr> Horizontal ruler color by index
        banner=dict(color='white', bgcolor='dark0'),
        # Introduction default is base1
        intro=dict(color='darkest1', bgcolor='lightest1', # .introduction h1
            link='dark1', hover='darker1'), # .introduction h1 a
        intro1=dict(color='darkest1', bgcolor='lightest1', # .introduction h1
            link='dark1', hover='darker1'), # .introduction h1 a

        group=dict(color='light1', bgcolor='black',
            diapcolor='dark1', diapbgcolor='white'),
        collection=dict(color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='dark1'),

        # Base 2
        menu2=DEFAULT_MENU_DARK(2),
        mobilemenu2=DEFAULT_MENU_DARK(2),
        hr2=dict(color='base2'), # <hr> Horizontal ruler color by index
        p=dict(color='white', bgcolor='darkest2',
            diapcolor='dark2', diapbgcolor='lightest2',
            link='dark2', hover='darker2',
            diaplink='lighter2', diaphover='light2'),
        li=dict(color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='darker2', hover='dark2',
            diaplink='lightest2', hoverlink='light2'),
        # Introduction default is base1
        intro2=dict(color='darkest2', bgcolor='lightest2', # .introduction h1
            link='dark2', hover='darker2'), # .introduction h1 a

        # Base 3
        menu3=DEFAULT_MENU_DARK(3),
        mobilemenu3=DEFAULT_MENU_DARK(3),
        hr3=dict(color='base3'), # <hr> Horizontal ruler color by index
        side=dict(color='white', bgcolor='black',
            padding=pt(12), link='darkest3', hover='dark3'),
        # Introduction default is base1
        intro3=dict(color='darkest3', bgcolor='lightest3', # .introduction h1
            link='dark3', hover='darker3'), # .introduction h1 a

        # Base 4 (supporting color)
        menu4=DEFAULT_MENU_DARK(4),
        mobilemenu4=DEFAULT_MENU_DARK(4),
        hr4=dict(color='base4'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro4=dict(color='darkest4', bgcolor='lightest4', # .introduction h1
            link='dark4', hover='darker4'), # .introduction h1 a

        # Base 5 (supporting color)
        menu5=DEFAULT_MENU_DARK(5),
        mobilemenu5=DEFAULT_MENU_DARK(5),
        hr5=dict(color='base5'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro5=dict(color='darkest5', bgcolor='lightest5', # .introduction h1
            link='dark5', hover='darker5'), # .introduction h1 a

        # Functional
        feature=dict(hed='lightest0', deck='lighter1',
            subhead='light2', byline='lightest0',
            text='lightest0', support='lightest4',
            shadow='black',
            front='darkest0', middle='base0', back='lightest0'),
        # Relative to base
        # Plain base0, base1, base2, base3, base4, base5 are available too
        base0=dict(
            fronter='lighter0', front='light0', frontest='lightest0',
            backer='darker0', back='dark0', backest='darkest0',
        ),
        base1=dict(
            fronter='lighter1', front='light1', frontest='lightest1',
            backer='darker1', back='dark1', backest='darkest1',
        ),
        base2=dict(
            fronter='lighter2', front='light2', frontest='lightest2',
            backer='darker2', back='dark2', backest='darkest2',
        ),
        base3=dict(
            fronter='lighter3', front='light3', frontest='lightest3',
            backer='darker3', back='dark3', backest='darkest3',
        ),
        base4=dict( # Supporting color
            fronter='lighter4', front='light4', frontest='lightest4',
            backer='darker4', back='dark4', backest='darkest4',
        ),
        base5=dict( # Supporting color
            fronter='lighter5', front='light5', frontest='lightest5',
            backer='darker5', back='dark5', backest='darkest5',
        ),
    )

    STYLES_SMOOTH = STYLES_NORMAL
    STYLES_CONTRAST = STYLES_NORMAL
    # To be redefined by inheriting Them classes if necessary
    MOOD_NAME_LIGHT = 'light'
    MOOD_NAME_NORMAL = 'normal'
    MOOD_NAME_DARK = 'dark'
    MOOD_NAME_SMOOTH = 'smooth'
    MOOD_NAME_CONTRAST = 'contrast'

    MOODS = {
        MOOD_NAME_LIGHT: STYLES_LIGHT,
        MOOD_NAME_NORMAL: STYLES_NORMAL,
        MOOD_NAME_DARK: STYLES_DARK,
        MOOD_NAME_SMOOTH: STYLES_SMOOTH,
        MOOD_NAME_CONTRAST: STYLES_CONTRAST,
    }
    # Keep them in order for popups
    MOOD_NAMES = (
        MOOD_NAME_LIGHT,
        MOOD_NAME_NORMAL,
        MOOD_NAME_DARK,
        MOOD_NAME_SMOOTH,
        MOOD_NAME_CONTRAST,
    )
    DEFAULT_MOOD_NAME = MOOD_NAME_NORMAL
    NAME = "BaseTheme"
    COLORS = None # To redefined by inheriting Theme classes.
    BASE_COLORS = {}


    def __init__(self, name=None):
        self.palette = Palette(self.BASE_COLORS)
        self.name = self.NAME
        self.selectMood(name)

    def selectMood(self, name):
        name = name or 'normal'
        self.mood = Mood(name, self.MOODS[name], self.palette)
        return self.mood

    def __repr__(self):
        return '<Theme %s mood=%s>' % (self.name, self.mood.name)

    def __getitem__(self, selector):
        return self.selectMood(selector)


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

