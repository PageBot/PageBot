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
from pagebot.contexts import defaultContext as context
from pagebot.contributions.filibuster.blurb import Blurb

#text = Blurb().getBlurb('article_ankeiler', noTags=True)
text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin."""

t = context.newString(text,
                style=dict(fontSize=30,
                           hyphenationHead=4,
                           hyphenationTail=3))

w=554 # change width to see other hyphenations

W = 1000
H = 2000
context.newPage(W, H)

context.hyphenation(True)
context.textBox(t, (100,600,w,400))
context.fill(None)
context.stroke(0)
context.rect(100,600,w,600)

context.hyphenation(False)
context.textBox(t, (100,100,w,400))
context.fill(None)
context.stroke(0)
context.rect(100,100,w,600)
