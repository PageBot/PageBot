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
#     happyholidays.py
#
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import color

class HappyHolidays(BaseTheme):
    NAME = 'Happy Holidays'
    BASE_COLORS = dict(
        base0=color(1, 0, 0.2),
        base1=color(0.7, 0.1, 0.2),
        base2=color(0.9, 0, 0.3),
        base3=color(0.5, 0.96, 0.2),
        base4=color(0, 1, 0),
        base5=color(0.55, 0.5, 0.5),
    )
    
if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
