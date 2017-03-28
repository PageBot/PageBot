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

from pagebot.style import makeStyle
from pagebot.toolbox.transformer import pointOrigin2D

class Document(object):
    u"""Container of Page instance, Style instances and Template instances."""
    
    from pagebot.elements.page import Page, Template
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    TEMPLATE_CLASS = Template # Allow inherited versions of the Template class.

    def __init__(self, rootStyle, styles=None, title=None, minPageId=1, pages=1, template=None, fileName=None, **kwargs):
        u"""Contains a set of Page instance and formatting methods. Allows to compose the pages
        without the need to send them directly to the output. This allows "asynchronic" page filling.
        Use (docW, docH) attributes if document size is different from page (w, h) in rootStyle."""

        self.rootStyle = makeStyle(rootStyle, **kwargs) # self.w and self.h are available as properties
        self.title = title or 'Untitled'
        self.fileName = fileName or (self.title + '.pdf')
        self.template = template # Used as default document master template if undefined in pages.
        self.pages = {} # Key is pageID, often the page number. Value is Page instances.
        self.initializeStyles(rootStyle, styles)
        # Expand the document to the request anount of pages. Make sure to use the size of the rootStyle,
        # not the style of the document, as it may be different.
        pageW = self.rootStyle['w']
        pageH = self.rootStyle['h']
        self.makePages(minPageId=minPageId, pages=pages, w=pageW, h=pageH, templates=template, **kwargs)
        # Storage for collected content while typesetting and composing, referring to the pages
        # they where placed on during composition.
        self.footnotes = {} # Keys is sequential order. Value is (page, e)
        self.literatureRefs = {} # Storage for literature references.
        self.imageRefs = {} # Storage for image references.
        self.toc = {} # Keys is header index, value is header node, to connect the header markers with the nodes.

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

    # Set the (w, h) from the rootStyle, if not defined as attributes. We keep the document size
    # separate from the actual page sizes, so the pages can detect if crop-marks should be drawn
    # and where to position them, depending on the page style settings of style['showCropMarks'] and
    # style['showPageFrame']. 
    # For intuitive compatibility doc.docW and doc.w have the same functionality.
    def _get_w(self):
        return self.rootStyle['docW'] or self.rootStyle['w']
    def _set_w(self, w):
        self.rootStyle['docW'] = w
    w = docW = property(_get_w, _set_w)

    def _get_h(self):
        return self.rootStyle['docH'] or self.rootStyle['h']
    def _set_h(self, h):
        self.rootStyle['docH'] = h
    h = docH = property(_get_h, _set_h)

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

    def addTocNode(self, node):
        u"""Add nodes for the Table of Content assembly. This adding is done during typesetting of the 
        galleys, typically by the header-hook method for headlines. A unique tocId is created that serves
        as key for the node to be stored. Then it is answered, to be used by the calling Typesetter
        in a marker in the text. Since we only can store strings in the attribute field of markers,
        we can not cache the node itself. Using the tocId as reference, the composer is able to 
        find back the relation between page-position of the marker and the related header node. """
        tocId = 'toc%d' % (len(self.toc)+1)
        self.toc[tocId] = node
        return tocId

    def __repr__(self):
        return '[Document: %s Pages: %d]' % (self.title, len(self))
        
    def __len__(self):
        return len(self.pages)
    
    def __getitem__(self, pIndex):
        u"""Answer page by index, which may be the same a the page number."""
        return self.pages[pIndex]

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

    def getLastPage(self):
        u"""Answer the page with the highest sorted page id. Answer None if there are not pages.
        """
        if self.pages:
            return self.pages[sorted(self.pages.keys())[-1]]
        return None

    def newPage(self, style=None, w=None, h=None, pageId=None, template=None, **kwargs):
        u"""Create a new page with the optional (w,h). Use (self.w, self.h) if one of the values is omitted.
        If pageId is omitted, then use the highest page number in self.pages as previous page.
        If pageId already exists, then raise an error."""
        if template is None: # If template undefined, then used document master template.
            template = self.template
        if template is not None:
            w = w or template.w
            h = h or template.h
        else: # If no template defined, tben use self.w, self.h from rootStyle.
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
        return page # Answer the page instance for convenience of the caller.
  
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
         
    def export(self, fileName, pageSelection=None, multiPage=True):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted. The fileName can have extensions ['pdf', 'svg', 'png', 'gif'] to direct the type of
        drawing and export that needs to be done.
        The multiPage value is passed on to the DrawBot saveImage call.

        document.export(...) is the most common way to export documents. But in special cases, there is not 
        straighforward (or sequential) export of pages, e.g. when generating HTML/CSS. In that case use 
        MyBuilder(document).export(fileName), the builder is responsible to query the document, pages, elements and styles."""
        if pageSelection is None:
            pageSelection = range(1, len(self.pages)+1) # [1,2,3,4,...] inclusive
        for pIndex in pageSelection:
            # Get the current Page instance, indicated by the page number.
            page = self.pages[pIndex] # Page numbering stars at #1
            # Create a new DrawBot viewport page to draw template + page, if not already done.
            # In case the document is oversized, then make all pages the size of the document, so the
            # pages can draw their crop-marks. Otherwise make DrawBot pages of the size of each page.
            newPage(self.w, self.h) #  Same size, make page of this size.
            # Let the page draw itself on the current DrawBot view port if self.writer is None.
            page.draw((0, 0)) 

        # If rootStyle['frameDuration'] is set and saving as movie or animated gif, 
        # then set the global frame duration.
        rs = self.getRootStyle()
        if rs['frameDuration'] is not None and (fileName.endswith('.mov') or fileName.endswith('.gif')):
            frameDuration(rs['frameDuration'])

        # http://www.drawbot.com/content/canvas/saveImage.html
        saveImage(fileName, multipage=multiPage)

