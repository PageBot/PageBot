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

from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.publications.proofing.pagewide import PageWide
from pagebot.constants import A3
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import getFontPaths

print(getFontPaths())
font = findFont('Roboto-Bold')
WIDTH, HEIGHT = A3
context = getContext()
context.newPage(pt(WIDTH), pt(HEIGHT))
proof = PageWide(context)
SIZE = 54
context.translate(SIZE, SIZE)
proof.draw(font, 'abcdefghijklmnopqrstuvwxyz', SIZE)