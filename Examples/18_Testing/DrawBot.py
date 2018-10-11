#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DrawBot.py
#

import drawBot
import math, os, random
from pagebot.contexts.drawbotcontext import DrawBotContext

attrs = []

for k in drawBot.__dict__.keys():
    if not (k in math.__dict__ or k in os.__dict__ or k in random.__dict__):
        #print(k)
        attrs.append(k)
        
print('Not in PageBot')

for a in attrs:
    if a not in DrawBotContext.__dict__.keys():
        print('* %s' % a)

print('Not in DrawBot')

for k in DrawBotContext.__dict__.keys():
    if k not in attrs:
        print('* %s' % k)
    