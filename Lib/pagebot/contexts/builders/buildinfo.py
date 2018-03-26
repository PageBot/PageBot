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
#     buildinfo.py
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
        self.appleTouchIconUrl = None
        # Make None for force unsecure version to load instead.
        self.jsUrls = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js',
            #'http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js',
            'http://code.google.com/p/css3-mediaqueries-js'
        )
        # Device
        self.viewPort = "width=device-width, initial-scale=1.0"
        # Fonts
        self.webFonts = (
            'http://fonts.googleapis.com/css?family=Bree+Serif',
            'http://fonts.googleapis.com/css?family=Droid+Sans:400,700',
        )
        # Define string or file paths where to read content, instead of constructing by the builder.
        self.htmlPath = None # Set to string in case the full HTML is defined in a single file.
        self.cssCode = None # Set to string, if CSS is available as single source.
        self.cssPath = None # Set to path, if CSS is available in a single file.
        self.headPath = None # Optional set to string that contains the page <head>...</head>, excluding the tags.
        self.headHtml = None # Set to path, if head is available in a single file, excluding the tags.
        self.bodyHtml = None # Optional set to string that contains the page <body>...</body>, excluding the tags.
        self.bodyPath = None # Set to path, if body is available in a single file, excluding the tags.
        self.jsPath = None # Optional javascript, to be added at the end of the page, inside <body>...</body> tag.
        self.jsCode = None # Set to path, if JS is available in a single file, excluding the tags.

        for name, value in kwargs.items():
            assert hasattr(self, name) # Check only to set attributes that are supported by default value.
            setattr(self, name, value)

