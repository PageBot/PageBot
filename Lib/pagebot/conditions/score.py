# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     score.py
#       
class Score(object):
    def __init__(self):
        self.result = 0
        self.fails = []

    def __repr__(self):
        return 'Score: %s Fails: %d' % (self.result, len(self.fails))
