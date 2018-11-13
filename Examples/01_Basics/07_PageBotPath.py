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
#     07_PageBotPath.py
#
#     Draw a string outline as PageBotPath.
#
from pagebot.toolbox.units import pt
from pagebot.contexts import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.constants import A3

H, W = A3
context = getContext()
doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
page = doc[1]
c = (Right2Right(), Top2Top(), Float2Left())

# TODO: add to frame?
bungee = findFont('BungeeOutline-Regular')

t = newText('*PageBot Path*', parent=page, conditions=c, style={'fill': 1, 'fontSize': 32, 'stroke': 0, 'strokeWidth': 2})

path = newPageBotPath(context=context)
path.text('ABC', style=dict(font=bungee, fontSize=pt(120)))
newPaths(path, parent=page, fill=(1, 0, 0), conditions=c)

roboto = findFont('Roboto-Bold')
path = PageBotPath(context=context)
path.text('CDE', style=dict(font=roboto, fontSize=pt(240)))
path = path.removeOverlap()
newPaths(path, parent=page, fill=(1, 1, 0), stroke=0, conditions=c)

# FIXME: y-translation always same direction?
#path.translate((-60, 200))

page.solve()
doc.build()