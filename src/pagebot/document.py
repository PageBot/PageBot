# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     document.py
#
import copy
from pagebot.page import Page, Template
from pagebot.style import makeStyle
from drawBot import newPage, saveImage, installedFonts, installFont
            
class Document(object):
    u"""Container of Page instance, Style instances and Template instances."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    TEMPLATE_CLASS = Template # Allow inherited versions of the Template class.

    def __init__(self, rootStyle, styles=None, title=None, minPageId=1, pages=1, template=None, **kwargs):
        u"""Contains a set of Page instance and formatting methods. Allows to compose the pages
        without the need to send them directly to the output. This allows "asynchronic" page filling."""

        self.rootStyle = makeStyle(rootStyle, **kwargs) # self.w and self.h are available as properties
        self.title = title or 'Untitled'
        self.template = template # Used as document master template if undefined in pages.
        self.pages = {} # Key is pageID, often the page number. Value is Page instances.
        self.initializeStyles(rootStyle, styles)
        # Expand the document to the request anount of pages.
        self.makePages(minPageId=minPageId, pages=pages, w=self.w, h=self.h, templates=template, **kwargs)
        # Storage for collected content while typesetting and composing, referring to the pages
        # they where placed on during composition.
        self.footnotes = {} # Keys is sequential order. Value is (page, e)
        self.literatureRefs = {}
        self.toc = {}

    def initializeStyles(self, rootStyle, styles):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = {}
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, rootStyle)
        name = 'document'
        if not name in self.styles:
            self.addStyle(name, newStyle(name=name, showGrid=True))
        name = 'page'
        if not name in self.styles:
            self.addStyle(name, newStyle(name=name, showGrid=True))

    def _get_w(self):
        return self.rootStyle['w']
    w = property(_get_w)

    def _get_h(self):
        return self.rootStyle['h']
    h = property(_get_h)

    def fromRootStyle(self, **kwargs):
        u"""Answer a new style as copy from the root style. Overwrite the defined arguments."""
        style = copy.copy(self.styles['root'])
        for name, value in kwargs.items():
            setattr(style, name, value)
        return style
        
    def getStyles(self):
        return self.styles
 
    def getStyle(self, name):
        u"""Answer the names style. If that does not exist, answer the default root style."""
        self.styles.get(name) or self.styles['root']
        
    def getRootStyle(self):
        u"""Answer the default root style, used by the composer as default for all other stacked styles."""
        return self.styles['root']
              
    def setStyles(self, styles):
        u"""Set the dictionary of styles for the document. This method can be used to swap in/out a complete
        set of styles while processing specific pages. It is the responsibility of the caller to save the existing
        style set."""
        self.styles = styles

    def getInstalledFonts(self):
        u"""Answer the list of font names, currently installed in the application."""
        return installedFonts()

    def installFont(self, path):
        u"""Install a font with a given path and the postscript font name will be returned. The postscript
        font name can be used to set the font as the active font. Fonts are installed only for the current
        process. Fonts will not be accessible outside the scope of drawBot.
        All installed fonts will automatically be uninstalled when the script is done."""
        return installFont(path)

    def __repr__(self):
        return '[Document: %s Pages: %d]' % (self.title, len(self))
        
    def __len__(self):
        return len(self.pages)
    
    def __getitem__(self, pIndex):
        u"""Answer page by index, which may be the same a the page number."""
        return self.pages[pIndex]
    
    def addToc(self, node, page, fs, tag):
        u"""Add stuff for the Table of Content, connecting the node with the composed page."""
        if not page.pageId in self.toc:
            self.toc[page.pageId] = []
        self.toc[page.pageId].append((node, page, fs, tag))

    def getPage(self, pageId):
        u"""Answer the pageNumber, where the first pages #1 is self.pages[1]"""
        return self[pageId]
  
    def nextPage(self, page, nextPage=1, template=None, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page."""
        pageId = page.pageId + nextPage # Currently assuming it is a number.
        if not pageId in self.pages:
            self.newPage(eId=pageId, template=self.getTemplate())
        return self.getPage(pageId)
          
    def makePages(self, style=None, w=None, h=None, minPageId=1, pages=1, template=None, **kwargs):
        for pageId in range(minPageId, minPageId+pages):
            if template is None: # If template undefined, then use document master template.
                template = self.template
            self.newPage(style=style, w=w, h=h, eId=pageId, template=template, **kwargs)

    def lastPage(self):
        u"""Answer the page with the highest sorted page id. Answer None if there are not pages.
        """
        if not self.pages:
            return None
        return self.pages[sorted(self.pages.keys())[-1]]

    def newPage(self, style=None, w=None, h=None, pageId=None, template=None, **kwargs):
        u"""Create a new page with the optional (w,h). Use (self.w, self.h) if one of the values is omitted.
        If pageId is omitted, then use the highest page number in self.pages as previous page.
        If pageId already exists, then raise an error."""
        if template is None: # If template undefined, then used document master template.
            template = self.template
            w = w or template.w
            h = h or template.h
        else:
            w = w or self.w
            h = h or self.h
        if pageId is None:
            if not self.pages: # If not pages yet, start with the first page number defined in root style.
                rs = self.getRootStyle()
                pageId = rs['firstPageId']
            else:
                pageId = max(self.pages.keys())+1
        assert not pageId in self.pages # Make sure that we don't accidentally overwrite existing pages.
        page = self.PAGE_CLASS(parent=self, style=style, w=w, h=h, pageId=pageId, template=template, **kwargs)
        self.pages[pageId] = page
        return page
  
    def getStyle(self, name):
        u"""Answer the names style. Answer None if it does not exist."""
        return self.styles.get(name)

    def _getDefaultTemplate(self):
        u"""Answer tje most simple default template (one column, referring to the next page), to be used
        when everything else fails and there is no fall-back template defined by the calling application."""
        boxId = 'DEFAULT'
        template = self.TEMPLATE_CLASS(self.getRootStyle())
        template.cTextBox(0, 0, 4, 8, boxId, nextBox=boxId, nextPage=1)  # Simple template with 1 column.
        return template

    def getTemplate(self):
        u"""Answer the best choice of template by answering the document default template, as it is
        defined at Document creation. If it was omitted at that time, a default class template is used."""
        template = self.template # If template undefined, then use defined page template.
        if template is None: # Still None (not defined at Document creation), use to fallback default template.
            template = self._getDefaultTtemplate()
        return template

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
         
    def export(self, fileName, pageSelection=None):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted."""
        if pageSelection is None:
            pageSelection = range(1, len(self.pages)+1) # [1,2,3,4,...]
        for pIndex in pageSelection:
            # Get the current Page instance, indicated by the page number.
            page = self.pages[pIndex-1] # Page numbering stars at #1
            # Create a new Drawbot viewport page to draw template + page, if not already done.
            # Skip if the first page of the document was already made as graphic state canvas by a Composer instance.
            if pIndex > 0:
                newPage(page.w, page.h)
            # Let the page draw itself on the current Drawbot view port. pIndex can be used on output.
            page.draw() 
        saveImage(fileName)
