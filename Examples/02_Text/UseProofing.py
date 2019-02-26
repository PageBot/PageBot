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
#     UseProofing.py
#
#

from pagebot import getContext
from pagebot.toolbox.units import *
#from pagebot.publications.proofing.pagewide import PageWide
from pagebot.constants import A3
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import getFontPaths

#print(sorted(getFontPaths().keys()))
font = findFont('BungeeOutline-Regular')
font = findFont('Roboto-Regular')
H, W = A3 # Landscape, reverse W, H
PADDING = p(5)
S = 'abcdefghijklmnopqrstuvwxyz'
LEADING = 1

context = getContext()
context.newPage(W, H)
y = 0
for ps in (10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 36, 40, 46, 54):
    y += ps*LEADING/2
    bs = context.newString(S, style=dict(font=font, fontSize=ps))
    tw, th = bs.size
    context.textBox(bs, (PADDING, H-PADDING-y, W-2*PADDING, th))
