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
#     intothewoods.py
#
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor
from pagebot.toolbox.units import px

class IntoTheWoods(BaseTheme):
    u"""The IntoTheWoods theme is ..."""

    NAME = 'Into the Woods'
    PALETTE = Palette(
        black=spot(350),
        white=whiteColor,
        # Colors with gray tone function
        dark=spot('warmgray10u'),
        middle=spot('warmgray8u'),
        light=spot('warmgray4u'),
        # Temperature
        warm=spot(348),  
        cold=spot('processblue'),
        # Highlight
        hilite1=spot(305),
        hilite2=spot(2975),
        hilite3=spot(381),   
        # Supporters
        supporter1=spot(392),   
        supporter2=spot(398),   
        supporter3=spot(376),
        supporter3_light=spot(376).lighter(0.6),
        # Logo/corporate identity color 
        logo1=spot(165), # DesignDesign.Space logo color
        logo2=spot(286),
    )
    STYLES_LIGHT = dict(
        body=Style(PALETTE, color='black', bgcolor='black'),
        page=Style(PALETTE, color='black', bgcolor='white'),
        logo=Style(PALETTE, color='logo1', bgcolor='supporter1'),
        hr=Style(PALETTE, color='supporter3'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='white', bgcolor='black', 
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        h3=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        banner=Style(PALETTE, color='middle', bgcolor='white'),
        intro=Style(PALETTE, color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=Style(PALETTE, color='black', bgcolor='hilite1',
            diapcolor='white', diapbgcolor='dark'),
        menu=Style(PALETTE, color='black', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='black',
            link='hilite2', hover='supporter2'),
        p=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        li=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        side=Style(PALETTE, color='black', bgcolor='hilite3',
            padding=12, 
            link='middle', hover='black'),
    )
    STYLES_NORMAL = dict(
        body=Style(PALETTE, color='black', bgcolor='black'),
        page=Style(PALETTE, color='black', bgcolor='white'),
        logo=Style(PALETTE, color='logo1', bgcolor='supporter1'),
        hr=Style(PALETTE, color='supporter3'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='white', bgcolor='black', 
            link='middle', hover='light'),
        h2=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        h3=Style(PALETTE, color='hilite3', bgcolor='white',
            diapcolor='white', diapbgcolor='hilite3'),
        banner=Style(PALETTE, color='middle', bgcolor='white'),
        intro=Style(PALETTE, color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=Style(PALETTE, color='black', bgcolor='hilite1',
            diapcolor='white', diapbgcolor='dark'),
        menu=Style(PALETTE, color='black', bgcolor='hilite1',
            diapcolor='hilite1', diapbgcolor='black',
            link='hilite2', hover='supporter2'),
        p=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        li=Style(PALETTE, color='black', bgcolor='white',
            diapcolor='white', diapbgcolor='black',
            link='warm', hover='cold'),
        side=Style(PALETTE, color='black', bgcolor='hilite3',
            padding=12, 
            link='middle', hover='black'),
    )
    STYLES_DARK = dict(
        body=Style(PALETTE, color='white', bgcolor='black'),
        page=Style(PALETTE, color='white', bgcolor='black'),
        logo=Style(PALETTE, color='logo1', bgcolor='supporter1'),
        hr=Style(PALETTE, color='supporter3'), # <hr> Horizontal ruler
        h1=Style(PALETTE, color='black', bgcolor='white', 
            link='middle', hover='dark'),
        h2=Style(PALETTE, color='white', bgcolor='hilite3',
            diapcolor='hilite3', diapbgcolor='white'),
        h3=Style(PALETTE, color='white', bgcolor='hilite3',
            diapcolor='hilite3', diapbgcolor='white'),
        banner=Style(PALETTE, color='white', bgcolor='middle'),
        intro=Style(PALETTE, color='white', bgcolor='supporter2',
            link='white', hover='warm'),
        group=Style(PALETTE, color='hilite1', bgcolor='black',
            diapcolor='dark', diapbgcolor='white'),
        menu=Style(PALETTE, color='hilite1', bgcolor='black',
            diapcolor='black', diapbgcolor='hilite1',
            link='hilite2', hover='supporter2'),
        p=Style(PALETTE, color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='cold', hover='warm'),
        li=Style(PALETTE, color='white', bgcolor='black',
            diapcolor='black', diapbgcolor='white',
            link='warm', hover='cold'),
        side=Style(PALETTE, color='hilite3', bgcolor='black',
            padding=12, 
            link='middle', hover='light'),
    )
    MOODS = {
        'light': Mood('Light', STYLES_LIGHT),
        'normal': Mood('Normal', STYLES_NORMAL),
        'dark': Mood('Dark', STYLES_DARK),
        #'smooth': Mood('Smooth', STYLES_SMOOTH),
        #'contrast': Mood('Contrast', STYLES_CONTRAST),
    }

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
