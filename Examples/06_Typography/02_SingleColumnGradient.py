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
#     030_SingleColumnYPositions.py
#
#     Draw a single columns with various typographic styles inside and show the
#     baselines, using the view.showBaselineGrid = True display option.
#     The text column includes a footnote reference with baseline shift.
#
#from pagebot.contexts.flatcontext import FlatContext
from pagebot import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color, whiteColor, grayColor
from pagebot.toolbox.units import em, pt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import * # Import all constants for convenience
from pagebot.gradient import Gradient, Shadow

#context = FlatContext()
context = getContext()

W = H = pt(1000) # Document size optionally defined as units
PADDING = pt(80) # Page padding on all sides
BASELINE = em(1.4)

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

# Get the Font instances, so they can be queried for metrics.
fontVF = findFont('RobotoDelta-VF') # Use the RobotoDelta Variable font for this example
print(fontVF.axes) # Uncomment to see axes and values for this VF

location = dict(XTRA=320) # SLight condensed Roman
font = fontVF.getInstance(location)

location = dict(wght=700, XTRA=290) # Bold condensed
bold = fontVF.getInstance(location)

# Defined styles
headStyle = dict(font=bold, fontSize=125, leading=BASELINE, textFill=whiteColor, hyphenation=False,
    paragraphBottomSpacing=em(0.2))
style = dict(font=font, fontSize=24, leading=BASELINE, textFill=0.15, hyphenation=False)

# Make BabelString from multiple cascadeing styles
t = context.newString('Head hkpx\n', style=headStyle) # Start with headline
t += context.newString(text * 5, style=style) # Body text
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, baselineGrid=BASELINE, originTop=False)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showBaselineGrid = False # Show default baseline grid of the column lines.
view.showPadding = False # Make True to see the gray frame of the padding box.
# Get the first (and only) page
page = doc[1]
# Prepare a gradient to the text box. See gradient.py for options.
# Note that the colors can be set as Color instance, and also for
# convenience as tuples for default RGB.
gradient = Gradient(colors=(whiteColor, color(spot=300)))
# Prepare a shadow for this text box. Defining them separate and they can be reused.
shadow = Shadow(offset=pt(15 -15), blur=pt(30), color=color(0.2))
textShadow = Shadow(offset=pt(8, -8), blur=pt(16), color=color(spot=300).darker())
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
# Red frame to show position and dimensions of the text box element.
# Default behavior of the textbox is to align the text at "top of the em-square".
c1 = newTextBox(t, parent=page, w=500, yAlign=TOP,
    showOrigin=True, showBaselineGrid=False, gradient=gradient, 
    textShadow=textShadow, shadow=shadow,
    padding=pt(24), # Padding inside gradient rect
    conditions=[Left2Left(), Top2Top(), Fit2Height(), Fit2Width()])
# Solve the page/element conditions, so the text box as it's position and size.
doc.solve()

# Export the document to this PDF file.
doc.export('_export/SingleColumnYPositions.pdf')

