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

from pagebot.constants import *
from pagebot.paths import DEFAULT_FONT_NAME
from pagebot.toolbox.units import pt, perc, p
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
    ATTRS = ('textFill', 'textStroke', 'stroke', 'fill', 'link', 'hover',
        'textFillDiap', 'fillDiap', 'textLinkDiap', 'textHoverDiap',
        )
    UNITS = ('leading', 'fontSize', 'width', 'padding', 'margin', 
        'tracking', 'height', 
        )
    NAMES = ('font',)

    def __init__(self, name, styles, palette):
        self.name = name
        self.palette = palette
        self.attributes = {}
        self.styles = {} # Dictionary of values by tag name
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
                # Save the styleName-attrName-value as style dictionary, that can be directly
                # used for creating formattef strings.
                if not styleName in self.styles:
                    self.styles[styleName] = {}
                self.styles[styleName][attrName] = value

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

    def getStyle(self, tag):
        """Answer the style dictionary indicated by tag. Note that this is the 
        reference to the original, so a called can change values directly in the style.
        Answer None if there is not style with that tag name.

        >>> theme = BaseTheme('dark') # Using default mood and default palette
        >>> theme.mood
        <Mood dark>
        >>> style = theme.mood.getStyle('h2')
        >>> style['fontSize']
        28pt
        """
        return self.styles.get(tag)

class BaseTheme:
    u"""The Theme instances combines a number of style dictionaries (property
    values), in relation to a selector path for their usage. In Html/Css terms,
    a theme could describe the entire CSS file where the keys are used as CSS
    selector and the connected styles are used as property:value declaration.

    PageBot will support a growing number of predefined themes, that can be
    copied in a document and then modified. Thet CSS behavior of elements will
    comply to the selected theme of a document, unless they have their own
    style defined.

    >>> from pagebot.style import makeStyle
    >>> theme = BaseTheme('dark') # Using default mood and default palette
    >>> theme.mood
    <Mood dark>
    >>> theme = BaseTheme()
    >>> theme.mood
    <Mood normal>
    >>> theme.mood['page.fill'] # Access by key renders the value to text.
    'FFFFFF'
    >>> theme.mood.page_fill # Access by attribute answers color instance.
    Color(r=1, g=1, b=1)
    >>> theme.mood['h1.fill']
    'FFFFFF'
    >>> theme.mood['body.fill'], theme.mood.body_fill
    ('E7E7E7', Color(r=0.90625, g=0.90625, b=0.90625))
    >>> theme.mood['p.textHover'], theme.mood.p_textHover # Both access by key and by attribute syntax work
    ('DFDFDF', Color(r=0.875, g=0.875, b=0.875))
    >>> theme.mood.body_fontSize, theme.mood.h1_fontSize
    (12pt, 44pt)
    >>> theme.mood.li_fontSize, theme.mood.li_leading
    (12pt, 16.8pt)
    >>> # Test if all generated styles in the mood are a valid PageBot style
    >>> for styleTag, style in theme.mood.styles.items():
    ...     style = makeStyle(style=style)
    >>> # Switch to ligh mood and test again.
    >>> mood = theme.selectMood('light')
    >>> for styleTag, style in theme.mood.styles.items():
    ...     style = makeStyle(style=style)
    """
    def MAKE_FONT_SIZES(fs):
        return dict(
            body=pt(fs, fs*1.4, fs*0.05),
            h5=pt(fs, fs*1.4, fs*0.05),
            h4=pt(fs+4, (fs+4)*1.3, (fs+4)*0.05),
            h3=pt(fs+8, (fs+8)*1.2, 0),
            h2=pt(fs+16, (fs+16)*1.1, 0),
            h1=pt(fs+32, (fs+32)*1.1, 0),
            logo=pt(fs+32, (fs+32)*1.1, 0),
        )
    FONT_SIZES = MAKE_FONT_SIZES(DEFAULT_FONT_SIZE)
    def DEFAULT_TYPOGRAPHIC(tag, fontSizes):
            # Add typographic styles to the standards for this class.
        if tag not in fontSizes:
            tag = 'body'
        fontSize, leading, tracking = fontSizes[tag] 
        padding = p(4)
        margin = 0
        return dict(
            font=DEFAULT_FONT_NAME,
            fontSize=fontSize,
            tracking=tracking,
            leading=leading,
            pt=padding, pr=padding, pb=padding, pl=padding,
            mt=margin, mr=margin, mb=margin, ml=margin,
            strokeWidth=pt(0),
            xAlign=LEFT,
        )

    def DEFAULT_H_COLORS_NORMAL(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            textFill='darkest%d'%c, fill='white',
            textFillDiap='lightest%d'%c, fillDiap='black',
            textLink='darker%d'%c, textHover='dark%d'%c,
            textLinkDiap='lightest%d'%c, textHoverDiap='lighter%d'%c)

    def DEFAULT_MENU_COLORS_NORMAL(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            textFill='darkest%d'%c, fill='lightest%d'%c,
            textFillDiap='lightest%d'%c, fillDiap='dark%d'%c,
            textLink='darkest%d'%c, textHover='dark%d'%c, fillHover='lightest%d'%c,
            textLinkDiap='lightest%d'%c, textHoverDiap='lighter%d'%c,
            textSublink='darker%d'%c, textSubhover='dark%d'%c,
            textSublinkDiap='lightest%d'%c, textSubhoverDiap='lighter%d'%c)

    STYLES_NORMAL = dict(
        # white <-- lighest <-- light <-- lighter <-- base
        # base --> darker --> dark --> darkest --> black
        # Normal.Base 0
        body=dict(textFill='dark0', fill='lightest0'),
        page=dict(textFill='dark0', fill='white'),
        logo=dict(textFill='logo', fill='white'),
        h1=DEFAULT_H_COLORS_NORMAL(0),
        h2=DEFAULT_H_COLORS_NORMAL(0),
        h3=DEFAULT_H_COLORS_NORMAL(0),
        h4=DEFAULT_H_COLORS_NORMAL(0),
        h5=DEFAULT_H_COLORS_NORMAL(0),
        # Default menu and navigation with base0
        menu=DEFAULT_MENU_COLORS_NORMAL(0), # Default base0 if no index used
        mobileMenu=DEFAULT_MENU_COLORS_NORMAL(0), # Default base0 if no index used
        menu0=DEFAULT_MENU_COLORS_NORMAL(0),
        mobileMenu0=DEFAULT_MENU_COLORS_NORMAL(0),
        hr0=dict(textFill='darker0'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro0=dict(textFill='light0', fill='dark0', # .introduction h1
            textLink='light0', textHover='darker0'), # .introduction h1 a

        # Base 1
        menu1=DEFAULT_MENU_COLORS_NORMAL(1),
        mobileMenu1=DEFAULT_MENU_COLORS_NORMAL(1),
        hr=dict(textFill='darker1'), # Default ruler color
        hr1=dict(textFill='darker1'), # <hr> Horizontal ruler color by index
        banner=dict(textFill='base1', fill='white'),
        # Introduction default is base1
        intro=dict(textFill='lightest1', fill='dark1', # .introduction h1
            textLink='light1', textHover='lighter1'), # .introduction h1 a
        intro1=dict(textFill='lightest1', fill='dark1', # .introduction h1
            textLink='light1', textHover='lighter1'), # .introduction h1 a

        group=dict(textFill='black', fill='light1',
            textFillDiap='white', fillDiap='dark1'),
        collection=dict(textFill='black', fill='white',
            textFillDiap='white', fillDiap='dark1'),

        # Base 2
        menu2=DEFAULT_MENU_COLORS_NORMAL(2),
        mobileMenu2=DEFAULT_MENU_COLORS_NORMAL(2),
        hr2=dict(textFill='darker2'), # <hr> Horizontal ruler color by index
        p=dict(textFill='darkest2', fill='white',
            textFillDiap='lightest2', fillDiap='dark2',
            textLink='dark2', textHover='base3', # Hover uses base3
            textLinkDiap='light2', textHoverDiap='lighter2'),
        li=dict(textFill='black', fill='white',
            textFillDiap='white', fillDiap='black',
            textLink='dark2', textHover='darker2',
            textLinkDiap='light2', textHoverLink='lightest2'),
        # Introduction default is base1
        intro2=dict(textFill='lightest2', fill='dark2', # .introduction h1
            textLink='light2', textHover='lighter2'), # .introduction h1 a

        # Base 3
        menu3=DEFAULT_MENU_COLORS_NORMAL(3),
        mobileMenu3=DEFAULT_MENU_COLORS_NORMAL(3),
        hr3=dict(textFill='darker3'), # <hr> Horizontal ruler color by index
        side=dict(textFill='black', fill='white',
            pt=pt(12), pr=pt(12), pb=pt(12), pl=pt(12), 
            textLink='dark3', textHover='darkest3'),
        # Introduction default is base1
        intro3=dict(textFill='lightest3', fill='dark3', # .introduction h1
            textLink='light3', textHover='lighter3'), # .introduction h1 a

        # Base 4 (supporting color)
        menu4=DEFAULT_MENU_COLORS_NORMAL(4),
        mobileMenu4=DEFAULT_MENU_COLORS_NORMAL(4),
        hr4=dict(textFill='darker4'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro4=dict(textFill='lightest4', fill='dark4', # .introduction h1
            textLink='light4', textHover='lighter4'), # .introduction h1 a

        # Base 5 (supporting color)
        menu5=DEFAULT_MENU_COLORS_NORMAL(5),
        mobileMenu5=DEFAULT_MENU_COLORS_NORMAL(5),
        hr5=dict(textFill='darker5'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro5=dict(textFill='lightest5', fill='dark5', # .introduction h1
            textLink='light5', textHover='lighter5'), # .introduction h1 a

        # Functional
        feature=dict(textHed='darkest0', textDeck='darker1',
            textSubhead='dark2', textByline='darkest0',
            textBody='darkest0', textSupport='darkest4',
            textShadow='black',
            textFront='lightest0', textMiddle='base0', textBack='darkest0'),
        # Relative to base
        # Plain base0, base1, base2, base3, base4, base5 are available too
        base0=dict(
            textBack='lighter0', textMoreBack='light0', textMostBack='lightest0',
            textFront='darker0', textMoreFront='dark0', textMostFront='darkest0',
        ),
        base1=dict(
            textBack='lighter1', textMoreBack='light1', textMostBack='lightest1',
            textFront='darker1', textMoreFront='dark1', textMostFront='darkest1',
        ),
        base2=dict(
            textBack='lighter2', textMoreBack='light2', textMostBack='lightest2',
            textFront='darker2', textMoreFront='dark2', textMostFront='darkest2',
        ),
        base3=dict(
            textBack='lighter3', textMoreBack='light3', textMostBack='lightest3',
            textFront='darker3', textMoreFront='dark3', textMostFront='darkest3',
        ),
        base4=dict(
            textBack='lighter4', textMoreBack='light4', textMostBack='lightest4',
            textFront='darker4', textMoreFront='dark4', textMostFront='darkest4',
        ),
        base5=dict(
            textBack='lighter5', textMoreBack='light5', textMostBack='lightest5',
            textFront='darker5', textMoreFront='dark5', textMostFront='darkest5',
        ),
    )
    STYLES_LIGHT = STYLES_NORMAL

    def DEFAULT_H_COLORS_DARK(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            textFill='lightest%d'%c, fill='black',
            textFillDiap='darkest%d'%c, fillDiap='white',
            textLink='lighter%d'%c, textHover='light%d'%c,
            textLinkDiap='darkest%d'%c, textHoverDiap='dark%d'%c)

    def DEFAULT_MENU_DARK(c):
        """Make new dictionary, in case the caller wants to change value."""
        return dict(
            textFill='lightest%d'%c, fill='black',
            textFillDiap='darkest%d'%c, fillDiap='white',
            textLink='lightest%d'%c, textHover='lighter%d'%c, fillHover='darkest%d'%c,
            textLinkDiap='darkest%d'%c, textHoverDiap='dark%d'%c,
            textSublink='lighter%d'%c, textSubhover='light%d'%c,
            textSublinkDiap='darkest%d'%c, textSubhoverDiap='darker%d'%c)

    STYLES_DARK = dict(
        # white <-- lighest <-- light <-- lighter <-- base
        # base --> darker --> dark --> darkest --> black
        # Base 0
        body=dict(textFill='lightest0', fill='dark0'),
        page=dict(textFill='white', fill='dark0'),
        logo=dict(textFill='logo', fill='black'),
        h1=DEFAULT_H_COLORS_DARK(0),
        h2=DEFAULT_H_COLORS_DARK(0),
        h3=DEFAULT_H_COLORS_DARK(0),
        h4=DEFAULT_H_COLORS_DARK(0),
        h5=DEFAULT_H_COLORS_DARK(0),
        # Default menu and navigation with base0
        menu=DEFAULT_MENU_DARK(0), # Default base0 if no index used
        mobileMenu=DEFAULT_MENU_DARK(0), # Default base0 if no index used
        menu0=DEFAULT_MENU_DARK(0),
        mobileMenu0=DEFAULT_MENU_DARK(0),
        hr=dict(textFill='base0'), # Default ruler color
        hr0=dict(textFill='base0'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro0=dict(textFill='darkest0', fill='lightest0', # .introduction h1
            textLink='dark0', textHover='darker0'), # .introduction h1 a

        # Base 1
        menu1=DEFAULT_MENU_DARK(1),
        mobileMenu1=DEFAULT_MENU_DARK(1),
        hr1=dict(textFill='base1'), # <hr> Horizontal ruler color by index
        banner=dict(textFill='white', fill='dark0'),
        # Introduction default is base1
        intro=dict(textFill='darkest1', fill='lightest1', # .introduction h1
            textLink='dark1', textHover='darker1'), # .introduction h1 a
        intro1=dict(textFill='darkest1', fill='lightest1', # .introduction h1
            textLink='dark1', textHover='darker1'), # .introduction h1 a

        group=dict(textFill='light1', fill='black',
            textFillDiap='dark1', fillDiap='white'),
        collection=dict(textFill='black', fill='white',
            textFillDiap='white', fillDiap='dark1'),

        # Base 2
        menu2=DEFAULT_MENU_DARK(2),
        mobileMenu2=DEFAULT_MENU_DARK(2),
        hr2=dict(textFill='base2'), # <hr> Horizontal ruler color by index
        p=dict(textFill='white', fill='darkest2',
            textFillDiap='dark2', fillDiap='lightest2',
            textLink='dark2', textHover='darker2',
            textLinkDiap='lighter2', textHoverDiap='light2'),
        li=dict(textFill='white', fill='black',
            textFillDiap='black', fillDiap='white',
            textLink='darker2', textHover='dark2',
            textLinkDiap='lightest2', textHoverLink='light2'),
        # Introduction default is base1
        intro2=dict(textFill='darkest2', fill='lightest2', # .introduction h1
            textLink='dark2', textHover='darker2'), # .introduction h1 a

        # Base 3
        menu3=DEFAULT_MENU_DARK(3),
        mobileMenu3=DEFAULT_MENU_DARK(3),
        hr3=dict(textFill='base3'), # <hr> Horizontal ruler color by index
        side=dict(textFill='white', fill='black',
            mt=pt(12), mr=pt(12), mb=pt(12), ml=pt(12), 
            textLink='darkest3', textHover='dark3'),
        # Introduction default is base1
        intro3=dict(textFill='darkest3', fill='lightest3', # .introduction h1
            textLink='dark3', textHover='darker3'), # .introduction h1 a

        # Base 4 (supporting color)
        menu4=DEFAULT_MENU_DARK(4),
        mobileMenu4=DEFAULT_MENU_DARK(4),
        hr4=dict(textFill='base4'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro4=dict(textFill='darkest4', fill='lightest4', # .introduction h1
         	textLink='dark4', textHover='darker4'), # .introduction h1 a

        # Base 5 (supporting color)
        menu5=DEFAULT_MENU_DARK(5),
        mobileMenu5=DEFAULT_MENU_DARK(5),
        hr5=dict(textFill='base5'), # <hr> Horizontal ruler color by index
        # Introduction default is base1
        intro5=dict(textFill='darkest5', fill='lightest5', # .introduction h1
            textLink='dark5', textHover='darker5'), # .introduction h1 a

        # Functional
        feature=dict(textHed='lightest0', textDeck='lighter1',
            textSubhead='light2', textByline='lightest0',
            textBody='lightest0', textSupport='lightest4',
            textShadow='black',
            textFront='darkest0', textMiddle='base0', textBack='lightest0'),
        # Relative to base
        # Plain base0, base1, base2, base3, base4, base5 are available too
        base0=dict(
            textMoreFront='lighter0', textFront='light0', textMostFront='lightest0',
            textMoreBack='darker0', back='dark0', textMostBack='darkest0',
        ),
        base1=dict(
            textMoreFront='lighter1', textFront='light1', textMostFront='lightest1',
            textMoreBack='darker1', back='dark1', textMostBack='darkest1',
        ),
        base2=dict(
            textMoreFront='lighter2', textFront='light2', textMostFront='lightest2',
            textMoreBack='darker2', back='dark2', textMostBack='darkest2',
        ),
        base3=dict(
            textMoreFront='lighter3', textFront='light3', textMostFront='lightest3',
            textMoreBack='darker3', back='dark3', textMostBack='darkest3',
        ),
        base4=dict( # Supporting color
            textMoreFront='lighter4', textFront='light4', textMostFront='lightest4',
            textMoreBack='darker4', back='dark4', textMostBack='darkest4',
        ),
        base5=dict( # Supporting color
            textMoreFront='lighter5', textFront='light5', textMostFront='lightest5',
            textMoreBack='darker5', back='dark5', textMostBack='darkest5',
        ),
    )

    STYLES_SMOOTH = STYLES_NORMAL
    STYLES_CONTRAST = STYLES_NORMAL
    # To be redefined by inheriting Theme classes if necessary
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
    # Add typographic value, taking tag into account
    for mood in MOODS.values():
        for tag, tagStyle in mood.items():
            for key, value in DEFAULT_TYPOGRAPHIC(tag, FONT_SIZES).items():
                tagStyle[key] = value

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
    BASE_COLORS = {} # To redefined by inheriting Theme classes.

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

