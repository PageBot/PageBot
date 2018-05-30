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
import objc
from AppKit import NSObject
from PyObjCTools import AppHelper

from pagebotapp import PageBotApp

class AppDelegate(NSObject):
    u"""
    Main delegate for PageBot application.
    """

    @objc.IBAction
    def applicationDidFinishLaunching_(self, notification):
        u"""
        """
        self.pagebotapp = PageBotApp()

    def applicationShouldTerminate_(self, sender):
        self.pagebotapp.terminate()
        return True

AppHelper.runEventLoop()
