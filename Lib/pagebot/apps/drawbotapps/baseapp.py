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
#     baseapp.py
#
from vanilla import Window

class BaseApp(object):
    u"""The BaseApp class implements generic functions for DrawBotApp classes.
    The main function of apps is to create applications (with window UI) that
    offers an interface to PageBot publication building scripts. This way
    apps can be stored and standalone desktop applications, offering more
    interactive feedback to non-scripting users. 
    Also it hides code form the user, just presenting a coherent set of choices,
    that then build into PDF documents, websites or identity stationary.
    """
    W, H = 400, 400
    DEFAULT_NAME = 'Publication'
    
    def __init__(self):
        self.w = Window((100, 100, self.W, self.H), self.__class__.__name__)
        self.buildAppUI()
        self.initialize()
        self.w.open()

    def buildAppUI(self):
        u"""To be implemented by inheriting app classes."""

    def initialize(self):
    	u"""To be implemente by inheriting app classes.
    	Should initialize the self._doc Publication instance.
    	"""

    def buildPublication(self, sender=None):
    	u"""Default behavior, building the publications. To be redefined by
    	inheriting classes if additional functions are needed."""
    	self._doc.solve()
    	self._doc.export('_export/%s.pdf' % self.DEFAULT_NAME)
   

