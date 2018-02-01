#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2017 Thom Janssen <https://github.com/thomgb>
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
## Works with this version of DrawBot:
## https://github.com/thomgb/drawbot
## download my DrawBot: https://www.dropbox.com/s/xsu1mz89ipo5x3y/DrawBot.dmg?dl=0
from pagebot.contexts import defaultContext as c

t = c.newString("programmatic",
                style=dict(fontSize=30,
                           hyphenationHead=4,
                           hyphenationTail=3))
c.hyphenation(True)

w=200 # change width to see other hyphenations

c.newPage(1000, 2000)
c.textBox(t, (100,100,w,600))
c.fill(None)
c.stroke(0)
c.rect(100,100,w,600)
