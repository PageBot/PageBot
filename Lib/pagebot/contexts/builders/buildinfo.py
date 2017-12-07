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
class BuildInfo(object):
    u"""Container with builder flags and data, as stored in elements, to guide conditional 
    e.build( ) and e.buildCss( ) and e.buildFlat( ) calls.
    Note that these attribute and flags can be defined specifically per element, so they
    cannot be part of a view.
    """
    def __init__(self, **kwargs):
        self.title = None # Can be used to overwrite the standard name/title of an element.
        self.description = None
        self.keyWords = None
        # Urls for <link>
        self.webFontsUrl = 'fonts/webfonts.css'
        self.favIconUrl = None
        self.jsUrls = None
        self.appleTouchIconUrl = None
        self.jQueryUrl = 'http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'
        self.jQueryUrlSecure = 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'
        self.mediaQueriesUrl = 'http://code.google.com/p/css3-mediaqueries-js'
        # Device
        self.viewPort = "width=device-width, initial-scale=1.0"
        # Fonts
        self.webFonts = [
            'http://fonts.googleapis.com/css?family=Bree+Serif',
            'http://fonts.googleapis.com/css?family=Droid+Sans:400,700',
        ]
        # Define file paths where to read content, instead of constructing by the builder.
        self.cssPath = None
        self.htmlPath = None
        self.headPath = None
        self.bodyPath = None

        for name, value in kwargs.items():
            assert hasattr(self, name) # Check only to set attributes that are supported by default value.
            setattr(self, name, value)

