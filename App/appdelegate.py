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

    @objc.IBAction
    def new_(self, sender):
        self.pagebotapp.new()

    @objc.IBAction
    def open_(self, sender):
        self.pagebotapp.open()

    @objc.IBAction
    def close_(self, sender):
        self.pagebotapp.close()

    @objc.IBAction
    def save_(self, sender):
        self.pagebotapp.save()

    @objc.IBAction
    def saveAs_(self, sender):
        self.pagebotapp.saveAs()

    @objc.IBAction
    def cut_(self, sender):
        self.pagebotapp.cut()

    @objc.IBAction
    def copy_(self, sender):
        self.pagebotapp.copy()

    @objc.IBAction
    def paste_(self, sender):
        self.pagebotapp.paste()

    @objc.IBAction
    def delete_(self, sender):
        self.pagebotapp.delete()

    @objc.IBAction
    def undo_(self, sender):
        self.pagebotapp.undo()

    @objc.IBAction
    def redo_(self, sender):
        self.pagebotapp.redo()

AppHelper.runEventLoop()
