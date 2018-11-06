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
import os

from pagebot.elements import Element
from pagebot.document import Document
from pagebot.toolbox.finder import Finder

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

    def __init__(self, findersOrPaths, **kwargs):
        Element.__init__(self, **kwargs)
        self.finders = {} # Key is finder root, so we keep unique finders.
        self.addFinder(findersOrPaths)
        self.originTop = True
        
    def getAPI(self):
    	u"""Answers the API dictionary for this class that can be used by calling apps,
    	e.g. for construction and behavior of the scope of app UI parameter controls.
		This method needs to be redefined by inheriting publications classes to answer
		different than the default empty dictionary."""
    	return {}
        
    def newDocument(self, autoPages=1):
        u"""Answer a new Document instance for this publication, to be filled by the 
        publication composer, using existing data and pages. Set autoPages to 0,
        so all pages are appended by the publication.
        """
        doc = Document(w=self.w, h=self.h, originTop=self.originTop, padding=self.padding,
            gw=self.gw, gh=self.gh, gridX=self.gridX, gridY=self.gridY, autoPages=autoPages,
            baseline=self.baselineGrid, baselineStart=self.baselineGridStart)
        view = doc.view
        view.showGrid = self.showGrid
        view.showPadding = self.showPadding
        view.showImageLoresMarker = self.showImageLoresMarker
        view.showBaselines = self.showBaselines
        
        return doc

    #   P A R T S

    def _get_partNames(self):
        """Answer the list names for all child elements that have one."""
        partNames = []
        for e in self.elements:
            if e.name:
                partName.append(e.name)
        return partNames
    partNames = property(_get_partNames)

    #   F I N D I N G  R E S O U R C E S

    def find(self, name=None, pattern=None, extension=None):
        """Answer elements created by fitting the name, pattern and/or extension."""
        elements = []
        for _, finder in sorted(self.finders.items()):
            elements = finder.find(name=name, pattern=pattern, extension=extension)
            if elements:
                break
        return elements

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


