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
#     calendars/__init__.py
#
from pagebot.publications.calendars.photocalendar import PhotoCalendar

CALENDAR_CLASSES = {
	'Photo': PhotoCalendar, # Eanch month a photo and a table of month days
}

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
