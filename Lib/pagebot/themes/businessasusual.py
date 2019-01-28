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
#     businesasusual.py
#
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class BusinessAsUsual(BaseTheme):
    u"""The BusinessAsUsual theme is a generic “woody cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

    NAME = 'Business as Usual'
    BASE_COLORS = dict(
        base0=spot('blacku'),
        base1=spot(404),
        base2=spot(541),
        base3=spot(542),
        base4=spot(139), # Supporter1
        base5=spot(877),
    )
    """
    STYLES_LIGHT = dict(
        logo=Style(PALETTE, color='supporter2', bgcolor='supporter1'),
        hr=Style(PALETTE, color='dark'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='white', bgcolor='black', 
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        banner=Style(PALETTE, color='black', bgcolor='hilite1'),
        intro=Style(PALETTE, color='black', bgcolor='hilite1'),
        group=Style(PALETTE, color='black', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='black'),
        menu=Style(PALETTE, color='black', bgcolor='hilite1',
            link='middle', hover='light',
            diapcolor='hilite1', diapbgcolor='black'),
        body=Style(PALETTE, color='black', bgcolor='white'),
        p=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        li=Style(PALETTE, color='supporter3', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite2', hover='supporter1'),
    )
    STYLES_NORMAL = dict(
        logo=Style(PALETTE, color='supporter2', bgcolor='supporter1'),
        hr=Style(PALETTE, color='black'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='hilite2', bgcolor='hilite1',
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        banner=Style(PALETTE, color='black', bgcolor='supporter2'),
        intro=Style(PALETTE, color='black', bgcolor='supporter3'),
        group=Style(PALETTE, color='black', bgcolor='supporter3',
            diapcolor='supporter3', diapbgcolor='black'),
        menu=Style(PALETTE, color='black', bgcolor='supporter3',
            link='middle', hover='light',
            diapcolor='supporter3', diapbgcolor='black'),
        body=Style(PALETTE, color='black', bgcolor='white'),
        p=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        li=Style(PALETTE, color='supporter3', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite2', hover='supporter1'),
    )
    STYLES_DARK = dict(
        logo=Style(PALETTE, color='supporter2', bgcolor='supporter1'),
        hr=Style(PALETTE, color='light'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='hilite2', bgcolor='hilite1',
            link='middle', hover='light'),
        h2=Style(PALETTE, color='white', bgcolor='hilite3',
            diapcolor='hilite3', diapbgcolor='white'),
        banner=Style(PALETTE, color='white', bgcolor='black'),
        intro=Style(PALETTE, color='white', bgcolor='dark'),
        group=Style(PALETTE, color='white', bgcolor='dark',
            diapcolor='dark', diapbgcolor='white'),
        menu=Style(PALETTE, color='white', bgcolor='dark',
            link='middle', hover='light',
            diapcolor='dark', diapbgcolor='white'),
        body=Style(PALETTE, color='white', bgcolor='black'),
        p=Style(PALETTE, color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite1', hover='supporter1'),
        li=Style(PALETTE, color='supporter3', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite2', hover='supporter1'),
    )
    STYLES_SMOOTH = dict(
        logo=Style(PALETTE, color='warm', bgcolor='light'),
        hr=Style(PALETTE, color='dark'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='hilite3', bgcolor='white',
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite4', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='hilite4'),
        banner=Style(PALETTE, color='hilite3', bgcolor='dark'),
        intro=Style(PALETTE, color='hilite2', bgcolor='middle'),
        group=Style(PALETTE, color='light', bgcolor='dark',
            diapcolor='dark', diapbgcolor='light'),
        menu=Style(PALETTE, color='light', bgcolor='dark',
            link='middle', hover='light',
            diapcolor='dark', diapbgcolor='light'),
        body=Style(PALETTE, color='supporter1', bgcolor='hilite1'),
        p=Style(PALETTE, color='supporter3', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite2', hover='supporter1'),
        li=Style(PALETTE, color='supporter3', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='hilite2', hover='supporter1'),
    )
    STYLES_CONTRAST = dict(
        logo=Style(PALETTE, color='warm', bgcolor='light'),
        hr=Style(PALETTE, color='dark'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='hilite1', bgcolor='white',
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite2', bgcolor='hilite2',
            diapcolor='hilite1', diapbgcolor='hilite4'),
        banner=Style(PALETTE, color='hilite3', bgcolor='black'),
        intro=Style(PALETTE, color='light', bgcolor='dark'),
        group=Style(PALETTE, color='black', bgcolor='light',
            diapcolor='light', diapbgcolor='black'),
        menu=Style(PALETTE, color='black', bgcolor='light',
            link='middle', hover='light',
            diapcolor='light', diapbgcolor='black'),
        body=Style(PALETTE, color='white', bgcolor='hilite2'),
        p=Style(PALETTE, color='white', bgcolor='black',
            diapcolor='warm', diapbgcolor='white',
            link='light', hover='supporter1'),
        li=Style(PALETTE, color='white', bgcolor='black',
            diapcolor='warm', diapbgcolor='white',
            link='light', hover='supporter1'),
    )
    MOODS = {
        'light': Mood('Light', STYLES_LIGHT),
        'normal': Mood('Normal', STYLES_NORMAL),
        'dark': Mood('Dark', STYLES_DARK),
        'smooth': Mood('Smooth', STYLES_SMOOTH),
        'contrast': Mood('Contrast', STYLES_CONTRAST),
    }
    """
if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
