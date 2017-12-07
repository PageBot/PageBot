# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     UseBabelStrings.py
#
#     BabelString instances are wrappers around formatted strings,
#     hiding their context. For DrawBot BabelStrings (bs.s) contain
#     OSX/IOS FormattedStrings.
#     For FlexContext, equivalent text-formatted structures are implemented.
#
from pagebot.contexts import defaultContext as c

W = H = 1000
M = 100

EXPORT_PATH = '_export/UseBabelStrings.pdf'
# Create a page and set y on top margin.
c.newPage(W, H)
y = H - M
# Create formatted string, with default settings of font, fontSize and textFill color
bs = c.newString('This is a formatted BabelString')
c.text(bs, (100, y))
# Add string with formatting style dict
bs += c.newString('\nAdd an other string with format', style=dict(textFill=(1, 0, 0), fontSize=20, rLeading=1.4))
y -= 50
c.text(bs, (100, y))


c.saveImage(EXPORT_PATH)