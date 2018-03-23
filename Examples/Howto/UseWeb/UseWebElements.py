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
#     UseWebElements.py
#
from __future__ import print_function
from pagebot.elements import *

from pagebot.publications.website import Website, Navigation


website = Website(autoPages=4)
website.newView('Mamp')
website.info.cssPath = None
website.info.htmlPath = None
website.info.bodyPath = None

page = website[1]
page.name = 'ABCDE'
newRect(w=300, h=200, parent=page)
Navigation(parent=page, name='Navigation')
print(page.elements)

website.export('_export/UseWebElements')