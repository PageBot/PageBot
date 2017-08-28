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
#     website.py
#
from pagebot.conditions import *
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.toolbox.units import fr, px


class Website(Publication):
    """Create a default website home page.
    Layout and content options defined by external parameters.
    Subclassed from Document with the following optional attributes:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, 
    w=None, h=None, exportPaths=None, **kwargs)"""

    def initialize(self, **kwargs):
        u"""Initialize the generic website templates. """
        
        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, no horizontal division.

        t = Template(w=w, h=h, name='Home', padding=padding, gridX=gridX, gridY=gridY) 
        newRect(parent=t, conditions=[Fit2Sides()], name='Home')
        self.addTemplate(t.name, t)
        newTextBox('AAAA', parent=t)
        newTextBox('VVVV', parent=t)

        