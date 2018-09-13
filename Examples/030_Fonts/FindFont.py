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
#     = Under development =
#
#     Some examples how to find Font instances, for the given installed fonts.
#
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.family import findFamily
from pagebot.fonttoolbox.objects.font import findFont

context = getContext()

fontNames = context.installedFonts()
# Total installed fonts: 1993
print('Total installed fonts: %d' % len(fontNames))

fontNames = context.installedFonts('Verdana')
# ['Verdana', 'Verdana-Bold', 'Verdana-BoldItalic', 'Verdana-Italic']
print(fontNames)

fontNames = context.installedFonts('Verdana-BoldItalic')
# ['Verdana-BoldItalic']
print(fontNames)

fontNames = context.installedFonts(['Verdana', 'Georgia'])
# ['Georgia', 'Georgia-Bold', 'Georgia-BoldItalic', 'Georgia-Italic', 'Verdana', 'Verdana-Bold', 'Verdana-BoldItalic', 'Verdana-Italic']
print(fontNames)
 
family = findFamily('Roboto')
# None
print(family)

font = findFont('Roboto')
# None
print(font)

robotoRegular = findFont('Roboto-Regular')
# <Font Roboto-Regular>
print(robotoRegular)

font = findFont('Roboto-cannot-be-found', default='Roboto-Regular')
# <Font Roboto-Regular>
print(font)

font = findFont('Roboto-cannot-be-found', default=robotoRegular)
# <Font Roboto-Regular>
print(font)



