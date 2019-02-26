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

SITE_NAME = 'SimpleSite'

MD_PATH = 'content.md'
EXPORT_PATH = '_export/' + SITE_NAME

DO_PDF = 'Pdf' # Save as PDF representation of the site.
DO_FILE = 'File' # Generate website output in _export/SimpleSite and open browser on file index.html
DO_MAMP = 'Mamp' # Generate website in /Applications/Mamp/htdocs/SimpleSite and open a localhost
DO_GIT = 'Git' # Generate website and commit to git (so site is published in git docs folder.
EXPORT_TYPE = DO_FILE

blueColor = color(rgb='#2A8BB8')

headerBackgroundColor = color(0.9) #whiteColor
heroBackgroundColor = color(0.95)
bannerBackgroundColor = color(0, 1, 0) #whiteColor
navigationBackgroundColor = blackColor
coloredSectionBackgroundColor = blueColor
logoColor = blueColor
logoBackgroundColor = color(1, 1, 0)
coloredSectionColor = color(0.9)
footerBackgroundColor = color(0.8)
footerColor = blackColor

siteDescription = [
    ('index', 'PageBot Responsive Home'),
    ('content', 'PageBot Responsive Content'),
    ('page3', 'PageBot Responsive Page 3'),
    ('page4', 'PageBot Responsive Page 4'),
    ('page5', 'PageBot Responsive Page 5'),
]
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
def makeNavigation(header, currentPage):
    navigation = Navigation(parent=header, fill=navigationBackgroundColor)
    # TODO: Build this automatic from the content of the pages table.
    menu = TopMenu(parent=navigation)
    menuItem1 = MenuItem(parent=menu, href='index.html', label='Home', current=currentPage=='index.html')
    menuItem2 = MenuItem(parent=menu, href='content.html', label='Internal page demo', current=currentPage=='content.html')
    menuItem3 = MenuItem(parent=menu, href='page3.html', label='menu item 3', current=currentPage=='page3.html')
    menuItem4 = MenuItem(parent=menu, href='page4.html', label='menu item 4', current=currentPage=='page4.html')
    menuItem5 = MenuItem(parent=menu, href='page5.html', label='menu item 5', current=currentPage=='page5.html')
    
    menu3 = Menu(parent=menuItem3)
    menuItem31 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.1', current=False)
    menuItem32 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.2 with longer link name', current=False)
    menuItem33 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.3', current=False)
    menuItem34 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.4', current=False)
    menuItem35 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.5', current=False)
    menuItem36 = MenuItem(parent=menu3, href='page3.html', label='menu item 3.6', current=False)

    menu33 = Menu(parent=menuItem33)
    menuItem331 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.1', current=False)
    menuItem332 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.2 with longer link name', current=False)
    menuItem333 = MenuItem(parent=menu33, href='page3.html', label='menu item 3.3.3', current=False)
    
    menu4 = Menu(parent=menuItem4)
    menuItem41 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.1', current=False)
    menuItem42 = MenuItem(parent=menu4, href='page4.html', label='menu item 4.2', current=False)
    
    menu5 = Menu(parent=menuItem5)
    menuItem51 = MenuItem(parent=menu5, href='page5.html', label='menu item 5.1', current=False)
    menuItem52 = MenuItem(parent=menu5, href='page5.html', label='menu item 5.2', current=False)

    return navigation

def makePages(doc, siteDescription):

    for pn, (name, title) in enumerate(siteDescription):
        pn += 1 # Page numbers start at 1
        page = doc[pn]
        page.name, page.title = name, title
        page.description = 'PageBot SimpleSite is a basic generated template for responsive web design'
        page.keyWords = 'PageBot Python Scripting Simple Demo Site Design Design Space'
        page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'
        page.style = styles['body']

        currentPage = name + '.html'
        # Add neste content elements for this page.
        conditions = (Left2Left(), Float2Top(), Fit2Width())
        header = Header(parent=page, fill=headerBackgroundColor, conditions=conditions)
        banner = Banner(parent=header, fill=bannerBackgroundColor, conditions=conditions)
        logo = Logo(parent=banner, name=name, textFill=logoColor, fill=logoBackgroundColor,
            conditions=(Left2Left(), Float2Top()))
        navigation = makeNavigation(header, currentPage)

        if pn == 1:
            hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor)    
            content = Content(parent=page)
            section = ColoredSection(parent=page, fill=coloredSectionBackgroundColor)
            content = Content(parent=page, contentId='Content2') #  fill=(0.7, 0.7, 0.9)
        elif pn == 2:
            hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor)    
            content = Content(parent=page)
            section = ColoredSection(parent=page, fill=coloredSectionBackgroundColor)
        elif pn == 3:
            hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor)    
            content = Content(parent=page)
            section = ColoredSection(parent=page, fill=coloredSectionBackgroundColor)
        elif pn == 4:
            hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor)    
            content = Content(parent=page)
            section = ColoredSection(parent=page)
        elif pn == 5:
            hero = Hero(parent=page, fontSize=em(1.1), fill=heroBackgroundColor)    
            content = Content(parent=page)
            section = ColoredSection(parent=page, fill=coloredSectionBackgroundColor,
                textFill=coloredSectionColor)
        footer = Footer(parent=page, fill=footerBackgroundColor, textFill=footerColor)


def makeSite(siteDescription, styles, viewId):
    doc = Site(viewId=viewId, autoPages=len(siteDescription), styles=styles)
    view = doc.view
    view.resourcePaths = ('css','fonts','images','js')
    view.jsUrls = (
        URL_JQUERY, 
        #URL_MEDIA, 
        'js/main.js'
    )
    # SiteView will automatic generate css/style.scss.css from assumed css/style.scss
    view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style-org.css')

    # Make the all pages and elements of the site as empty containers
    makePages(doc, siteDescription)    
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
    doc = makeSite(siteDescription, styles=styles, viewId='Page')
    doc.export(EXPORT_PATH + '.pdf')

elif EXPORT_TYPE == DO_FILE:
    doc = makeSite(siteDescription, styles=styles, viewId='Site')
    siteView = doc.view
    doc.export(EXPORT_PATH)
    #print('Site file path: %s' % EXPORT_PATH)
    os.system(u'/usr/bin/open "%s"' % ('%s/index.html' % EXPORT_PATH))

elif EXPORT_TYPE == DO_MAMP:
    # Internal CSS file may be switched off for development.
    doc = makeSite(siteDescription, styles=styles, viewId='Mamp')
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
    doc = makeSite(siteDescription, styles=styles, viewId='Git')
    doc.export(EXPORT_PATH)
    # Open the css file in the default editor of your local system.
    os.system('git pull; git add *;git commit -m "Updating website changes.";git pull; git push')
    os.system(u'/usr/bin/open "%s"' % view.getUrl(DOMAIN))

else: # No output view defined
    print('Set EXPORTTYPE to DO_FILE or DO_MAMP or DO_GIT')

