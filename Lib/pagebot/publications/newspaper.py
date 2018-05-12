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
from pagebot.elements import Group, newRect, newTextBox
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.elements.pbpage import Template
from pagebot.conditions import *

class Title(Group):
    pass

class Article(Group):
    pass

class Newspaper(Publication):
    """Create a default newspaper, with layout and content options defined by external parameters.
    Inheriting from Document with the following optional attribures:
    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None, 
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
    exportPaths=None, **kwargs)

    >>> blurb = Blurb()
    >>> name = blurb.getBlurb('news_newspapername')
    >>> w, h = Broadsheet
    >>>
    >>> np = Newspaper(w=w, h=h, title=name, originTop=False, autoPages=4, template='MainPage')
    >>> view = np.view
    >>> view.padding = 50
    >>> view.showPageCropMarks = True
    >>> view.showPageRegistrationMarks = True
    >>> #view.showPagePadding = True
    >>> view.showPageFrame = True
    >>> view.showPageNameInfo = True
    >>> #view.showGrid = True
    >>> #view.showGridColumns = True
    >>> #view.showBaselineGrid = True
    >>> #view.showElementFrame = True
    >>> templateFront = np.getTemplate('Front')
    >>> templateMainPage = np.getTemplate('MainPage')
    >>> np[1].applyTemplate(templateFront)
    >>> np[2].applyTemplate(templateMainPage)
    >>> np[3].applyTemplate(templateMainPage)
    >>> np[4].applyTemplate(templateMainPage)
    >>> result = np.solve()
    >>> np.export('_export/Newspaper.pdf')
    """
    COLUMNS = 7
    GUTTER = 16
    PADDING = 48

    def initialize(self, padding=None, gutter=None, columns=None, **kwargs):
        u"""Initialize the generic book templates. """
        blurb = Blurb()

        # TODO: Solve for left/right templates.
        if padding is None:
            padding = self.PADDING
        if gutter is None:
            gutter = self.GUTTER
        if columns is None:
            columns = self.COLUMNS

        w, h = self.w, self.h
        cw = (w - 2*padding - gutter*(columns-1))/columns
        cwg = cw + gutter
        lineW = 4

        newspaperTitleFont = 'Upgrade Semibold'
        h1Font = 'Upgrade Medium'
        bodyFont = 'Upgrade Book'

        titleStyle = dict(font=newspaperTitleFont, fontSize=140, w=(columns-2)*cw, textFill=0)
        h1Style = dict(font=h1Font, fontSize=90, leading=90, textFill=0)
        h2Style = dict(font=h1Font, fontSize=60, leading=60, textFill=0)
        bodyStyle = dict(font=bodyFont, fontSize=14, hyphenation=True, leading=18, textFill=0,
            firstParagraphIndent=2*gutter, firstLineIndent=gutter)
        h1IntroStyle = dict(font=bodyFont, fontSize=45, hyphenation=True, leading=52, textFill=0)
        h2IntroStyle = dict(font=bodyFont, fontSize=30, hyphenation=True, leading=36, textFill=0)

        titleLine = dict(strokeWidth=1, stroke=0)

        # grid-template-columns, grid-template-rows, grid-auto-rows, grid-column-gap, grid-row-gap,
        gridX = []
        for n in range(columns):
            gridX.append([cw, gutter])
        gridX[-1][-1] = 0
        gridY = [(None, 0)] # Default is full height of columns

        # Template 'Front'
        
        t = Template(w=w, h=h, name='Front', padding=padding, gridX=gridX, gridY=gridY)  
        # Newspaper name with border lines on top and bottom
        bs = self.view.newString(self.title.upper(), style=titleStyle) 
        _, nameHeight = bs.size()      
        title = Title(parent=t, mb=2*gutter, h=nameHeight,
            conditions=[Top2Top(), Fit2Width()])
        tb = newTextBox(bs, parent=title, h=nameHeight, xTextAlign=CENTER, pt=gutter, 
            borderTop=titleLine, borderBottom=titleLine, 
            conditions=[Fit2Width()])

        # Place article 3 columns

        cc = 3 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, h=h/3, mb=gutter,
            conditions=[Left2Left(), Float2Top()])
        
        headLine = blurb.getBlurb('news_headline')
        bs = self.view.newString(headLine, style=h2Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, 
            conditions=[Left2Left(), Float2Top()])
        
        intro = blurb.getBlurb('article_ankeiler')
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])

        cc = 3 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, h=h/4, pt=gutter, borderTop=titleLine, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        headLine = blurb.getBlurb('news_headline')
        bs = self.view.newString(headLine, style=h2Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, 
            conditions=[Left2Left(), Float2Top()])
        
        intro = blurb.getBlurb('article_ankeiler')
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        
        cc = 3 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, pt=gutter, borderTop=titleLine, mb=gutter,
            conditions=[Left2Left(), Float2Top(), Fit2Bottom()])
        
        headLine = blurb.getBlurb('news_headline')
        bs = self.view.newString(headLine, style=h2Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, 
            conditions=[Left2Left(), Float2Top()])
        
        intro = blurb.getBlurb('article_ankeiler')
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        
        # Place article 4 columns with photo
        cc = 4
        article = Article(parent=t, w=cc*cwg, h=h/2, pr=gutter, 
            conditions=[Right2RightSide(), Float2Top(), Float2Left()])

        newRect(h=cc*cw*2/3, mb=gutter, parent=article, 
            fill=0.8, stroke=0, strokeWidth=0.5, 
            conditions=[Left2Left(), Top2Top(), Fit2Width()])
        
        headLine = blurb.getBlurb('news_headline', cnt=12)
        bs = self.view.newString(headLine, style=h1Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, 
            conditions=[Left2Left(), Float2Top(), Fit2Width()])
        
        intro = blurb.getBlurb('article_ankeiler', cnt=20)
        bs = self.view.newString(intro, style=h1IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter,
            conditions=[Left2Left(), Float2Top(), Fit2Width()])

        """
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg, h=10,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        """
        cc = 2 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, borderTop=titleLine, mb=gutter, 
            conditions=[Right2Right(), Float2Top(), Float2Left(), Fit2Bottom()])
        
        headLine = blurb.getBlurb('news_headline')
        bs = self.view.newString(headLine, style=h2Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, pt=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        intro = blurb.getBlurb('article_ankeiler')
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        

        cc = 2 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, borderTop=titleLine, mb=gutter,
            conditions=[Right2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        
        headLine = blurb.getBlurb('news_headline')
        bs = self.view.newString(headLine, style=h2Style)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, pt=gutter,
            conditions=[Left2Left(), Float2Top()])
        
        intro = blurb.getBlurb('article_ankeiler')
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter, 
            conditions=[Left2Left(), Float2Top()])
        
        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cwg,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
        


        self.addTemplate(t.name, t)

        # Template 'MainPage'

        t = Template(w=w, h=h, name='MainPage', padding=padding, gridX=gridX, gridY=gridY)
        for n in range(columns):
            if n == 0:
                cc = 3
                headLine = blurb.getBlurb('news_headline')
                bs = self.view.newString(headLine, style=h2Style)
                newTextBox(bs, parent=t, pr=gutter, w=cc*cwg, 
                    conditions=[Left2Left(), Float2Top()])
                intro = blurb.getBlurb('article_ankeiler')
                bs = self.view.newString(intro, style=h2IntroStyle)
                newTextBox(bs, parent=t, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter,
                    conditions=[Left2Left(), Float2Top()])

            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=t, pr=gutter, w=cw+gutter, z=0,
                conditions=[Right2RightSide(), Float2Top(), Fit2Bottom(), Float2Left()])
        self.addTemplate(t.name, t)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

