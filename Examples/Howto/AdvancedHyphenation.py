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
## This works with the current (3.97) version of DrawBot
from pagebot.contexts import defaultContext as c
"""
Hyphenation with head and tail
TODO:
    - show hyphen if hyphenated...
    > make it work in drawBot, extra aguments in FormattedString (headHyphenation=4, tailHyphenation=3)
    >> then drawBot.context.baseContext.BaseContext.hyphenateAttributedString will take care if it (eventually)
"""
t = "programmatic"
fs = c.newString(t, style=dict(fontSize=70, language='en'))
softHyphen = unichr(0x00AD)

# set head and tail
head = 4
tail  = 4

print "lenght of string:", len(fs)

hyphenPositions=[]
for i in range(len(fs)):
    p = fs.getNSObject().lineBreakByHyphenatingBeforeIndex_withinRange_(i, (0, len(fs)))
    #print p
    if head <= p <= len(fs)-tail:
        hyphenPositions.append(p)

hyphenPositions=list(set(hyphenPositions))
hyphenPositions.sort()
print "Hyphenation indexes:", hyphenPositions

a=fs
b=fs

n=0
for p in hyphenPositions:
    a=a[:p+n] + "-" + a[p+n:] # hyphen, show hyphenation
    b=b[:p+n] + softHyphen + b[p+n:] # softHyphen here can the word hyphenate 

    n+=1 # hyphenationPositions are 0+n, where n = number of hyphenation positions
         # that are already defined, because we add (soft)hyphens...

c.newPage(1000, 2000)

# the hard hyphens:
c.textBox(a,(20,500,900,500))

# the soft hyphens:
w = 472 # change width to see hyphenations
c.textBox(b, (20,50,w,500))
c.fill(None)
c.stroke(0)
c.rect(20,50,w,500)
