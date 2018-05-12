# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     newspaper.py
#
from pagebot.publications.publication import Publication
from pagebot.constants import Broadsheet, CENTER
from pagebot.elements import newRect, newTextBox, newPlacer
from pagebot.elements.pbpage import Template
from pagebot.conditions import *

class Newspaper(Publication):
    """Create a default newspaper, with layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)

    >>> w, h = Broadsheet
    >>> np = Newspaper(w=w, h=h, title="The Newspaper", originTop=False, autoPages=4, template='MainPage')
    >>> view = np.view
    >>> view.padding = 50
    >>> view.showPageCropMarks = True
    >>> view.showPageRegistrationMarks = True
    >>> view.showPagePadding = True
    >>> view.showPageFrame = True
    >>> view.showPageNameInfo = True
    >>> view.showGrid = True
    >>> view.showGridColumns = True
    >>> #view.showBaselineGrid = True
    >>> templateFront = np.getTemplate('Front')
    >>> templateMainPage = np.getTemplate('MainPage')
    >>> np[1].applyTemplate(templateFront)
    >>> np[2].applyTemplate(templateMainPage)
    >>> np[3].applyTemplate(templateMainPage)
    >>> np[4].applyTemplate(templateMainPage)
    >>> np.export('_export/Newspaper.pdf')
    """
    COLUMNS = 8
    GUTTER = 12
    PADDING = 48

    def initialize(self, padding=None, gutter=None, columns=None, **kwargs):
        u"""Initialize the generic book templates. """

        # TODO: Solve for left/right templates.
        if padding is None:
            padding = self.PADDING
        if gutter is None:
            gutter = self.GUTTER
        if columns is None:
            columns = self.COLUMNS

        w, h = self.w, self.h
        cw = (w - 2*padding - gutter*(columns-1))/columns

        # grid-template-columns, grid-template-rows, grid-auto-rows, grid-column-gap, grid-row-gap,
        gridX = []
        for n in range(columns):
            gridX.append([cw, gutter])
        gridX[-1][-1] = 0
        gridY = [(None, 0)] # Default is full height of columns

        t = Template(w=w, h=h, name='Front', padding=padding, gridX=gridX, gridY=gridY)  
        bs = self.view.newString('Newspaper', style=dict(font='Verdana', fontSize=150, textFill=(1, 0, 0)))        
        tb = newTextBox(bs, parent=t, conditions=[Fit2Width(), Top2Top()], fill=0.7, h=200)

        score = t.solve()
        for n in range(columns):
            newRect(parent=t, w=cw, h=100, ml=gutter, conditions=[Bottom2Bottom(), Float2Right()])
            #, Float2Right(), Float2Top(), Fit2Bottom()], fill=0.7)
        self.addTemplate(t.name, t)
        t.solve(score)

        t = Template(w=w, h=h, name='MainPage', padding=padding, gridX=gridX, gridY=gridY)
        for n in range(columns):
            newRect(parent=t, w=cw, ml=gutter, conditions=[Top2Top(), Fit2Height(), Float2Right()], fill=0.7)
        self.addTemplate(t.name, t)
        t.solve(score)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

