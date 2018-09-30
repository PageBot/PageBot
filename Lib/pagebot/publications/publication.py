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

class Publication(Element):
    u"""Implementing data and templates for generic publications.
    See also other – more specific – implementations, such as Poster, Brochure and Magazines.

    An old approach was to make Publication subclass from Document, but it shows to be more
    flexible as holding all kinds of information, generating multiple types of documents,
    the Publication class is now an independent base class, holding multiple documents. 
    """

    def getAPI(self):
    	u"""Answer the API dictionary for this class that can be used by calling apps,
    	e.g. for construction and behavior of the scope of app UI parameter controls.
		This method needs to be redefined by inheriting publications classes to answer
		different than the default empty dictionary."""
    	return {}
