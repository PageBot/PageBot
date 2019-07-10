# ----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     basecalendar.py
#
from random import random
from pagebot.constants import *
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.toolbox.color import color
from pagebot.toolbox.dating import now, Dating
from pagebot.toolbox.units import p, pt
from pagebot.publications.publication import Publication

class RRect(Rect):

    def buildElement(self, view, p, drawElements, **kwargs):
        pass

class BaseCalendar(Publication):
    """Create a default calendar for the indicated year.
    Add cover and monthly pages.

    >>> from pagebot.toolbox.dating import now
    >>> calendar = BaseCalendar(now().year)
    >>> calendar.year == now().year
    True
    >>> calendar.size # A3Square
    (297mm, 297mm)
    >>> calendar.document.export('_export/BaseCalendar.pdf')
    """

    # Default paper sizes that are likely to be used for
    # books in portrait ratio.
    PAGE_SIZES = {
        'A2': A2,
        'B2': B2,
        'A3': A3,
        'B3': B3,
        'A4': A4,
        'B4': B4,
        'A5': A5,
        'B5': B5,
        'A2Square': A2Square,
        'A3Square': A3Square,
        'A4Square': A4Square,
        'HalfLetter': HalfLetter,
        'Letter': Letter,
        'Legal': Legal,
        'JuniorLegal': JuniorLegal,
        'Tabloid': Tabloid,
        'Ledger': Ledger,
        'Statement': Statement,
        'Executive': Executive,
        'Folio': Folio,
        'Quarto': Quarto,
        'Size10x14': Size10x14,
        'A4Letter': A4Letter,
        'A4Oversized': A4Oversized,
    }
    DEFAULT_PAGE_SIZE_NAME = 'A3Square'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    def __init__(self, year=None, w=None, h=None, size=None, name=None, **kwargs):

        if year is None:
            year = now().year
        if name is None:
            name = 'Calendar %d' % year
        if w is None and h is None and size is None:
            w, h = self.PAGE_SIZES[self.DEFAULT_PAGE_SIZE_NAME]
        Publication.__init__(self, name=name, w=w, h=h, size=size, **kwargs)

        self.year = year

        self.initialize()

    def initialize(self):
        # Suggestion of cover image.
        doc = self.document
        gray = color(0.8)
        page = doc[1]
        page.bleed = bleed = p(1)
        page.padding = padding = p(4)
        newRect(parent=page, x=-bleed, y=-bleed, w=page.w+2*bleed,
            h=page.h+2*bleed, fill=gray)
        calendarYear = Dating(year=self.year).calendarYear
        for month in range(0, 12):
            page = page.next
            page.bleed = bleed
            page.padding = padding
            newRect(parent=page, x=-bleed, y=page.h/2, w=page.w+2*bleed, h=page.h/2+bleed,
                fill=gray)
            weekH = page.ph/2
            weekW = page.pw
            dayH = weekH/5
            dayW = weekW/7
            for wIndex, week in enumerate(calendarYear[month]):
                for dIndex, day in enumerate(week):
                    RRect(parent=page, w=dayW, h=dayH, fill=color(random(), 0, random()),
                        x=page.pl+dIndex*dayW, y=page.pb+page.ph/2-(wIndex+1)*dayH)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
