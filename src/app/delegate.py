# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    PageBot appication.
#    Copyright (c) 2016+ Type Network
#
#
# -----------------------------------------------------------------------------
#
#    delegate.py
#

# General Python libraries.

import os, os.path
import string
import datetime

# Objective-C.
from vanilla import Window
import objc
from AppKit import NSObject
from PyObjCTools import AppHelper
from drawView import DrawView

from pagebotapp import PageBotApp

class AppDelegate(NSObject):
    u"""
    Main delegate for PageBot application.
    """

    windowSize = (800, 600)

    @objc.IBAction
    def applicationDidFinishLaunching_(self, notification):
        u"""
        """
        window = Window(self.windowSize, minSize=(1, 1), closable=True)
        window.drawView = DrawView((0, 32, -0, -0))
        window.outputView = None
        self.pagebotapp = PageBotApp(window)
        self.pagebotapp.initialize()
        window.open()

    def applicationShouldTerminate_(self, sender):
        self.pagebotapp.terminate()
        return True

AppHelper.runEventLoop()
