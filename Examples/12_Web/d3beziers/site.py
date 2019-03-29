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
#     site.py
# 
#     This example creates a single page site that also can be exported as PDF.
#     It implements several D3.js info-graphics, starting with the interactice 
#     Bezier demo.

import os
import webbrowser

from pagebot.document import Document
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.color import color, whiteColor, blackColor
from pagebot.toolbox.units import em, pt

SITE_NAME = 'D3-Beziers'

MD_PATH = 'content.md'
EXPORT_PATH = '_export/' + SITE_NAME

DO_PDF = 'Pdf' # Save as PDF representation of the site.
DO_FILE = 'File' # Generate website output in _export/SimpleSite and open browser on file index.html
EXPORT_TYPE = DO_FILE

class D3Bezier(Element):
    u"""Container for header elements on a page. Using standard
    Element.build for non-Html contexts.
    """
    def build_html(self, view, path. **kwargs):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.header(cssClass='wrapper clearfix')
        for e in self.elements:
            e.build_html(view, path, **kwargs)
        b._header()
        b.comment('End '+self.__class__.__name__)

def makePage(doc):

    page = doc[1] # There is only one page here.
    page.name, page.title = 'index', SITE_NAME
    page.description = 'PageBot D3 single page site is a basic generated template for responsive web design'
    page.keyWords = 'D3 PageBot Python Scripting Simple Demo Site Design Design Space'
    page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'

    currentPage = page.name + '.html'
    # Add nested content elements for this page.
    conditions = (Left2Left(), Float2Top(), Fit2Width())
    D3Bezier(parent=page)


def makeSite(viewId):
    doc = Document(viewId=viewId, autoPages=1)
    view = doc.view
    view.resourcePaths = ('css','fonts','images','js')
    view.jsUrls = (
        URL_JQUERY, 
        #URL_MEDIA, 
        'js/d3.js', 
        'js/main.js'
    )
    # SiteView will automatic generate css/style.scss.css from assumed css/style.scss
    view.cssUrls = ('css/normalize.css', 'css/style.scss.css')

    # Make the single page and elements of the site as empty containers
    makePage(doc)        
    
    doc.solve() # Solve all layout and float conditions for pages and elements.

    return doc
    
if EXPORT_TYPE == DO_PDF: # PDF representation of the site
    doc = makeSite(styles=styles, viewId='Page')
    doc.export(EXPORT_PATH + '.pdf')

elif EXPORT_TYPE == DO_FILE:
    doc = makeSite(viewId='Site')
    siteView = doc.view
    doc.export(EXPORT_PATH)
    #print('Site file path: %s' % EXPORT_PATH)
    os.system(u'/usr/bin/open "%s"' % ('%s/index.html' % EXPORT_PATH))

else: # No output view defined
    print('Set EXPORTTYPE to DO_FILE or DO_MAMP or DO_GIT')
