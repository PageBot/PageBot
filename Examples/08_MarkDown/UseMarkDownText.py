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
#     UseMarkDownText.py
#
from pagebot.contexts.platform import getContext
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.typesetter import Typesetter
from pagebot.toolbox.color import color, blackColor
from pagebot.constants import A4

W, H = A4

MARKDOWN_PATH = 'EmbeddedPython.md'

context = getContext()

doc = Document(originTop=False, w=W, h=H, autoPages=1)
#print(doc.styles.keys())
doc.addStyle('h1', dict(textFill=blackColor), force=True)
doc.addStyle('h2', dict(textFill=blackColor), force=True)
doc.addStyle('p', dict(textFill=blackColor), force=True)

ts = Typesetter(context, doc.styles, g)
ts.typesetFile(MARKDOWN_PATH)

page = doc[1] # Get the first/single page of the document.
page.padding = 40 # TODO: order if 4 values?

# Make rect as page element centered with centered origin.
conditions = [Fit()]
g = newTextBox(parent=page, conditions=conditions, textFill=blackColor, autoPages=10)

# Solve the layout conditions of the red rectangle.
# Show if one of the conditions failed to solve.
score = page.solve()
if score.fails:
    print('Failed conditions', score.fails)


# Set the view parameters for the required output.
view = doc.getView()
view.padding = 0 # Make view padding to show crop marks and frame
view.showFrame = True # Show frame of the page in blue
#view.showPadding = True
view.showCropMarks = True # Show crop marks

doc.export('_export/UseMarkdownText.pdf')
