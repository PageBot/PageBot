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
#     score.py
#       
class Score:
    def __init__(self):
        self.result = 0
        self.fails = []

    def __repr__(self):
        return 'Score: %s Fails: %d' % (self.result, len(self.fails))
