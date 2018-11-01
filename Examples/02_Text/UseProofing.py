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
from pagebot.publications.proofing.pagewide import PageWide
from pagebot.constants import A3
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import getFontPaths

print(sorted(getFontPaths().keys()))
font = findFont('BungeeOutline-Regular')
HEIGHT, WIDTH = A3
context = getContext()
context.newPage(pt(WIDTH), pt(HEIGHT))
proof = PageWide(context)
SIZE = 54
context.translate(SIZE, HEIGHT - SIZE)
proof.draw(font, 'abcdefghijklmnopqrstuvwxyz', SIZE)
