# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
from basebuilder import BaseBuilder
from xmlbuilder import XmlBuilder
from htmlbuilder import HtmlBuilder
from webbuilder import WebBuilder

class BuildInfo(object):
    u"""Container with builder flags and data, as stored in elements, to direct conditional e.build( ) calls."""
    def __init__(self, **kwargs):
        self.title = None # Can be used to overwrite the standard name/title of an element.
        self.favIconUrl = None
        self.jsUrls = None
        self.appleTouchIconUrl = None
        self.keyWords = None
        self.jQueryUrl = 'http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'
        self.mediaQueriesUrl = 'http://code.google.com/p/css3-mediaqueries-js'
        self.viewPort = "width=device-width, initial-scale=1.0"

        self.webFonts = [
            'http://fonts.googleapis.com/css?family=Bree+Serif',
            'http://fonts.googleapis.com/css?family=Droid+Sans:400,700',
        ]
        # Define file paths where to read content, instead of constructing it via the builder.
        self.cssPath = None
        self.htmlPath = None
        self.headPath = None
        self.bodyPath = None

        for name, value in kwargs.items():
            assert hasattr(self, name) # Check only to set attributes that are supported by default value.
            setattr(self, name, value)

# Future developments Python --> JS ??
#
# http://stromberg.dnsalias.org/~strombrg/pybrowser/python-browser.html
# http://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html
# https://www.nativescript.org/nativescript-example-application?utm_medium=referral&utm_source=documentation&utm_campaign=getting-started
# http://pyjs.org
# http://www.infoworld.com/article/3033047/javascript/4-tools-to-convert-python-to-javascript-and-back-again.html
# 