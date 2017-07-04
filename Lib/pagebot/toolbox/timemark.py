# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     timemark.py
#
class TimeMark(object):
    u"""TimeMarks are used by elements to keep style attributes sorted in a time line."""
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

     