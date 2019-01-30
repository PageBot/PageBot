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
#     ContextBehavior.py
#
#     This example script does focus on the difference between exporting
#     for DrawBotContext documents and HtmlContext documents, both
#     using the same MarkDown file as source. 
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.htmlcontext import HtmlContext
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.toolbox.color import color, blackColor
from pagebot.constants import A4
from pagebot.toolbox.units import pt, em

W, H = A4
PADDING = pt(40) # Simple page padding
G = pt(6)

# Path to the MarkDown source file
MARKDOWN_PATH = 'EmbeddedPython.md'

pdfContext = DrawBotContext()
htmlContext = HtmlContext()

styles = dict(
    h1=dict(textFill=color('red'), fontSize=pt(24), leading=em(1.4), paragraphBottomSpacing=pt(12)),
    h2=dict(textFill=color(0.3), fontSize=pt(18), leading=em(1.4),
        paragraphTopSpacing=pt(12), paragraphBottomSpacing=pt(12)),
    p=dict(textFill=blackColor, fontSize=pt(12), leading=em(1.4), firstLineIndent=pt(24), firstColumnIndent=0),
    li=dict(textFill=color('green'), tabs=pt(8, 16, 24, 36, 48), fontSize=pt(12), leading=em(1.4), 
        indent=16, firstLineIndent=0),
    strong=dict(textFill=color('red'), firstLineIndent=0),
    em=dict(textFill=color('blue'), firstLineIndent=0),
)

# Create the overall documents, side by side for the two contexts.
pdfDoc = Document(originTop=False, name='Demo PDF MarkDown', w=W, h=H, context=pdfContext)
htmlDoc = Document(originTop=False, name='Demo HTML MarkDown', context=htmlContext, viewId='Site')

for doc in (pdfDoc, htmlDoc):
    # Set the view parameters for the required output.
    view = doc.view
    view.padding = pt(40) # Make view padding to show crop marks and frame
    view.showFrame = True # Show frame of the page in blue
    view.showPadding = True
    view.showCropMarks = True # Show crop marks
    view.showRegistrationMarks = True
    view.showNameInfo = True

    # Read the markdown file, where all elements (embedded code blocks) are pasted
    # on a galley element, in sequential order. No execution of code blocks
    # takes place yet.
    t = Typesetter(doc.context, styles=styles)
    galley = t.typesetFile(MARKDOWN_PATH)

    # Make a simple template: one page with one column.
    page = doc[1] # Get the first/single page of the document.
    page.padding = PADDING # Set the padding of this page.
    # Make a text box, fitting the page padding on all sides.
    newTextBox(parent=page, name='Box', conditions=[Fit()])
    page.solve() # Solve the fitting condition.
    
    # Create a new page after the current one
    page = page.next
    page.padding = PADDING # Set the padding of this page.
    # Make a text box, fitting the page padding on all sides.
    newTextBox(parent=page, name='Box', w=(page.pw-G)/2, fill=0.9,
        conditions=[Left2Left(), Top2Top(), Fit2Bottom(), Overflow2Next()], 
        nextElement='Box2', prefix='AAA')
    newTextBox(parent=page, name='Box2', w=(page.pw-G)/2, fill=0.9,
        conditions=[Right2Right(), Top2Top(), Fit2Bottom()],
        prefix='AAA')

    # Create the Composer instance that will interpret the galley.
    composer = Composer(doc)

    # Create the global targets dictionary with objects that can be used during
    # interpretation of the markdown elements on the galley. The composer instance
    # will run sequentially through the elements, executing the code blocks. 
    # This may cause the shifting of target for the text elements to another block
    # or another page.
    page1 = doc[1]
    targets = dict(doc=doc, page=page1, box=page1.select('Box'), composer=composer)
    composer.compose(galley, targets=targets)

    # Now the targets dictionary is filled with results that were created during
    # execution of the code blocks, such as possible errors and warnings.
    # Also it contains the latest “box”
    print('Keys in target results:', targets.keys())
    print('Errors:', targets['errors'])
    print('Number of verbose feedback entries:', len(targets['verbose']))
    print('Values created in the code block: aa=%s, bb=%s, cc=%s' % (targets['aa'], targets['bb'], targets['cc']))

    doc.solve()

# Save the created document as (2 page) PDF.
pdfDoc.export('_export/ContextBehavior.pdf')
htmlDoc.export('_export/ContextBehaviorSite')
