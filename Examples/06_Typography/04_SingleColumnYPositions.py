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
#     04_SingleColumnYPositions.py
#
#     Draw a single columns with various typographic styles inside and show the
#     baselines, using the view.showBaselineGrid = True display option.
#     The text column includes a footnote reference with baseline shift.
#

from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, pt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import * # Import all constants for convenience

context = getContext()

W = H = pt(1000) # Document size optionally defined as units
PADDING = pt(80) # Page padding on all sides
BASELINE = em(1.4)

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

# Get the Font instances, so they can be queried for metrics.
font = findFont('Roboto-Regular')
bold = findFont('Roboto-Bold')

# Defined styles
headStyle = dict(font=bold, fontSize=125, leading=BASELINE, textFill=0.1, hyphenation=False,
    paragraphBottomSpacing=em(0.2))
style = dict(font=font, fontSize=24, leading=BASELINE, textFill=0.15, hyphenation=False)

# Make BabelString from multiple cascadeing styles
t = context.newString('Å Head hkpx\n', style=headStyle) # Start with headline
t += context.newString(text * 5, style=style) # Body text
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, baselineGrid=BASELINE, originTop=False)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showBaselineGrid = False # Show default baseline grid of the column lines.
view.showPadding = True
# Get the first (and only) page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
# Red frame to show position and dimensions of the text box element.
# Default behavior of the textbox is to align the text at "top of the em-square".
c1 = newTextBox(t, parent=page, w=500, stroke=(1, 0, 0), yAlign=TOP,
    showOrigin=True,
    showBaselineGrid=False, 
    conditions=[Left2Left(), Top2Top(), Fit2Height(), Fit2Width()])
# Solve the page/element conditions, so the text box as it's position and size.
doc.solve()

# Get the position of the first baseline of the text.
firstLine = c1.textLines[0]
#print(sorted(c1.baselines))
#print(firstLine, firstLine.y)
#print(firstLine[0].fontMatrix)
#newLine(x=0, y=firstLine.y, w=page.pl, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
#newLine(x=c1.x, y=c1.h-firstLine.y-firstLine.xHeight, w=c1.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
#newLine(x=c1.x, y=c1.h-firstLine.y-firstLine.capHeight, w=c1.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
# FIX: Something with the ascender position? Or is it showing the max-value for all glyphs?
#newLine(x=c1.x, y=c1.h-firstLine.y-firstLine.ascender, w=c1.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
#newLine(x=c1.x, y=c1.h-firstLine.y-firstLine.descender, w=c1.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)

# Export the document to this PDF file.
doc.export('_export/SingleColumnYPositions.pdf')

