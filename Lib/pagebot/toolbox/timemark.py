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
#     timemark.py
#
class TimeMark:
    """TimeMarks are used by elements to keep style attributes masters sorted 
    in a time line, and to interpolate (blend) between them."""
    def __init__(self, t, style):
        self.t = t
        self.style = style

    def __repr__(self):
        return '[TimeMark %0.2f]' % self.t

    def __lt__(self, tm):
        return self.t < tm.t

    def __le__(self, tm):
        return self.t <= tm.t

    def __gt__(self, tm):
        return self.t > tm.t

    def __ge__(self, tm):
        return self.t >= tm.t

    def __eq__(self, tm):
        return self.t == tm.t

    def blend(self, tm, t, name):
        u"""Answers the blended value between self and tm at time t for 
        the name attribute of self.style.


        tm1 = TimeMark()
        """
