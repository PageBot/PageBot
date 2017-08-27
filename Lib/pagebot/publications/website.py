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
# Page and Template instances are holding all elements of a page together.
from pagebot.elements import *
from pagebot.toolbox.units import fr, px

 
class Website(Publication):
    """Create a default book, with cover, title pages, table of content,
    chapters and index. Layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, 
    w=None, h=None, exportPaths=None, **kwargs)"""

    def initialize(self, **kwargs):
        u"""Initialize the generic book templates. """

        # TODO: Solve for left/right templates.
        
        padding = self.css('pt'), self.css('pr'), self.css('pb'), self.css('pl')
        w, h = self.w, self.h
        self.gw = self.gh = px(8)
        gridX = (fr(1), fr(1))
        gridY = [None] # Default is full height of columns, not horizontal division.

        t = Template(w=w, h=h, name='Home', padding=padding, gridX=gridX, gridY=gridY) 
        newRect(parent=t, conditions=[Fit2Sides()], name='Home')
        self.addTemplate(t.name, t)
        score = t.solve()
        
        if score.fails:
            print 'Score', score
            for failed in score.fails:
                print '\t', failed