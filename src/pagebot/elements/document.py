# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     document.py
#
import copy

from drawBot import newPage, saveImage, installedFonts, installFont

from pagebot.elements.page import Page
from pagebot.elements.element import Element
from pagebot.style import makeStyle, getRootStyle
from pagebot.toolbox.transformer import pointOffset, obj2StyleId, point3D

class Document(Element):
    u"""A Document is just another kind of container."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.

    def __init__(self, rootStyle=None, styles=None, title=None, name=None, fileName=None, autoPages=1, pageTemplate=None, displayMode=None, **kwargs):
        u"""Contains a set of Page elements and other elements used for display in thumbnail mode. Allows to compose the pages
        without the need to send them directly to the output for "asynchronic" page filling."""
        Element.__init__(self, **kwargs)
        if rootStyle is None:
            rootStyle = getRootStyle()
        self.rootStyle = makeStyle(rootStyle, **kwargs) # self.w and self.h are available as properties
        self.initializeStyles(rootStyle, styles)

        self.title = title or 'Untitled'
        self.name = name or self.title
        self.fileName = fileName or (self.title + '.pdf')
        self.displayMode = displayMode

        # Used as default document master template if undefined in pages.
        self.pageTemplate = pageTemplate 

        # Document (w, h) size is default from page, but will modified by the type of display mode. 
        if autoPages:
            self.makePages(pageCnt=autoPages, **kwargs)
        # Storage lib for collected content while typesetting and composing, referring to the pages
        # they where placed on during composition.
        self._lib = {}

    def _get_lib(self):
        u"""Answer the global storage dictionary, used by TypeSetter and others to keep track of footnotes,
        table of content, etc. Some common entries are predefined. """
        return self._lib 
    lib = property(_get_lib)

    # Document[12] answers a list of pages where page.y == 12
    # This behaviour is different from regular elements, who want the page.eId as key.
    def __getitem__(self, pageNumber):
        u"""Answer the pages with pageNumber equal to page.y. """
        return self.getPageMatrix()[pageNumber]

    def __setitem__(self, key, value):
        raise KeyError('Set page.y instead.')

    def initializeStyles(self, rootStyle, styles):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = {}
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, rootStyle)
        name = 'document'
        if not name in self.styles: # Empty dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))
        name = 'page'
        if not name in self.styles: # Empty dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))

    def _get_ancestors(self):
        return [] # Behave as Element, alsways root, top of tree.
    ancestors = property(_get_ancestors)

    def getMaxPageSizes(self, pageSelection=None):
        u"""Answer the (w, h, d) size of all pages together. If the optional pageSelection is defined (set of y-values),
        then only evaluate the selected pages."""
        w = h = d = 0
        for e in self.elements:
            if pageSelection is not None and not e.y in pageSelection:
                continue
            w = max(w, e.w)
            h = max(h, e.h)
            d = max(d, e.d)
        return w, h, d

    # Answer the cascaded style value, looking up the chain of ancestors, until style value is defined.

    def css(self, name, default=None, styleId=None):
        u"""If optional sId is None or style cannot found, then use the root style. 
        If the style is found from the (cascading) sId, then use that to return the requested attribute."""
        style = self.findStyle(styleId)
        if style is None:
            style = self.rootStyle
        return style.get(name, default)

    def findStyle(self, styleId):
        u"""Answer the style that fits the optional sequence naming of styleId.
        Answer None if no style can be found. styleId can have one of these formats:
        ('main h1', 'h1 b')"""
        if styleId is None:
            return None
        styleId = obj2StyleId(styleId)
        while styleId and not ' '.join(styleId) in self.styles:
            styleId = styleId[1:]
        if styleId:
            return self.styles[styleId]
        return None

    def getNamedStyle(self, styleName):
        u"""In case we are looking for a named style (e.g. used by the Typesetter to build a stack
        of cascading tag style, then query the ancestors for the named style. Default behavior
        of all elements is that they pass the request on to the root, which is nornally the document."""
        return self.getStyle(styleName)

    def getStyle(self, name):
        u"""Answer the names style. If that does not exist, answer the default root style."""
        self.styles.get(name, self.getRootStyle())
    
    def getRootStyle(self):
        u"""Answer the default root style, used by the composer as default for all other stacked styles."""
        return self.rootStyle

    def addStyle(self, name, style):
        u"""Add the style to the self.styles dictionary."""
        assert not name in self.styles # Make sure that styles don't get overwritten. Remove them first.
        self.styles[name] = style
        # Force the name of the style to synchronize with the requested key.
        style['name'] = name
      
    def replaceStyle(self, name, style):
        u"""Set the style by name. Overwrite the style with that name if it already exists."""
        self.styles[name] = style
        # Force the name of the style to synchronize with the requested key.
        style['name'] = name
        return style # Answer the style for convenience of tha caller, e.g. when called by self.newStyle(args,...)

    def newStyle(self, **kwargs):
        u"""Create a new style with the supplied arguments as attributes. Force the style in self.styles,
        even if already exists. Forst the name of the style to be the same as the style key.
        Answer the new style."""
        return self.replaceStyle(kwargs['name'], dict(**kwargs))
         
    def getInstalledFonts(self):
        u"""Answer the list of font names, currently installed in the application."""
        return installedFonts()

    def installFont(self, path):
        u"""Install a font with a given path and the postscript font name will be returned. The postscript
        font name can be used to set the font as the active font. Fonts are installed only for the current
        process. Fonts will not be accessible outside the scope of drawBot.
        All installed fonts will automatically be uninstalled when the script is done."""
        return installFont(path)

    def getPage(self, y, x=0, index=0):
        u"""Answer the page at index, for equal y and x. Raise index errors if it does not exist.
        Note that this calla=s self.getPageMatrix(), which is an expensive method."""
        return self.getXPages(y, x)[index]

    def getXPages(self, y, x=0):
        u"""Answer all pages that share the same page.y page number. Raise KeyError if non exist.
        Note that this calla=s self.getPageMatrix(), which is an expensive method."""
        return self.getYPages(y)[x]

    def getYPages(self, y):
        u"""Answer all pages that share the same page.y page number. Rase KeyError if non exist.
        Note that this calla=s self.getPageMatrix(), which is an expensive method."""
        return self[y]

    def getPageByName(self, name):
        u"""Answer the list of page(s) with this name. Answer None if is does not exist."""
        return self.find(name)
  
    def newPage(self, parent=None, **kwargs):
        u"""Use point (x, y) to define the order of pages and spreads. Ignore any parent here, force to self."""
        page = self.PAGE_CLASS(parent=self, **kwargs)
        self.appendElement(page)
    
    def getPageMatrix(self):
        u"""Answer the dictionary where key is page.y and value a dictionary of lists of page.x pages."""
        pageMatrix = {}
        for page in self.elements:
            if not page.y in pageMatrix:
                pageMatrix[page.y] = {}
            if not page.x in pageMatrix[page.y]:
                pageMatrix[page.y][page.x] = []
            pageMatrix[page.y][page.x].append(page)
        return pageMatrix

    def makePages(self, pageCnt, point=None, **kwargs):
        u"""Make a range of pages. (Mis)using the (x,y) position of page elements, as their sorting order.
        If no "point" is defined as page id, then we'll continue after the maximum value of page.y origin position."""
        if point is None:
            pages = self.getLastPages()
            if pages:
                x, y = 0, pages[0].y
            else:
                x = y = 0
        else:
            x, y, _, = point3D(point) # Ignore z-axis of page location in the document for now.
        for n in range(pageCnt):
            self.newPage(point=(x, y+n), template=self.pageTemplate, **kwargs) # Parent is forced to self.

    def nextPages(self, page, nextPage=1, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page."""
        pageMatrix = self.getPageMatrix()
        pageNumbers = sorted(pageMatrix.keys())
        if page.y == max(pageNumbers):
            y = page.y + nextPage
        elif page.y in pages:
            y = pageNumber[min(pageNumbers.index(page.y) + nextPage, len(pageNumber))]
        return pages[y]

    def getFirstPages(self):
        u"""Answer the list of pages with the lowest sorted page.y. Answer empty list if there are no pages."""
        pageMatrix = self.getPageMatrix()
        if self.pageMatrix:
            return pageMatrix[min(pageMatrix.keys())]
        return []
 
    def getLastPages(self):
        u"""Answer the list of pages with the highest sorted page.y. Answer empty list if there are no pages."""
        pageMatrix = self.getPageMatrix()
        if pageMatrix:
            return pageMatrix[max(pageMatrix.keys())]
        return []
 
    def getSortedPages(self):
        u"""Answer the dynamic list of pages, sorted by y, x and index."""
        sortedPages = []
        for y, yPages in sorted(self.getPageMatrix().items()):
            for x, xPages in sorted(yPages.items()):
                for page in xPages:
                    sortedPages.append(page)
        return sortedPages

    def getStyle(self, name):
        u"""Answer the names style. Answer None if it does not exist."""
        return self.styles.get(name)

    def drawPages(self, pageSelection=None):
        u"""Draw the selected pages. pageSelection is an optional set of y-pageNumbers to draw."""
        w, h, _ = self.getMaxPageSizes(pageSelection)
        paddingX = self.pl + self.pr
        paddingY = self.pt + self.pb
        for page in self.getSortedPages():
            if pageSelection is not None and not page.y in pageSelection:
                continue
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            # Size depends on the size of the larges pages + optional decument padding.
            if paddingX or paddingY:
                w += paddingX
                h += paddingY
            else:
                w = page.w # No padding defined, follow the size of the page.
                h = page.h

            newPage(w, h) #  Make page in DrawBot of self size, actual page may be smaller if showing cropmarks.
            # Let the page draw itself on the current DrawBot view port if self.writer is None.
            # Use the (docW, docH) as offset, in case cropmarks need to be displayed.
            origin = point3D((self.pl, self.pt, self.pzf))
            page.draw(origin) 

    def export(self, fileName, pageSelection=None, multiPage=True):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted. The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct the type of
        drawing and export that needs to be done.
        The multiPage value is passed on to the DrawBot saveImage call.
        document.export(...) is the most common way to export documents. But in special cases, there is not 
        straighforward (or sequential) export of pages, e.g. when generating HTML/CSS. In that case use 
        MyBuilder(document).export(fileName), the builder is responsible to query the document, pages, elements and styles.
        """
        self.drawPages(pageSelection)

        # If rootStyle['frameDuration'] is set and saving as movie or animated gif, 
        # then set the global frame duration.
        frameDuration = self.css('frameDuration')
        if frameDuration is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
            frameDuration(frameDuration)

        # http://www.drawbot.com/content/canvas/saveImage.html
        saveImage(fileName, multipage=multiPage)

