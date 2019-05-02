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
#     02_SingleColumnBaselines.py
#
#     Draw a single columns with various typographic styles inside and show their
#     vertical positions. This allows for alignment on parts of the headline.
#

from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, pt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT
from pagebot.mining.filibuster.samplecontent import SampleContent

sampleContent = SampleContent()
# Uncomment to show the attribute names of
# available sample content.
#print(sampleContent.info)
# Dummy text
text = sampleContent.articles[0]

context = getContext()

W = H = pt(1000) # Document size optionally defined as units
PADDING = pt(120) # Page padding on all sides
BASELINE = em(1.4)

# Get the Font instances, so they can be queried for metrics.
font = findFont('PageBot-Regular')
bold = findFont('PageBot-Bold')

# Defined styles
headStyle = dict(font=bold, fontSize=36, leading=BASELINE, textFill=0.1, hyphenation=False,
    paragraphBottomSpacing=em(0.5))
subHeadStyle = dict(font=bold, fontSize=24, leading=em(1.4), textFill=0.1, 
    paragraphBottomSpacing=em(0.2), paragraphTopSpacing=em(0.8))
style = dict(font=font, fontSize=24, leading=BASELINE, textFill=0.15, hyphenation=False)
footNoteRefStyle = dict(font=font, fontSize=12, baselineShift=em(0.2), textFill=0.2)
footNoteStyle = dict(font=font, fontSize=14, leading=BASELINE, textFill=0.6, paragraphTopSpacing=em(1))

# Make BabelString from adding multiple cascading styles
t = context.newString('Headline of this example page\n', style=headStyle) # Start with headline
t += context.newString(text, style=style) # Body text
t += context.newString('Reference for a footnote.', style=style) # Body text
t += context.newString('12', style=footNoteRefStyle) # Body text
t += context.newString('\n', style=style) # Footnote referece
t += context.newString('Subhead in a column\n', style=subHeadStyle) # Subhead
t += context.newString(text + '\n', style=style) # Body text
t += context.newString('12 '+text, style=footNoteStyle) # Footnote on new line
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, baselineGrid=BASELINE)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showBaselineGrid = False # No baselines shown in grid. Element shows its own.

# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
# Red frame to show position and dimensions of the text box element.
# Default behavior of the textbox is to align the text at "top of the em-square".
# Show index of baselines on left and vertical position of baselines on the right.
c1 = newTextBox(t, parent=page, stroke=(1, 0, 0), conditions=[Fit()],
    showOrigin=True,
    showBaselineGrid=[BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT])

# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/SingleColumnBaselines.pdf')

