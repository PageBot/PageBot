#!/usr/bin/env python
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

from pagebot.publications.publication import Publication
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.composer import Composer
from pagebot.typesetter import Typesetter
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.color import color, whiteColor, blackColor
from pagebot.toolbox.units import em, pt
from pagebot.elements.web.simplesite.siteelements import *

SITE_NAME = 'D3Beziers'

MD_PATH = 'content.md'
EXPORT_PATH = '_export/' + SITE_NAME

USE_SCSS = True

DO_PDF = 'Pdf' # Save as PDF representation of the site.
DO_FILE = 'File' # Generate website output in _export/SimpleSite and open browser on file index.html
DO_MAMP = 'Mamp' # Generate website in /Applications/Mamp/htdocs/SimpleSite and open a localhost
DO_GIT = 'Git' # Generate website and commit to git (so site is published in git docs folder.
EXPORT_TYPE = DO_FILE

blueColor = color(rgb='#2A8BB8')

headerBackgroundColor = color(1) #whiteColor
heroBackgroundColor = whiteColor
bannerBackgroundColor = color(0, 1, 0) #whiteColor
navigationBackgroundColor = blackColor
coloredSectionBackgroundColor = whiteColor
logoColor = blueColor
logoBackgroundColor = color(1, 1, 0)
coloredSectionColor = color(0.4)
footerBackgroundColor = color(1)
footerColor = blackColor
CurrentMenu = color(0, 0, 255)

styles = dict(
    body=dict(
        fill=whiteColor,
        margin=em(0),
        padding=em(3),
        fontSize=pt(12),
        leading=em(1.4),
    ),
    br=dict(leading=em(1.4)
    ),
)

def makePage(doc):

    page = doc[1] # There is only one page here.
    page.name, page.title = 'index', SITE_NAME
    page.description = 'PageBot D3 single page site is a basic generated template for responsive web design'
    page.keyWords = 'D3 PageBot Python Scripting Simple Demo Site Design Design Space'
    page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'
    page.style = styles['body']

    currentPage = page.name + '.html'
    # Add nested content elements for this page.
    conditions = (Left2Left(), Float2Top(), Fit2Width())
    # comlpete header
    header = Header(parent=page, fill=headerBackgroundColor, conditions=conditions)
    banner = Banner(parent=header, fill=bannerBackgroundColor, conditions=conditions)
    logos = Logo(parent=banner, name=page.title, textFill=logoColor, fill=logoBackgroundColor,
        conditions=(Left2Left(), Float2Top()))

    #section for the 1st image slider
    #1st section content
    content = Content(parent=page, cssID='vis', conditions=(Fit2LeftSide()) )
    #content = SecondSection(parent=page, cssID='vis')
    #hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor) 
    #section for the 3 column layout
    #3rth section content repeat
    content = Content(parent=page)
    content = Content(parent=page, contentId='Content2') #  fill=(0.7, 0.7, 0.9)
    section = ColoredSection(parent=content, fill=coloredSectionBackgroundColor, cssClass='paddingcolor')

    footer = Footer(parent=page, fill=footerBackgroundColor, textFill=footerColor)


def makeSite(styles, viewId):
    doc = Site(viewId=viewId, autoPages=1, styles=styles)
    view = doc.view
    view.resourcePaths = ('css','fonts','images','js')
    view.jsUrls = (URL_JQUERY, URL_MEDIA, 'js/d3.js', 'js/main.js')
    # SiteView will automatic generate css/style.scss.css from assumed css/style.scss
    if USE_SCSS:
        view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style.scss.css')
    else:
        view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style-org.css')

    # Make the single page and elements of the site as empty containers
    makePage(doc)    
    # By default, the typesetter produces a single Galley with content and code blocks.
    
    t = Typesetter(doc.context)
    galley = t.typesetFile(MD_PATH)
    # Create a Composer for this document, then create pages and fill content. 
    composer = Composer(doc)
    # The composer executes the embedded Python code blocks that direct where context should go.
    # by the HtmlContext.
    composer.compose(galley)
    
    doc.solve() # Solve all layout and float conditions for pages and elements.

    return doc
    
if EXPORT_TYPE == DO_PDF: # PDF representation of the site
    doc = makeSite(styles=styles, viewId='Page')
    doc.export(EXPORT_PATH + '.pdf')

elif EXPORT_TYPE == DO_FILE:
    doc = makeSite(styles=styles, viewId='Site')
    siteView = doc.view
    siteView.useScss = USE_SCSS
    doc.export(EXPORT_PATH)
    #print('Site file path: %s' % EXPORT_PATH)
    os.system(u'/usr/bin/open "%s"' % ('%s/index.html' % EXPORT_PATH))

elif EXPORT_TYPE == DO_MAMP:
    # Internal CSS file may be switched off for development.
    doc = makeSite(styles=styles, viewId='Mamp')
    mampView.useScss = USE_SCSS
    mampView.resourcePaths = view.resourcePaths
    mampView.jsUrls = view.jsUrls
    mampView.cssUrls = view.cssUrls
    print('View.jsUrls: %s' % view.jsUrls)
    print('View.cssUrls: %s' % view.cssUrls)

    MAMP_PATH = '/Applications/MAMP/htdocs/' + SITE_NAME 
    print('Site path: %s' % MAMP_PATH)
    doc.export(MAMP_PATH)

    if not os.path.exists(MAMP_PATH):
        print('The local MAMP server application does not exist. Download and in stall from %s.' % view.MAMP_SHOP_URL)
        os.system(u'/usr/bin/open %s' % view.MAMP_SHOP_URL)
    else:
        #t.doc.export('_export/%s.pdf' % NAME, multiPages=True)
        os.system(u'/usr/bin/open "%s"' % mampView.getUrl(SITE_NAME))

elif EXPORT_TYPE == DO_GIT and False: # Not supported for SimpleSite, only one per repository?
    # Make sure outside always has the right generated CSS
    doc = makeSite(styles=styles, viewId='Git')
    doc.export(EXPORT_PATH)
    # Open the css file in the default editor of your local system.
    os.system('git pull; git add *;git commit -m "Updating website changes.";git pull; git push')
    os.system(u'/usr/bin/open "%s"' % view.getUrl(DOMAIN))

else: # No output view defined
    print('Set EXPORTTYPE to DO_FILE or DO_MAMP or DO_GIT')