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
#     googlecloudview.py
#
#     TO BE DEVELOPED: Use MampView amd GitView as model
#
from pagebot.elements.views.htmlview import HtmlView

class GoogleCloudView(HtmlView):
    """The GoogleCloudView works similar to MampView (local server) and
    GitView (gitub/docs server), serving locally saved static HTML/CSS/JS file, 
    that are created by the WebSite publications class, using the HtmlContext as 
    HTML/CSS generator.
    
    This is different from the GoogleAppsView, which is using a live Python server.
    For this PageBot + HtmlContext + FlatContext are uploaded and are running as live
    server generating HTML/CSS pages.
    """
    viewId = 'GoogleCloud'

