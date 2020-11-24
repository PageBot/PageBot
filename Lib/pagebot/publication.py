#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     publication.py
#
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.finder import Finder
from pagebot.constants import *

class Publication(Element):
    """Implements data and templates for generic publications.

    Note: an earlier approach was to subclass Publication from Document, but it
    proved to be more flexible if the Publication class is an independent
    class that holds one or more documents.

    >>> from pagebot.constants import A4
    >>> from pagebot.filepaths import getResourcesPath
    >>> from pagebot import getContext
    >>> context = getContext()
    >>> p = Publication(getResourcesPath(), context=context) # Finder created from path
    >>> p.getAPI()
    {}
    >>> p.newDocument()
    <Document "Untitled" Pages=1 Templates=1 Views=1>
    >>> p.export()
    """
    FINDER_CLASS = Finder

    # Default values for a publication. To be redefined by inheriting publication classes.
    PAGE_SIZES = {
        'A3': A3,
        'A4': A4,
        'A5': A5,
        'B4': B4,
        'B5': B5,
    }
    DEFAULT_PAGE_SIZE_NAME = 'A4'
    DEFAULT_PAGE_SIZE = PAGE_SIZES[DEFAULT_PAGE_SIZE_NAME]

    TEMPLATES = {} # To be redefined by inheriting publication classes

    def __init__(self, findersOrPaths=None, api=None, templates=None, **kwargs):
        """

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.filepaths import getResourcesPath
        >>> path = getResourcesPath()
        >>> publication = Publication(findersOrPaths=path, context=context)
        >>> assert publication.context
        >>> publication.templates
        {}
        >>> len(publication.finders) > 0
        True
        """
        Element.__init__(self, **kwargs)
        if api is None:
            api = {} # All values will be default.
        self.api = api
        self.finders = {} # Key is finder root, so we keep unique finders.
        if not findersOrPaths: # At least make it search in the current directory
            findersOrPaths = ['.']
        self.addFinders(findersOrPaths)
        if templates is None:
            templates = self.TEMPLATES
        self.templates = templates
        self.initialize()

    def initialize(self):
        """Doing nothing by default. To be redefined by inheriting publications
        classes for default initialization of document and pages.
        """

    def getAPI(self):
        """Answers the API dictionary for this class that can be used by calling apps,
        e.g. for construction and behavior of the scope of app UI parameter controls.
        This method needs to be redefined by inheriting publications classes to answer
        different than the default empty dictionary."""
        return {}

    def produce(self, viewId=None, **kwargs):
        """Produce the publication, using the viewId as target. To be implemented by
        inheriting publication classes."""

    def newDocument(self, name=None, autoPages=None, w=None, h=None, makeCurrent=True,
            padding=None, theme=None, gw=None, gh=None, gridX=None, gridY=None,
            baselineGrid=None, baselineGridStart=None, context=None, **kwargs):
        """Answer a new Document instance for this publication, to be filled by the
        publication composer, using existing data and pages. Set autoPages to 0,
        so all pages are appended by the publication.
        Optional arguments can overwrite the parameters of the publication.
        """
        if name is None:
            name = self.name
        # If there is already a document with that name on stock, then simply answer
        # it without creating a new one. The current self.docName selection is not changed.
        assert name is not None
        for e in self.elements:
            if e.name == name:
                return e

        if autoPages is None:
            autoPages = 1
        if w is None:
            w = self.w
        if h is None:
            h = self.h
        if padding is None:
            padding = self.padding
        if gw is None: # Gutter width
            gw = self.gw
        if gh is None: # Gutter height
            gh = self.gh
        if gridX is None:
            gridX = self.gridX
        if gridY is None:
            gridY = self.gridY
        if baselineGrid is None:
            baselineGrid = self.baselineGrid
        if theme is None:
            theme = self.theme
        document = Document(name=name, w=w, h=h, padding=padding,
                context=context, theme=theme, gw=gw, gh=gh, gridX=gridX,
                gridY=gridY, autoPages=autoPages, baselineGrid=baselineGrid,
                baselineGridStart=self.baselineGridStart, **kwargs)
        view = document.view
        view.showGrid = self.showGrid
        view.showPadding = self.showPadding
        view.showImageLoresMarker = self.showImageLoresMarker
        view.showBaselineGrid = self.showBaselineGrid

        # Store the document in the publication as wrapped child element, and set
        # the current name as selected, so it can be retrieved if there are multiple
        # available at the same time.
        # Note that we can not use "self.doc" here, because a publication is a "normal"
        # element, the e.doc is used to find the top document where self can be placed in.
        # Yes, it's all very recursive.
        #
        DocWrap(document, parent=self)
        return document

    newSampleDocument = newDocument # To be redefined by inheriting publication classes.

    def _get_document(self):
        return self.getDocument(name=self.name)
    document = property(_get_document)

    def getDocument(self, name='Untitled', force=True):
        """Answer the named document, searching through the list of child elements.
        If it does not exist and he force flag is set, then create a new document
        and wrap it as child of self.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> pub = Publication(name='MyPublication', w=500, h=700, context=context)
        >>> doc = pub.document
        >>> doc
        <Document "MyPublication" Pages=1 Templates=1 Views=1>
        >>> doc.size
        (500pt, 700pt)
        """
        for e in self.elements: # Look for DocWrap child elements
            if isinstance(e, DocWrap):
                if name in (None, e.name): # If not name defined, then take first one.
                    return e.wrappedDocument
        if force: # If it does not exist, then create it with the settings of self.
            return self.newDocument(name=name)
        return None

    #   P A R T S

    def _get_partNames(self):
        """Answer the list names for all child elements that have one."""
        partNames = []
        for e in self.elements:
            if e.name:
                partNames.append(e.name)
        return partNames
    partNames = property(_get_partNames)

    #   F I N D I N G  I N T E R N A L  R E S O U R C E S

    def find(self, name=None, pattern=None, extension=None):
        """Answer elements created by fitting the name, pattern and/or extension."""
        elements = []
        for _, finder in sorted(self.finders.items()):
            elements = finder.find(name=name, pattern=pattern, extension=extension)
            if elements:
                break
        return elements

    #   F I N D I N G  E X T E R N A L  R E S O U R C E S

    def addFinders(self, findersOrPaths):
        """Add finders to the self.finders dictionary. If it is a file path, then create a Finder instance."""
        if not findersOrPaths:
            findersOrPaths = []
        elif not (findersOrPaths, (list, tuple)):
            findersOrPaths = [findersOrPaths]
        for finderOrPath in findersOrPaths:
            self.addFinder(finderOrPath)

    def addFinder(self, finderOrPath):
        """Add finder to the self.finders dictionary. If it is a file path, then create a Finder instance."""
        if isinstance(finderOrPath, str):
            finder = self.FINDER_CLASS(finderOrPath)
        else:
            finder = finderOrPath
        self.finders[finder.rootPath] = finder # Overwrite if there is already one on that root path,
        return finder # Answer the finders.

    def addTemplate(self, name, template):
        """Adds the template to the self.templates of dictionaries. There is no
        check, so the calling function can overwrite existing templates. Answer the
        template.

        >>> name ='TestTemplate'
        >>> t = Template(w=200, h=300, name=name)
        """

        """
        TODO: rewrite for publication
        >>> doc = Document(name='TestDoc')
        >>> doc.addTemplate('myTemplate', t)
        <Template>
        >>> doc.getTemplate('myTemplate').name == name
        True
        """
        template.parent = self
        self.templates[name] = template
        return template

    #   E X P O R T I N G

    def export(self, path=None, multiPage=True, **kwargs):
        document = self.document
        assert document is not None
        document.export(path=path, multiPage=multiPage, **kwargs)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
