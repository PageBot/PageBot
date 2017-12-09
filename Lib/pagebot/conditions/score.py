# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
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
