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
rootStyle['fontSize'] = 11

def makeThesis():
    flowId = 'myFlowName'
    myTemplate = Template(rootStyle)
    myTemplate.grid(rootStyle)
    myTemplate.baselineGrid(rootStyle)
    
    # Empty image element, cx, cy, cw, ch
    myTemplate.cContainer(0, 0, 3, 3, rootStyle, fill=(0, 0, 0, 0.5)) 

    myTemplate.cTextBox('', 3, 0, 3, 7, rootStyle, flowId, nextBox=flowId, nextPage=1, fill=BOX_COLOR)
    myTemplate.rect(x=200, y=200, w=300, h=400, fill=(1,0,0,0.5))
    myTemplate.cRect(1, 1, 2, 3, style=rootStyle, fill=(0, 1, 0, 0.5))

    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template2
    doc = Document(rootStyle, pages=1, template=myTemplate) 
    page1 = doc[1]

    doc.newStyle(name='h1', fontSize=32, font='Georgia', 
        fill=(1, 0, 0), 
        leading=40, postfix='\n')
    doc.newStyle(name='h2', fontSize=24, font='Georgia', 
        fill=(0, 0.5, 1), 
        leading=30, postfix='\n')

    
    # Create main Galley for this page, for pasting the sequence of elements.    
    g = Galley() 
    t = Typesetter(doc, g)
    t.typesetFile(MD_PATH)

    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, page1, flowId)

    return doc
    
d = makeThesis()
d.export(EXPORT_PATH) 
