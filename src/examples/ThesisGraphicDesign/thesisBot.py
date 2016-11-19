# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     thesisBot.py
#
#     Document
#         Styles
#         Templates
#         Page
#            Elements (TextBox, Image, Pagenumber, Galley, ...)
#         Page   
#
#       Typesetter (read .md, write .xml, create Galley)
#       Composer (takes galley and document, copy galley elements onto pages)
#
from pagebot.document import Document
from pagebot.style import getRootStyle
from pagebot.page import Template
from pagebot.elements import Galley
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer

EXPORT_PATH = 'export/MyThesis.gif'
BOX_COLOR = 0.7
MD_PATH = 'thesis.md'

rootStyle = getRootStyle()
rootStyle['font'] = 'Georgia'
rootStyle['fontSize'] = 11

def makeThesis():
    flowId = 'myFlowName'
    myTemplate = Template(rootStyle)
    myTemplate.grid(rootStyle)
    
    # Empty image element, cx, cy, cw, ch
    myTemplate.cContainer(0, 0, 3, 2, rootStyle, fill=(0, 0, 0, 0.5)) 
    myTemplate.cContainer(0, 2, 3, 2, rootStyle, fill=(0, 0, 0, 0.5)) 
    myTemplate.cContainer(0, 4, 3, 2, rootStyle, fill=(0, 0, 0, 0.5)) 

    myTemplate.cTextBox('', 3, 0, 3, 7, rootStyle, flowId, nextBox=flowId, nextPage=1, fill=BOX_COLOR)
    #myTemplate.rect(x=200, y=200, w=300, h=400, fill=(1,0,0,0.5))
    #myTemplate.cRect(1, 1, 2, 3, style=rootStyle, fill=(0, 1, 0, 0.5))

    # Draw baseline grid over content instead of below.
    myTemplate.baselineGrid(rootStyle)

    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rootStyle, pages=2, template=myTemplate) 
    page1 = doc[1] # Get the first page.
    
    doc.newStyle(name='h1', fontSize=32, fill=(1, 0, 0), leading=40, postfix='\n')
    doc.newStyle(name='h2', fontSize=24, fill=(0, 0.5, 1), leading=30, postfix='\n')
    doc.newStyle(name='h3', fontSize=24, fill=(1, 0, 1), leading=30, postfix='\n')

    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(doc, g) # Create a new TypeSetter, for this document on the empty galley.
    t.typesetFile(MD_PATH) # Typeset the galley from the text in the MD_PATH file.

    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, page1, flowId)

    # Answer the created document object.
    return doc
    
d = makeThesis()
d.export(EXPORT_PATH) 
