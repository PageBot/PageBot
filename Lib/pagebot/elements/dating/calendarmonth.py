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
#	  calendarmonth.py
#
from pagebot.elements import Element
from pagebot.toolbox.dating import now

class CalendarMonth(Element):

    def __init__(self, date=None, **kwargs):
        if date is None:
            date = now()
        self.date = date
        self.calendarMonth = date.calendarMonth

        Element.__init__(self, **kwargs)
    """
    def _get_colNames(self):

    	colNames = []
    	for day in self.calendarMonth[0]:
    		colNames.append(day.dayName)
    colNames = property(_get_colNames)
	"""
