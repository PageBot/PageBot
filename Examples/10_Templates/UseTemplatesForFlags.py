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
#     UseTemplatesForFlags.py
#
#     Shows the usage of templates, both as default in the document as well
#     as applying on an existing page.
#     The elements are copied from the template page, so not reference to the
#     original elenents remains in the page after thhe apply.
#     Note that also the apply will remove all previous element from the page,
#     so the order is important: first apply a new template, then add elements
#     to a specific page.
#

from pagebot import getContext
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.document import Document
from pagebot.toolbox.color import color, whiteColor

# Document is the main instance holding all information about the document togethers (pages, styles, etc.)

context = getContext()

PageSize = 500, 400

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseTemplates.pdf'

def makeTemplate(w, h, french=False):
    """Make template for the main page (flag), for the given (w, h) size.
    The optional **french** flag creates a French flag, otherwise Italian."""

    # Creat enew Template instance for the given size.
    template = Template(w=w, h=h) # Create template.
    # Add named text box to template for main specimen text.
    if french:
        rightColor = 0, 0, 0.5 # r, g, b Make French flag
    else:
        rightColor = 0, 0.5, 0 # r, g, b Make Italian flag.
    # Make 2 formatted strings with white text,
    fsLeft = context.newString('Template box left', style=dict(textFill=whiteColor))
    fsRight = context.newString('Template box right', style=dict(textFill=whiteColor))

    newTextBox(fsLeft, w=w/3, fill=color(1, 0, 0), padding=10,
        parent=template, conditions=[Left2Left(), Top2Top(), Fit2Height()])

    newTextBox(fsRight, w=w/3, fill=rightColor, padding=10,
        parent=template, conditions=[Right2Right(), Top2Top(), Fit2Height()])
    return template

def makeDocument():
    """Make a new document, using the rs as root style."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W, H = PageSize

    # Create overall template, and set it in the document as default template for new pages.
    template = makeTemplate(W, H)

    doc = Document(title='Color Squares', w=W, h=H, originTop=False, autoPages=3, defaultTemplate=template)

    view = doc.getView()
    view.padding = 0 # Don't show cropmarks in this example.

    # Get list of pages with equal y, then equal x.
    #page = [1][0] # Get the single page from the document.
    page0 = doc.getPage(1) # Get page by pageNumber, first in row (there is only one now in this row).

    # Overwrite the default template by another template (in this case with different color).
    # Note that this way it is possible to mix different page sizes in one document.
    # The elements are copied from the template page, so not reference to the
    # original elenents remains in the page after thhe apply.
    # Note that also the apply will remove all previous element from the page,
    # so the order is important: first apply a new template, then add elements
    # to a specific page.
    page1 = doc.getPage(1)
    page1.applyTemplate(makeTemplate(W, H, True))

    # Recursively solve the conditions in all pages.
    # If there are failing conditions, then the status is returned in the Score instance.
    score = doc.solve()
    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

d = makeDocument()
d.export(EXPORT_PATH)

