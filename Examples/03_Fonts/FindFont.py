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
from pagebot import getContext
from pagebot.fonttoolbox.objects.family import findFamily, getFamily
from pagebot.fonttoolbox.objects.font import getFont, findFont

context = getContext()
#
#    Installed fonts created a list of font names that are already installed.
#    This will miss out the fonts supported inside the PageBot library.
#    So for now, we'll just check on Verdana and Georgia, 
#    which is supposed to exist in all contexts.

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

# The PageBot method to look for fonts is find a fanily with an exact name match
family = getFamily('Bungee')
# <PageBot Family Bungee (5 fonts)>
print(family)

font = getFont('Verdana-BoldItalic')

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



