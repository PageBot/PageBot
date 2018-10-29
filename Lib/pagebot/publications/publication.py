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
from pagebot.elements import Element
from pagebot.document import Document

class Publication(Element):
    u"""Implementing data and templates for generic publications.
    See also other – more specific – implementations, such as Poster, Brochure and Magazines.

    An old approach was to make Publication subclass from Document, but it shows to be more
    flexible as holding all kinds of information, generating multiple types of documents,
    the Publication class is now an independent base class, holding multiple documents. 
    """

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