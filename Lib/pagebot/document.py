# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     document.py
#
from drawBot import newPage, installedFonts, installFont

from pagebot.conditions.score import Score
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.views import View, DefaultView, SingleView, ThumbView
from pagebot.style import makeStyle, getRootStyle, TOP, BOTTOM
from pagebot.toolbox.transformer import obj2StyleId

class Document(object):
    u"""A Document is just another kind of container."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    VIEW_CLASS = View

    def __init__(self, rootStyle=None, styles=None, views=None, name=None, class_=None, title=None, 
            autoPages=1, defaultTemplate=None, templates=None, originTop=True, startPage=0, w=None, h=None,
            exportPaths=None, **kwargs):
        u"""Contains a set of Page elements and other elements used for display in thumbnail mode. Allows to compose the pages
        without the need to send them directly to the output for "asynchronic" page filling."""
        if rootStyle is None:
            rootStyle = getRootStyle()
        self.rootStyle = rootStyle
        self.class_ = class_ or self.__class__.__name__ # Optional class name, e.g. to group elements together in HTML/CSS export.
        self.initializeStyles(styles) # Create some default styles, to make sure they are there.
        self.originTop = originTop # Set as property in rootStyle and also change default rootStyle['yAlign'] to right side.
        self.w = w or 1000 # Always needs a value. Take 1000 if None defined.
        self.h = h or 1000

        self.name = name or title or 'Untitled'
        self.title = title or self.name

        self.pages = {} # Key is pageNumber, Value is row list of pages: self.pages[pn][index] = page

        self.initializeTemplates(defaultTemplate, templates)

        # Storage lib for collected content while typesetting and composing, referring to the pages
        # they where placed on during composition.
        self._lib = {}

        # Initialize some basic views.
        self.initializeViews(views)

        # Document (w, h) size is default from page, but will modified by the type of display mode. 
        if autoPages:
            self.makePages(pageCnt=autoPages, template=defaultTemplate, pn=startPage, w=self.w, h=self.h, **kwargs)

        # Call generic initialize method, allowing inheriting publication classes to initialize their stuff.
        # This can be the creation of templates, pages, adding/altering styles and view settings.
        # Default is to do nothing.
        self.initialize()

    def initialize(self):
        u"""Default implementation of publication initialized. Can be redefined by inheriting classed."""
        pass

    def _get_lib(self):
        u"""Answer the global storage dictionary, used by TypeSetter and others to keep track of footnotes,
        table of content, etc. Some common entries are predefined. """
        return self._lib 
    lib = property(_get_lib)

    def __repr__(self):
        return '[Document-%s "%s"]' % (self.__class__.__name__, self.name)

    def _get_doc(self):
        u"""End of the chain of element properties, looking upward in the ancestors tree."""
        return self
    doc = property(_get_doc)

    # Document[12] answers a list of pages where page.y == 12
    # This behaviour is different from regular elements, who want the page.eId as key.
    def __getitem__(self, pnIndex):
        u"""Answer the pages with pageNumber equal to page.y. """
        if isinstance(pnIndex, (list, tuple)):
            pn, index = pnIndex
        else:
            pn, index = pnIndex, 0 # Default is left page on pn row.
        return self.pages[pn][index]
    def __setitem__(self, pn, page):
        if not pn in self.pages:
            self.pages[pn] = []
        self.pages[pn].append(page)
   
    def _get_ancestors(self):
        return []
    ancestors = property(_get_ancestors)
    
    def _get_parent(self):
        return None
    parent = property(_get_parent)

    def getInfo(self):
        u"""Answer a string with most representing info about the document."""
        info = []
        info.append('Document-%s "%s"' % (self.__class__.__name__, self.name))
        info.append('\tPages: %d' % len(self.pages))
        info.append('\tTemplates: %s' % ', '.join(self.templates.keys()))
        info.append('\tStyles: %s' % ', '.join(self.styles.keys()))
        info.append('\tLib: %s' % ', '.join(self._lib.keys()))
        return '\n'.join(info)

    #   T E M P L A T E

    def initializeTemplates(self, defaultTemplate, templates):
        if templates is None:
            templates = {}
        self.templates = templates # Store defined dictionary of templates or empty dict.
        # Used as default document master template if undefined in pages.
        if defaultTemplate is not None:
            if isinstance(defaultTemplate, basestring): # Make reference to existing template by name
                defaultTemplate = self.templates.get(defaultTemplate) # If it exists, otherwise it is None
            if defaultTemplate is None: # Only if we have one, overwriter existing default template if it was there.
                # Make sure there is at least a default template.
                defaultTemplate = Template(w=self.w, h=self.h, name='default', padding=self.css('padding'))
            self.templates['default'] = defaultTemplate
        for template in self.templates.values(): # Hard-reference the parent of all templates to Document self, so theu share the rootStyle.
            template.parent = self

    def getTemplate(self, name=None):
        u"""Answer the named template. If it does not exist, then answer the default template. Answer None of if there is no default."""
        if name in self.templates:
            return self.templates[name]
        return self.defaultTemplate

    def addTemplate(self, name, template):
        u"""Add the template to the self.templates of dictionaries. There is no check, so caller can overwrite existing templates.
        Answer the template as convenience of the caller."""
        template.parent = self
        self.templates[name] = template
        return template

    def _get_defaultTemplate(self):
        return self.templates.get('default')
    defaultTemplate = property(_get_defaultTemplate)

    #   S T Y L E

    def initializeStyles(self, styles):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = {}
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, self.rootStyle)
        name = 'document'
        if not name in self.styles: # Empty dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))
        name = 'page'
        if not name in self.styles: # Empty dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))

    def getMaxPageSizes(self, pageSelection=None):
        u"""Answer the (w, h, d) size of all pages together. If the optional pageSelection is defined (set of y-values),
        then only evaluate the selected pages."""
        w = h = d = 0
        for (y, x), page in self.pages.items():
            if pageSelection is not None and not y in pageSelection:
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
        return self.styles.get(name)
    
    def getRootStyle(self):
        u"""Answer the default root style, used by the Typesetter as default for all other stacked styles."""
        return self.rootStyle

    def add2Style(self, name, addStyle):
        u"""Add (overwrite) the values in the existing style *name* with the values in *addStyle*.
        Raise an error if the *name* style does not exist. Answer the named target style for convenience of the caller."""
        assert name in self.styles
        style = self.styles[name]
        for key, value in addStyle.items():
            style[key] = value
        return style # Answer the style for convenience of the caller.

    def addStyle(self, name, style):
        u"""Add the style to the self.styles dictionary.  Make sure that styles don't get overwritten. Remove them first
        with *self.removeStyle* or use *self.replaceStyle(name, style)* instead."""
        assert not name in self.styles
        self.styles[name] = style
        # Force the name of the style to synchronize with the requested key.
        style['name'] = name
        return style # Answer the style for convenience of the caller.
        
    def removeStyle(self, name):
        u"""Remove the style *name* if it exists. Raise an error if is does not exist."""
        del self.styles[name]

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
    
    #   D E F A U L T  A T T R I B U T E S 

    def _get_orjginTop(self):
        return self.getRootStyle('originTop')
    def _set_originTop(self, flag):
        rs = self.getRootStyle()
        if flag:
            rs['originTop'] = True
            rs['yAlign'] = TOP
        else:
            rs['originTop'] = False
            rs['yAlign'] = BOTTOM
    originTop = property(_get_orjginTop, _set_originTop)

    # CSS property service to children.
    def _get_w(self): # Width
        return self.rootStyle['w'] 
    def _set_w(self, w):
        self.rootStyle['w'] = w # Overwrite element local style from here, parent css becomes inaccessable.
    w = property(_get_w, _set_w)

    def _get_h(self): # Height
        return self.rootStyle['h'] 
    def _set_h(self, h):
        self.rootStyle['h'] = h # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    def _get_d(self): # Depth
        return self.rootStyle['d'] # From self.style, don't inherit.
    def _set_d(self, d):
        self.rootStyle['d'] = d # Overwrite element local style from here, parent css becomes inaccessable.
    d = property(_get_d, _set_d)

    #   F O N T S

    def getInstalledFonts(self):
        u"""Answer the list of font names, currently installed in the application."""
        return installedFonts()

    def installFont(self, path):
        u"""Install a font with a given path and the postscript font name will be returned. The postscript
        font name can be used to set the font as the active font. Fonts are installed only for the current
        process. Fonts will not be accessible outside the scope of drawBot.
        All installed fonts will automatically be uninstalled when the script is done."""
        return installFont(path)

    #   P A G E S

    def appendElement(self, e): 
        u"""Add page to the document. Called when page.parent is set or view.parent is set. 
        If Page, add after last page. If View, add as self.views[view.viewId]"""
        if e.isPage:
            self.appendPage(e)
        elif e.isView:
            e.setParent(self) # Set parent as weakref, without calling self.appendElement again.
            self.views[e.viewId] = e
        else:
            raise ValueError('Cannot append elements other that Page or View to Document; "%s"' % e)

    def appendPage(self, page):
        u"""Append a page to the document. Assert that it is a page element."""
        assert page.isPage    
        page.setParent(self) # Set parent as weakref, without calling self.appendElement again.
        if self.pages.keys():
            pn = max(self.pages.keys())+1
        else:
            pn = 0
        self[pn] = page

    def getPage(self, pnOrName, index=0):
        u"""Answer the page at (pn, index). Otherwise search for a page with this name. Raise index errors if it does not exist."""
        if pnOrName in self.pages:
            if index >= len(self.pages[pnOrName]):
                return None
            return self.pages[pnOrName][index]
        pages = self.findPages(name=pnOrName) # In case searching by name, there is chance that multiple are answered as list.
        if pages:
            return pages[0]
        return None

    def getPages(self, pn):
        u"""Answer all pages that share the same page number. Rase KeyError if non exist."""
        return self.pages[pn]

    def findPages(self, eId=None, name=None, pattern=None, pageSelection=None):
        u"""Various ways to find pages from their attributes."""
        pages = []
        for pn, pnPages in sorted(self.pages.items()):
            if not pageSelection is None and not pn in pageSelection:
                continue
            for page in pnPages: # List of pages with identical pn
                if eId == page.eId:
                    return [page]
                if (name is not None and name == page.name) or \
                       pattern is not None and page.name is not None and pattern in page.name:
                    pages.append(page)
        return pages

    def newPage(self, pn=None, template=None, w=None, h=None, name=None, **kwargs):
        u"""Create a new page with size (self.w, self.h) unless defined otherwise. Add the pages in the row of pn, if defined.
        Otherwise create a new row of pages at pn. If pn is undefined, add a new page row at the end.
        If template is undefined, then use self.pageTemplat to initialize the new page."""
        if isinstance(template, basestring):
            template = self.templates.get(template)
        if template is None:
            template = self.defaultTemplate
        
        if not name and template is not None:
            name = template.name

        page = self.PAGE_CLASS(parent=self, w=None, h=None, name=name, **kwargs)
        page.applyTemplate(template)
        return page # Answer the new page 

    def makePages(self, pageCnt, pn=0, template=None, w=None, h=None, name=None, **kwargs):
        u"""
        If no "point" is defined as page number pn, then we'll continue after the maximum value of page.y origin position.
        If template is undefined, then self.newPage will use self.defaultTemplate to initialize the new pages."""
        for n in range(pageCnt): # First page is n + pn
            self.newPage(pn=n+pn, template=template, name=name, w=w, h=h, **kwargs) # Parent is forced to self.

    def getElementPage():
        u"""Search ancestors for the page element. This call can only happen here if elements don't have a
        Page ancestor. Return None to indicate that there is no Page instance found amongst the ancesters."""
        return None

    def nextPage(self, page, nextPage=1, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page."""
        found = False
        for pn, pnPages in sorted(self.pages.items()):
            for index, page in enumerate(pnPages):
                if found:
                    return page
                if eId == page.eId:
                    found = True
        # Not found, create new one?
        if makeNew:
            return self.newPage()
        return None

    def getPageNumber(self, page):
        u"""Answer a string with the page number pn, if the page can be found. If the page has index > 0:
        then answer page format "pn-index". pn and index are incremented by 1.
        TODO: Make a reversed table if this squential search shows to be slow in the future with large docs.
        """
        for pn, pnPages in sorted(self.pages.items()):
            for index, pg in enumerate(pnPages):
                if pg is page:
                    if index:
                        return '%d-%d' % (pn+1, index+1)
                    return '%d' % (pn+1)
        return ''

    def getFirstPage(self):
        u"""Answer the list of pages with the lowest sorted page.y. Answer empty list if there are no pages."""
        for pn, pnPages in sorted(self.pages.items()):
            for index, page in enumerate(pnPages):
                return page
        return None

    def getLastPage(self):
        u"""Answer last page with the highest sorted page.y. Answer empty list if there are no pages."""
        pn = sorted(self.pages.keys())[-1]
        return self.pages[pn][-1]

    def getSortedPages(self, pageSelection=None):
        u"""Answer the dynamic list of pages, sorted by y, x and index."""
        pages = [] # List of (pn, pnPages) tuples of pages with the same page number.
        for pn, pnPages in sorted(self.pages.items()):
            if pageSelection is not None and not pn in pageSelection:
                continue
            pages.append((pn, pnPages))
        return pages

    def getMaxPageSizes(self, pageSelection=None):
        u"""Answer the max (w, h, d) for all pages. If pageSeleciton is defined as list of pageNumbers,
        then filter on that."""
        w = 0
        h = 0
        d = 0
        for pn, pnPages in self.pages.items():
            if not pageSelection is None and not pn in pageSelection:
                continue
            for page in pnPages:
                w = max(page.w, w)
                h = max(page.h, h)
                d = max(page.d, d)
            return w, h, d

    def solve(self, score=None):
        u"""Evaluate the content of all pages to return the total sum of conditions solving."""
        score = Score()
        for pn, pnPages in sorted(self.pages.items()):
            for page in pnPages: # List of pages with identical pn, step through the pages.
                page.solve(score)
        return score

    #   V I E W S

    def initializeViews(self, views):
        self.views = {} # Key is name or eId of View instance. 
        if views is not None:
            for view in views:
                assert not view.name in self.views
                self.appendElement(view)
        # Define some default views if not already  there.
        for viewClass in (DefaultView, ThumbView):
            if not viewClass.viewId in self.views: # Only if not already defined, to make sure it is there.
                # Create views, default with the same size as document.
                self.appendElement(viewClass(parent=self, w=self.w, h=self.h))

    def getView(self, viewId=None):
        u"""Answer the viewer instance with viewId. Answer DefaultView() if it does not exist."""
        if not viewId in self.views:
            viewId = DefaultView.viewId # We know for sure that this one is in self.views
        return self.views.get(viewId)

    #   D R A W I N G

    def drawPages(self, viewId=None, pageSelection=None):
        u"""Draw the selected pages, using DrawBot as canvas. 
        PageSelection is an optional list of y-pageNumbers to draw."""
        view = self.getView(viewId) # view.parent is self
        view.drawPages(pageSelection)

    def export(self, fileName=None, pageSelection=None, viewId=None, multiPage=True):
        u"""Let the view do the work."""
        view = self.getView(viewId) # view.parent is self
        view.export(fileName=fileName, pageSelection=pageSelection, multiPage=multiPage)



