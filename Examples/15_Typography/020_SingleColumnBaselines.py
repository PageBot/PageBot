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
#from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.platform import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, pt
from pagebot.conditions import * # Import all conditions for convenience.

#context = FlatContext()
context = getContext()

W = H = pt(1000) # Document size optionally defined as units
PADDING = pt(120) # Page padding on all sides

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

# Get the Font instances, so they can be queried for metrics.
font = findFont('Roboto-Regular')
bold = findFont('Roboto-Bold')

# Defined styles
headStyle = dict(font=bold, fontSize=36, leading=em(1.4), textFill=0.1, hyphenation=True,
    paragraphBottomSpacing=em(0.5))
subHeadStyle = dict(font=bold, fontSize=24, leading=em(1.4), textFill=0.1, 
    paragraphBottomSpacing=em(0.2), paragraphTopSpacing=em(0.8))
style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.15, hyphenation=False)
footNoteRefStyle = dict(font=font, fontSize=18, baselineShift=em(0.2), textFill=0.2)
footNoteStyle = dict(font=font, fontSize=20, leading=em(1.4), textFill=0.6, paragraphTopSpacing=em(1))

# Make BabelString from multiple cascadeing styles
t = context.newString('Headline\n', style=headStyle) # Start with headline
t += context.newString(text * 3, style=style) # Body text
t += context.newString('Reference for a footnote.', style=style) # Body text
t += context.newString('12', style=footNoteRefStyle) # Body text
t += context.newString('\n', style=style) # Footnote referece
t += context.newString('Subhead\n', style=subHeadStyle) # Subhead
t += context.newString(text * 2 + '\n', style=style) # Body text
t += context.newString('12 '+text, style=footNoteStyle) # Footnote on new line
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showTextBoxBaselines = False
# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
c1 = newTextBox(t, parent=page, conditions=[Fit()])
#print(c.baselines)
#print(c1.baselines)
for tl in c1.textLines:
    help(tl)
    break

# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/SingleColumn.pdf')

