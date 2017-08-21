# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     book.py
#
from pagebot.conditions import *
from pagebot.publications.publication import Publication
# Page and Template instances are holding all elements of a page together.
from pagebot.elements import *

 
class Book(Publication):
    """Create a default book, with cover, title pages, table of content,
    chapters and index. Layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, 
    w=None, h=None, exportPaths=None, **kwargs)"""

    def initialize(self, coverBackgroundFill=None, **kwargs):
        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        gridY = [(None, 0)] # Default is full height of columns, not horizontal division.

        if coverBackgroundFill is None:
            coverBackgroundFill = (0.3, 0.3, 0.3)

        t = Template(w=w, h=h, name='Cover', padding=padding, gridY=gridY) 
        newRect(parent=t, conditions=[Fit2Sides()], fill=coverBackgroundFill)
        self.addTemplate(t.name, t)

        t = Template(w=w, h=h, name='Title Page', padding=padding, gridY=gridY)
        newTextBox('AAAA', parent=t, conditions=[Right2Right(), Top2Top(), Fit2Height()], w=400, fill=(1, 0, 0))
        self.addTemplate(t.name, t)
        
        t = Template(w=w, h=h, name='Table Of Content', padding=padding, gridY=gridY)
        newTextBox('AAAA', parent=t, conditions=[Right2Right(), Top2Top(), Fit2Height()], w=400, fill=(1, 1, 0))
        self.addTemplate(t.name, t)
        
        t = Template(w=w, h=h, name='Main Page', padding=padding, gridY=gridY)
        self.addTemplate('default', t)
        
        t = Template(w=w, h=h, name='Register Page', padding=padding, gridY=gridY)
        self.addTemplate(t.name, t)
        
