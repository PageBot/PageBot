# -*- coding: UTF-8 -*-
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
#     newspaper.py
#
from pagebot.publications.publication import Publication
from pagebot.publications.newspaper.title import Title
from pagebot.publications.newspaper.article import Article
from pagebot.constants import *
from pagebot.elements import newRect, newTextBox
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.elements.pbpage import Template
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.family import getFontPaths
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color


class Newspaper(Publication):
    """Create a default newspaper, with layout and content options defined by
    external parameters. Inheriting from Document with the following optional
    attribures:

    rootStyle=None, styles=None, views=None, name=None, cssClass=None, title=None,
    autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None,
    exportPaths=None, **kwargs)

    >>> from pagebot.constants import Broadsheet, GRID_SQR, BASE_LINE
    >>> blurb = Blurb()
    >>> name = blurb.getBlurb('news_newspapername')
    >>> w, h = Broadsheet
    >>>
    >>> np = Newspaper(w=w, h=h, title=name, originTop=False, autoPages=1, template='MainPage')
    >>> view = np.view
    >>> view.padding = 50
    >>> view.showCropMarks = True
    >>> view.showRegistrationMarks = True
    >>> #view.showPadding = True
    >>> #view.showFrame = True
    >>> view.showNameInfo = True
    >>> #view.showGrid = GRID_SQR
    >>> #view.showBaselineGrid = [BASE_LINE]
    >>> #view.showFrame = True
    >>> templateFront = np.getTemplate('Front')
    >>> templateMainPage = np.getTemplate('MainPage')
    >>> np[1].applyTemplate(templateFront)
    >>> #np[2].applyTemplate(templateMainPage)
    >>> #np[3].applyTemplate(templateMainPage)
    >>> #np[4].applyTemplate(templateMainPage)
    >>> result = np.solve() # Drill down to all elements positions themselves.
    >>> np.export('_export/Newspaper.pdf')
    """
    COLUMNS = 7
    GUTTER = 18
    PADDING = 48

    # Default paper sizes that are likely to be used for 
    # newspapers in portrait ratio.
    PAGE_SIZES = {
        'A2': A2,
        'A3': A3,
        'A4': A4,
        'A5': A5,
        'B4': B4,
        'B5': B5,
        'HalfLetter': HalfLetter,
        'Letter': Letter,
        'Legal': Legal,
        'JuniorLegal': JuniorLegal,
        'Tabloid': Tabloid,
        'Ledger': Ledger,
        'Statement': Statement,
        'Executive': Executive,
        'Folio': Folio,
        'Quarto': Quarto,
        'Size10x14': Size10x14,
        'A4Letter': A4Letter,
        'A4Oversized': A4Oversized,
        'A3Oversized': A3Oversized,
    }
    DEFAULT_PAGE_SIZE_NAME = 'A3'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    def getHeadline(self, s, style, cnt=None, w=None):
        u"""Answers a styled BabelString instance, with some checking on the
        content. Create a blurb headline if s is None. Make sure it does not
        end with '.,:;-'.  If w is not None, then force the fontsize of the
        headline to fit the width."""
        if s is None:
            s = Blurb().getBlurb('news_headline', cnt=cnt)
            while s and s[-1] in '.,:;-':
                s = s[:-1]
        formattedHeadline = self.view.newString(s, style=style, w=w)
        return formattedHeadline

    def getAnkeiler(self, cnt=None):
        u"""Answers a blurb ankeiler. Make sure it does end with '.'"""
        ankeiler = Blurb().getBlurb('article_ankeiler', cnt=cnt)
        while ankeiler and ankeiler[-1] in ',:;-':
            ankeiler = ankeiler[:-1]
        if not ankeiler.endswith('.'):
            ankeiler += '.'
        return ankeiler

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

        fillColor1 = color(0.2, 0.2, 0.9, 0.6) # Temp fill of markers.
        fillColor2 = color(0.9, 0.2, 0.9, 0.6) # Temp fill of markers.
        fillColor3 = color(0.9, 0.2, 0.3, 0.6) # Temp fill of markers.
        fillColor4 = color(0.9, 0.9, 0.3, 0.6) # Temp fill of markers.
        #fillColor1 = fillColor2 = fillColor3 = fillColor4 = None

        w, h = self.w, self.h
        cw = (w - 2*padding - gutter*(columns-1))/columns
        cwg = cw + gutter
        lineW = 4

        # Max amount of words return by the blurb generator.
        maxHeadline = 6
        maxHeadlineShort = 4
        maxAnkeiler = 30

        fontPaths = getFontPaths()
        #for fontName, path in getFontPaths().items():
        #    if 'Escrow' in fontName:
        #        print(fontName, path)
        #newspaperTitleFont = fontPaths['Escrow-Black']
        #newspaperTitleFont = 'Proforma Book'
        newspaperTitleFont = 'Upgrade Semibold'
        h1Font = 'Upgrade Medium'
        bodyFont = 'Upgrade Book'

        titleStyle = dict(font=newspaperTitleFont, fontSize=pt(140), w=(columns-2)*cw, textFill=color(0))
        h1Style = dict(font=h1Font, fontSize=pt(90), leading=pt(90), textFill=color(0))
        h2Style = dict(font=h1Font, fontSize=pt(60), leading=pt(60), textFill=color(0))
        bodyStyle = dict(font=bodyFont, fontSize=pt(14), hyphenation=True,
                leading=pt(18), textFill=color(0), firstTagIndent=2*gutter, firstLineIndent=pt(gutter))
        h1IntroStyle = dict(font=bodyFont, fontSize=pt(45), hyphenation=True, leading=pt(52), textFill=color(0))
        h2IntroStyle = dict(font=bodyFont, fontSize=pt(30), hyphenation=True, leading=pt(36), textFill=color(0))

        titleLine = dict(strokeWidth=pt(1), stroke=color(0))

        # grid-template-columns, grid-template-rows, grid-auto-rows, grid-column-gap, grid-row-gap,
        gridX = []
        for n in range(columns):
            gridX.append([cw, gutter])
        gridX[-1][-1] = 0
        gridY = [(None, 0)] # Default is full height of columns

        # Template 'Front'

        t = Template(w=w, h=h, name='Front', padding=padding, gridX=gridX, gridY=gridY)

        # Newspaper name with border lines on top and bottom
        #self.title = 'NORTHAMPTON GLOBE'
        bs = self.view.newString(self.title.upper(), style=titleStyle)
        _, nameHeight = bs.size

        title = Title(parent=t, mb=2*gutter, h=nameHeight,
            conditions=[Top2Top(), Fit2Width()])
        tb = newTextBox(bs, parent=title, h=nameHeight, xTextAlign=CENTER, pt=gutter,
            borderTop=titleLine, borderBottom=titleLine,
            conditions=[Fit2Width()])

        # Place article 3 columns

        cc = 3 # Column width of this article.
        article = Article(parent=t, h=h/3, w=cc*cwg-gutter, mr=gutter, mb=gutter,
            fill=fillColor1, conditions=[Left2Left(), Float2Top()])

        s = None #'Happy birthday, Jill'
        headLine = self.getHeadline(s, h2Style, cnt=maxHeadline, w=cc*cwg-gutter)
        newTextBox(headLine, parent=article, w=cc*cwg-gutter,
            fill=fillColor2, conditions=[Left2Left(), Float2Top()])

        intro = self.getAnkeiler(cnt=maxAnkeiler)
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, w=cc*cwg-gutter, mt=gutter, mb=gutter,
            fill=fillColor3,
            conditions=[Left2Left(), Float2Top()])

        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, w=cw, mr=gutter, h=10,
                fill=fillColor4,
                conditions=[Right2Right(), Float2Top(), Float2Left(), Fit2Bottom()])


        cc = 3 # Column width of this article.
        article = Article(parent=t, h=h/4, w=cc*cwg-gutter, mr=gutter, mb=gutter, pt=gutter,
            borderTop=titleLine,
            conditions=[Left2Left(), Float2Top()])

        s = None #'Explore Northampton in spring'
        headLine = self.getHeadline(s, h2Style, cnt=maxHeadline, w=cc*cwg-2*gutter)
        newTextBox(headLine, parent=article, pr=gutter, w=cc*cwg,
            conditions=[Left2Left(), Float2Top()])

        intro = blurb.getBlurb('article_ankeiler', cnt=maxAnkeiler)
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg, mt=gutter, mb=gutter,
            conditions=[Left2Left(), Float2Top()])

        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, w=cw, mr=gutter,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])

        cc = 3 # Column width of this article.
        article = Article(parent=t, h=h/4, w=cc*cwg-gutter, mr=gutter, mb=gutter, pt=gutter,
            borderTop=titleLine,
            borderBottom=titleLine,
            conditions=[Left2Left(), Float2Top(), Fit2Bottom()])

        s = None #'Mothersday for Sara & Jill'
        headLine = self.getHeadline(s, h2Style, cnt=maxHeadline, w=cc*cwg-2*gutter)
        newTextBox(headLine, parent=article, pr=gutter, w=cc*cwg,
            conditions=[Left2Left(), Float2Top()])

        intro = self.getAnkeiler(cnt=maxAnkeiler)
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, w=cc*cwg, mt=gutter, mb=gutter,
            conditions=[Left2Left(), Float2Top()])

        for n in range(cc):
            dummyArticle = blurb.getBlurb('article', newLines=True)
            bs = self.view.newString(dummyArticle, style=bodyStyle)
            newTextBox(bs, parent=article, pr=gutter, w=cw, mr=gutter,
                conditions=[Left2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])

        # Place article 4 columns with photo
        cc = 4
        article = Article(parent=t, w=cc*cwg, h=h/2, pr=gutter,
            conditions=[Right2RightSide(), Float2Top(), Float2Left()])

        newRect(h=cc*cw*2/3, mb=gutter, parent=article,
            fill=color(0.8), stroke=color(0), strokeWidth=pt(0.5),
            conditions=[Left2Left(), Top2Top(), Fit2Width()])

        s = None #'Petr & Claudia visiting soon'
        headLine = self.getHeadline(s, h1Style, cnt=5, w=cc*cwg-2*gutter)
        newTextBox(headLine, parent=article, pr=gutter, w=cc*cwg, pb=gutter,
            conditions=[Left2Left(), Float2Top(), Fit2Width()])

        for n in range(cc):
            if n == 3:
                newRect(mb=gutter, parent=article, w=cw,
                    fill=color(0.8), stroke=color(0), strokeWidth=pt(0.5),
                    conditions=[Right2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])
            else:
                dummyArticle = blurb.getBlurb('article', newLines=True)
                bs = self.view.newString(dummyArticle, style=bodyStyle)
                newTextBox(bs, parent=article, pr=gutter, w=cw, mr=gutter, h=10,
                    conditions=[Right2Right(), Float2Top(), Float2Left(), Fit2Bottom()])

        cc = 2 # Column width of this article.
        article = Article(parent=t, w=cc*cwg, borderTop=titleLine, mb=gutter,
            borderBottom=titleLine,
            conditions=[Right2Right(), Float2Top(), Float2Left(), Fit2Bottom()])

        s = None #'AirB&B stock up 450%'
        headLine = self.getHeadline(s, h2Style, cnt=maxHeadlineShort, w=cc*cwg-gutter)
        newTextBox(headLine, parent=article, pr=gutter, w=cc*cwg, pt=gutter,
            conditions=[Left2Left(), Float2Top()])

        intro = self.getAnkeiler(cnt=maxAnkeiler)
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
            borderBottom=titleLine,
            conditions=[Right2RightSide(), Float2Top(), Float2Left(), Fit2Bottom()])

        s = None #u'Tay & Lan’s best moms'
        headLine = self.getHeadline(s, h2Style, cnt=maxHeadlineShort, w=cc*cwg-gutter)
        newTextBox(headLine, parent=article, pr=gutter, w=cc*cwg, pt=gutter,
            conditions=[Left2Left(), Float2Top()])

        intro = self.getAnkeiler(cnt=maxAnkeiler)
        bs = self.view.newString(intro, style=h2IntroStyle)
        newTextBox(bs, parent=article, pr=gutter, w=cc*cwg-gutter,
            mr=gutter, mt=gutter, mb=gutter,
            conditions=[Left2Left(), Float2Top()])

        newRect(mb=gutter, parent=article, h=200,
            fill=color(0.8), stroke=color(0), strokeWidth=pt(0.5),
            conditions=[Left2Left(), Float2Top(), Fit2Width()])

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
                headLine = self.getHeadline(None, h2Style, cnt=maxHeadline)
                newTextBox(headLine, parent=t, pr=gutter, w=cc*cwg,
                    conditions=[Left2Left(), Float2Top()])
                intro = self.getAnkeiler(cnt=maxAnkeiler)
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

