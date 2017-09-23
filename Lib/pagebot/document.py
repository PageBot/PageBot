# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------

#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     document.py
#
import copy

from pagebot.stylelib import styleLib # Library with named, predefined style dicts.
from pagebot.conditions.score import Score
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.views import viewClasses, defaultViewClass
from pagebot.style import makeStyle, getRootStyle, TOP, BOTTOM
from pagebot.toolbox.transformer import obj2StyleId
from pagebot.contexts.builders import BuildInfo # Container with Builder flags and data/parametets

class Document(object):
    u"""A Document is just another kind of container."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.

    DEFAULT_VIEWID = defaultViewClass.viewId

    def __init__(self, rootStyle=None, styles=None, viewId=None, name=None, class_=None, title=None, 
            autoPages=1, template=None, templates=None, originTop=True, startPage=0, w=None, h=None, 
            padding=None, info=None, 
            exportPaths=None, **kwargs):
        u"""Contains a set of Page elements and other elements used for display in thumbnail mode. Allows to compose the pages
        without the need to send them directly to the output for "asynchronic" page filling."""
        self.rootStyle = rs = self.makeRootStyle(rootStyle, **kwargs)
        self.class_ = class_ or self.__class__.__name__ # Optional class name, e.g. to group elements together in HTML/CSS export.
        self.initializeStyles(styles) # Create some default styles, to make sure they are there.
        self.originTop = originTop # Set as property in rootStyle and also change default rootStyle['yAlign'] to right side.
        self.w = w or 1000 # Always needs a value. Take 1000 if None defined.
        self.h = h or 1000
        if padding is not None:
            self.padding = padding

        self.name = name or title or 'Untitled'
        self.title = title or self.name

        self.pages = {} # Key is pageNumber, Value is row list of pages: self.pages[pn][index] = page

        # Initialize the current view of this document. All conditional checking and building
        # is done through this view. The defaultViewClass is set either to DrawBotView or FlatView,
        # depending on the type of platform we are running on.
        # TODO: If the view is (re)set in a later stage, some template and other initialization
        # needs to be done again, or else calculated text sizes may be wrong.
        self.setView(viewId or defaultViewClass.viewId)

        # Template is name or instance default template.
        self.initializeTemplates(templates, template) 

        # Storage lib for collected content while typesetting and composing, referring to the pages
        # they where placed on during composition.
        self._lib = {}

        # Instance to hold details flags and data to guide the self.view.b builder of this document.
        self.info = info or BuildInfo()

        # Document (w, h) size is default from page, but will modified by the type of display mode. 
        if autoPages:
            self.makePages(pageCnt=autoPages, pn=startPage, w=self.w, h=self.h, **kwargs)

        # Call generic initialize method, allowing inheriting publication classes to initialize their stuff.
        # This can be the creation of templates, pages, adding/altering styles and view settings.
        # Default is to do nothing.
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        u"""Default implementation of publication initialized. Can be redefined by inheriting classed.
        All **kwargs are available to allow access for inheriting Publication documents."""
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

    def getView(self):
        u"""For compatibility with old code."""
        return self.view

    def getInfo(self):
        u"""Answer a string with most representing info about the document."""
        info = []
        info.append('Document-%s "%s"' % (self.__class__.__name__, self.name))
        info.append('\tPages: %d' % len(self.pages))
        info.append('\tTemplates: %s' % ', '.join(sorted(self.templates.keys())))
        info.append('\tStyles: %s' % ', '.join(sorted(self.styles.keys())))
        info.append('\tLib: %s' % ', '.join(self._lib.keys()))
        return '\n'.join(info)

    #   T E M P L A T E

    def initializeTemplates(self, templates, defaultTemplate):
        u"""Initialize the document templates.""" 
        self.templates = {} # Store defined dictionary of templates or empty dict.
        if templates is not None:
            for name, template in templates.items():
                self.addTemplate(name, template)
        # Used as default document master template if undefined in pages.
        if isinstance(defaultTemplate, basestring): # Make reference to existing template by name
            defaultTemplate = self.templates.get(defaultTemplate) # If it exists, otherwise it is None
        if defaultTemplate is None: # Only if we have one, overwrite existing default template if it was there.
            # Make sure there is at least a default template.
            defaultTemplate = Template(w=self.w, h=self.h, name='default', padding=self.css('padding'))
        self.defaultTemplate = defaultTemplate

    def getTemplate(self, name=None):
        u"""Answer the named template. If it does not exist, then answer the default template. Answer None of if there is no default."""
        return self.templates.get(name, self.defaultTemplate)

    def addTemplate(self, name, template):
        u"""Add the template to the self.templates of dictionaries. There is no check, so caller can overwrite existing templates.
        Answer the template as convenience of the caller."""
        template.parent = self
        self.templates[name] = template
        return template

    def _get_defaultTemplate(self):
        return self.templates.get('default')
    def _set_defaultTemplate(self, template):
        self.addTemplate('default', template)
    defaultTemplate = property(_get_defaultTemplate, _set_defaultTemplate)

    #   S T Y L E

    def initializeStyles(self, styles):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = copy.copy(styleLib['default'])
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, self.rootStyle)
        name = 'document'
        if not name in self.styles: # Default dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))
        name = 'page'
        if not name in self.styles: # Default dict styles as placeholder, if nothing is defined.
            self.addStyle(name, dict(name=name))

    def makeRootStyle(self, rootStyle, **kwargs):
        u"""Create a rootStyle if not defined, then set the arguments from **kwargs, if their entry name already exists.
        This is similar (but not identical) to the makeStyle in Elements. There any value entry is copied, even if that
        is not defined in the root style."""
        if rootStyle is None:
            rootStyle = getRootStyle()
        for name, v in kwargs.items():
            if name in rootStyle: # Only overwrite existing values.
                rootStyle[name] = v 
        return rootStyle

    def applyStyle(self, style):
        u"""Apply the key-value of the style onto the self.rootStyle."""
        for key, value in style.items():
            self.rootStyle[key] = value

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
        If the style is found from the (cascading) sId, then use that to return the requested attribute.
        Note that self.css( ) is a generic query for a named CSS value, upwards the parent tree.
        This is different from the CSS functions as self.buildCss( ), that actually generate CSS code."""
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

    def _get_padding(self): # Tuple of paddings in CSS order, direction of clock
        return self.pt, self.pr, self.pb, self.pl
    def _set_padding(self, padding):
        # Can be 123, [123], [123, 234] or [123, 234, 345, 4565, ]
        if isinstance(padding, (long, int, float)):
            padding = [padding]
        if len(padding) == 1: # All same value
            padding = (padding[0], padding[0], padding[0], padding[0], padding[0], padding[0])
        elif len(padding) == 2: # pt == pb, pl == pr, pzf == pzb
            padding = (padding[0], padding[1], padding[0], padding[1], padding[0], padding[1])
        elif len(padding) == 3: # pt == pl == pzf, pb == pr == pzb
            padding = (padding[0], padding[1], padding[2], padding[0], padding[1], padding[2])
        elif len(padding) == 4: # pt, pr, pb, pl, 0, 0
            padding = (padding[0], padding[1], padding[2], padding[3], 0, 0)
        elif len(padding) == 6:
            pass
        else:
            raise ValueError
        self.pt, self.pr, self.pb, self.pl, self.pzf, self.pzb = padding
    padding = property(_get_padding, _set_padding)

    def _get_pt(self): # Padding top
        return self.css('pt', 0)
    def _set_pt(self, pt):
        self.rootStyle['pt'] = pt  
    pt = property(_get_pt, _set_pt)

    def _get_pb(self): # Padding bottom
        return self.css('pb', 0)
    def _set_pb(self, pb):
        self.rootStyle['pb'] = pb  
    pb = property(_get_pb, _set_pb)
    
    def _get_pl(self): # Padding left
        return self.css('pl', 0)
    def _set_pl(self, pl):
        self.rootStyle['pl'] = pl 
    pl = property(_get_pl, _set_pl)
    
    def _get_pr(self): # Margin right
        return self.css('pr', 0)
    def _set_pr(self, pr):
        self.rootStyle['pr'] = pr  
    pr = property(_get_pr, _set_pr)

    def _get_pzf(self): # Padding z-axis front
        return self.css('pzf', 0)
    def _set_pzf(self, pzf):
        self.rootStyle['pzf'] = pzf  
    pzf = property(_get_pzf, _set_pzf)
    
    def _get_pzb(self): # Padding z-axis back
        return self.css('pzb', 0)
    def _set_pzb(self, pzb):
        self.rootStyle['pzb'] = pzb  
    pzb = property(_get_pzb, _set_pzb)

    #   F O N T S

    def getInstalledFonts(self):
        u"""Answer the list of font names, currently installed in the application."""
        return self.view.installedFonts()

    def installFont(self, path):
        u"""Install a font with a given path and the postscript font name will be returned. The postscript
        font name can be used to set the font as the active font. Fonts are installed only for the current
        process. Fonts will not be accessible outside the scope of drawBot.
        All installed fonts will automatically be uninstalled when the script is done."""
        return self.view.installFont(path)

    #   P A G E S

    def appendPage(self, pageOrView):
        u"""Append a page to the document. Assert that it is a page element."""
        if pageOrView.isView:
            pageOrView.setParent(self) # Set parent as weakref, without calling self.appendElement again.
            self.view = pageOrView
        elif pageOrView.isPage:
            pageOrView.setParent(self) # Set parent as weakref, without calling self.appendElement again.
            if self.pages.keys():
                pn = max(self.pages.keys())+1
            else:
                pn = 0
            self[pn] = pageOrView
        else:
            raise TypeError, ('Cannot add element "%s" to document. Only pages and view supported.' % pageOrView)
    
    appendElement = appendPage

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

    def isLeft(self):
        u"""This is reached for e.isleft() queries, when elements are not placed on a page.
        The Document cannot know the answer then. Always answer False."""
        return False
    isRight = isLeft
    
    def isLeftPage(self, page):
        u"""Answer the boolean flag if the page is currently defined as a left page. Left page is even page number"""
        for pn, pnPages in self.pages.items():
            if page in pnPages:
                return bool(pn & 0x1)
        return False # Page not found

    def isRightPage(self, page):
        u"""Answer the boolean flag if the page is currently defined as a left page. Right page is odd page number."""
        for pn, pnPages in self.pages.items():
            if page in pnPages:
                return not pn & 0x1
        return False # Page not found

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

    def makePages(self, pageCnt, pn=0, template=None, name=None, w=None, h=None, **kwargs):
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
        u"""Evaluate the content of all pages to return the total sum of conditions solving.
        If necessary, the builder for solving specific text conditions, such as
        run length of text and overflow of text boxes, is found by the current self.view.b."""
        score = Score()
        for pn, pnPages in sorted(self.pages.items()):
            for page in pnPages: # List of pages with identical pn, step through the pages.
                page.solve(score)
        return score

    #   V I E W S

    def setView(self, viewId):
        u"""Set the self.view default view, that will be used for checking on view parameters,
        before any element rendering is done, such as layout conditions and creating the right
        type of strings. 
        """
        self.view = viewClasses[viewId](parent=self, w=self.w, h=self.h)

    #   D R A W I N G  &  B U I L D I N G

    def build_css(self, view):
        u"""Build the CSS for this document. Default behavior is to import the content of the file
        if there is a path reference, otherwise build the CSS from the available values and parameters
        in self.style and self.css()."""
        b = view.b
        if self.info.cssPath is not None:
            b.importCss(self.info.cssPath) # Add CSS content of file, if path is not None and the file exists.
        else: 
            b.headerCss(self.name or self.title)
            b.resetCss() # Add CSS to reset specific default behavior of browsers.
            b.sectionCss('Document root style')
            b.css('body', self.rootStyle) # <body> selector and style output

    def build(self, name=None, path=None, pageSelection=None, multiPage=True):
        u"""Build the document as website, using the MampView for export."""
        self.view.build(name=name, path=path, pageSelection=pageSelection, multiPage=multiPage)

    def export(self, path, multiPage=True):
        self.build(path=path, multiPage=multiPage)

