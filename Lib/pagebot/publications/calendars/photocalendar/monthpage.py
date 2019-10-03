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
#     calendars/photocalendar/monthpage.py
#
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.constants import *
from pagebot.toolbox.dating import Dating, now

def makeMonthPage(page, month, year=None):
    """Cover template for photo books.
    """
    if year is None:
        year = now().year
    CalendarMonth(Dating(month=month, year=year), parent=page, fill=0.5, conditions=[Fit()])

