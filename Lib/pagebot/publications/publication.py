# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
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
#     publication.py
#
from pagebot.document import Document
      
class Publication(Document):
    u"""Subclass of Document, implementing templates for generic publications.
    See also other – more specific – implementations, such as Poster, Brochure and Manaziner.

    Originally Publication was an abstract class, holding multiple documents. But since the split 
    between the Document container class and View classes for representations, there is no need
    to have a "top-class" containing multiple documents."""

    def getAPI(self):
    	u"""Answer the API dictionary for this class that can be used by calling apps,
    	e.g. for construction and behavior of the scope of app UI parameter controls.
		This method needs to be redefined by inheriting publications classes to answer
		different than the default empty dictionary."""
    	return {}