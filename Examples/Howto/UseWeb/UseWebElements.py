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

from pagebot.publications.website import Website


website = Website(autoPages=4)
website.newView('Mamp')
website.info.cssPath = None

website.export('_export/UseWebElements')