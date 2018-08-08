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
#from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.platform import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em
from pagebot.conditions import * # Import all conditions for convenience.

#context = FlatContext()
context = getContext()

W = H = 1000 # Document size
PADDING = 100 # Page padding on all sides

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

font = findFont('Roboto-Regular')

style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.3)
# Make long text to force box overflow
t = context.newString(text * 10, style=style)
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
newTextBox(t, parent=page, stroke=0.5, strokeWidth=1, conditions=[Fit()])
# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/SingleColumn.pdf')

