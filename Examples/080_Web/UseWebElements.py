# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseWebElements.py
#
import os
from pagebot.elements import *

from pagebot.publications.simplesite import SimpleSite, Navigation
from pagebot.contexts.htmlcontext import HtmlContext

context = HtmlContext()

NAME = "UseWebElements"

website = SimpleSite(autoPages=4, name=NAME, context=context)
view = website.newView('Mamp')

page = website[1]
page.name = 'index.html'
newRect(w=300, h=200, parent=page)
Navigation(parent=page, name='Navigation')
print(page.elements)
website.export('docs/UseWebElements')
os.system(u'open "%s"' % view.getUrl(NAME))
