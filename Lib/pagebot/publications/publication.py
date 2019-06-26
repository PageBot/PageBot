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
    u"""Implementing data and templates for generic publications.
    See also other – more specific – implementations, such as Poster, Brochure and Magazines.

    An old approach was to make Publication subclass from Document, but it shows to be more
    flexible as holding all kinds of information, generating multiple types of documents,
    the Publication class is now an independent base class, holding multiple documents. 
    
    >>> from pagebot.constants import A4
    >>> from pagebot.paths import RESOURCES_PATH
    >>> p = Publication(RESOURCES_PATH) # Finder created from path
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
        self.templates= templates

    def getAPI(self):
    	"""Answers the API dictionary for this class that can be used by calling apps,
    	e.g. for construction and behavior of the scope of app UI parameter controls.
		This method needs to be redefined by inheriting publications classes to answer
		different than the default empty dictionary."""
    	return {}
        

    def produce(self, viewId=None, **kwargs):
        """Produce the publication, using the viewId as target. To be implemented by
        inheriting pbulications classes."""
        pass

    def newDocument(self, name=None, autoPages=None, w=None, h=None, originTop=None, 
            padding=None, theme=None, gw=None, gh=None, gridX=None, gridY=None, 
            baselineGrid=None, baselineGridStart=None, **kwargs):
        """Answer a new Document instance for this publication, to be filled by the 
        publication composer, using existing data and pages. Set autoPages to 0,
        so all pages are appended by the publication.
        Optional arguments can overwrite the parameters of the publication.
        """
        if name is None:
            name = self.name
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
        doc = Document(name=name, w=w, h=h, originTop=originTop, padding=padding, 
            theme=theme, gw=gw, gh=gh, gridX=gridX, gridY=gridY, autoPages=autoPages,
            baselineGrid=baselineGrid, baselineGridStart=self.baselineGridStart, 
            **kwargs)
        view = doc.view
        view.showGrid = self.showGrid
        view.showPadding = self.showPadding
        view.showImageLoresMarker = self.showImageLoresMarker
        view.showBaselineGrid = self.showBaselineGrid
 
        return doc

    newSampleDocument = newDocument # To be redefined by inheriting publication classes.

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
        return finder # Answer the finders for convenience of the caller.


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])


