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
## Works with this version of DrawBot:
## https://github.com/thomgb/drawbot
## download my DrawBot: https://www.dropbox.com/s/xsu1mz89ipo5x3y/DrawBot.dmg?dl=0
from pagebot.document import Document
from pagebot import getContext
from pagebot.elements import *
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.toolbox.color import color

#from pagebot.contexts.flatcontext import FlatContext
#context = FlatContext()
context = getContext()

#text = Blurb().getBlurb('article_ankeiler', noTags=True)
text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin."""

t = context.newString(text,
                style=dict(fontSize=30,
                           hyphenationHead=4,
                           hyphenationTail=3))

w=554 # change width to see other hyphenations

W = 1000
H = 1000

doc = Document(w=W, h=H, autoPages=1)
page = doc[1]

t = context.newString(text,
                style=dict(fontSize=30,
                           hyphenationHead=4,
                           hyphenation=True,
                           hyphenationTail=3))

newTextBox(t, x=100, y=600, w=w, h=400, parent=page, border=1, fill=color(1, 0, 0))

t = context.newString(text,
                style=dict(fontSize=30,
                           hyphenationHead=4,
                           hyphenation=False,
                           hyphenationTail=3))

newTextBox(t, x=100, y=100, w=w, h=400, parent=page, border=1, fill=color(1, 0, 0))

doc.export('_export/AdvancedHyphenation.pdf')

