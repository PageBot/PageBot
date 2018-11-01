# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2017 Thom Janssen <https://github.com/thomgb>
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     Hyphenation.

from pagebot.document import Document
from pagebot import getContext
from pagebot.elements import *
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.toolbox.color import color
from pagebot.toolbox.units import pt
from pagebot.fonttoolbox.objects.font import findFont

#from pagebot.contexts.flatcontext import FlatContext
#context = FlatContext()
context = getContext()
bungee = findFont('Bungee-Regular')
txt = Blurb().getBlurb('article_ankeiler', noTags=True)

w = 400 # change width to see other hyphenations
h = 400

W = 1200
H = 1500
doc = Document(w=W, h=H, autoPages=1)
page = doc[1]

style = dict(font=bungee, fontSize=pt(24), hyphenationHead=4, hyphenationTail=3, hyphenation=True)
t = context.newString(txt, style=style)
newTextBox(t, x=100, y=H-100, w=w, h=h, parent=page, border=1, fill=color(0.3, 0.2, 0.1, 0.5))

style['hyphenationTail'] = 400
t = context.newString(txt, style=style)
newTextBox(t, x=100, y=H-100-h, w=w, h=h, parent=page, border=1, fill=color(1, 1, 0))

style['hyphenation'] = False
t = context.newString(txt, style=style)
newTextBox(t, x=100, y=H-100-2*h, w=w, h=h, parent=page, border=1, fill=color(1, 0, 1))
doc.export('_export/Hyphenation.pdf')

