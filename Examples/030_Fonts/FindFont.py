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
#     FindFont.py
#
#     Some examples how to find Font instances, for the given installed fonts.
#
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import findFont

context = getContext()

fontNames = context.installedFonts('Prof')
for fontName in fontNames:
    if 'Prof' in fontName:
        print(fontName)
print(fontNames)