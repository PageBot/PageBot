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

class CalendarMonth(Element):

	def __init__(self, date=None, **kwargs):
		Element.__init__(self, **kwargs)
		if date is None:
			date = now()
		self.date = date

	def build(self, view, origin, **kwargs):
	    print(self.date, self.date.monthName)
	    for week in self.date.calendarMonth:
	    	w = []
	    	for day in week:
	    		w.append((day.dayName, day.day))
	    	print(w)
