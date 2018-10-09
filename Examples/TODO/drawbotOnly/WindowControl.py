#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

import AppKit
from vanilla import Window, Button, CheckBox

class VariableController:

    def __init__(self, attributes, callback, document=None):
        self._callback = callback
        self._attributes = None
        self.w = vanilla.FloatingWindow((250, 50))
        self.buildUI(attributes)
        self.w.open()
        if document:
            self.w.assignToDocument(document)
        self.w.setTitle("Variables")

    def buildUI(self, attributes):
        if self._attributes == attributes:
            return
        self._attributes = attributes
        if hasattr(self.w, "ui"):
            del self.w.ui
        self.w.ui = ui = vanilla.Group((0, 0, -0, -0))
        y = 10
        labelSize = 100
        gutter = 5
        for attribute in self._attributes:
            uiElement = attribute["ui"]
            name = attribute["name"]
            args = dict(attribute.get("args", {}))
            height = 19
            # adjust the height if a radioGroup is vertical
            if uiElement == "RadioGroup":
                if args.get("isVertical", True):
                    height = height * len(args.get("titles", [""]))
            # create a label for every ui element except a checkbox
            if uiElement not in ("CheckBox", "Button"):
                # create the label view
                label = vanilla.TextBox((0, y + 2, labelSize - gutter, height), "%s:" % name, alignment="right", sizeStyle="small")
                # set the label view
                setattr(ui, "%sLabel" % name, label)
            else:
                args["title"] = name
            # check the provided args and add required keys
            if uiElement == "ColorWell":
                # a color well needs a color to be set
                # no size style
                if "color" not in args:
                    args["color"] = AppKit.NSColor.blackColor()
            elif uiElement == "TextEditor":
                # different control height
                # no size style
                height = attribute.get("height", 75)
            else:
                # all other get a size style
                args["sizeStyle"] = "small"
            # create the control view
            attr = getattr(vanilla, uiElement)((labelSize, y, -10, height), callback=self.changed, **args)
            # set the control view
            setattr(ui, name, attr)
            y += height + 6
        # resize the window according the provided ui elements
        self.w.resize(250, y)

    def changed(self, sender):
        self.documentWindowToFront()
        if self._callback:
            self._callback()

    def get(self):
        data = {}
        for attribute in self._attributes:
            if attribute["ui"] in ("Button", ):
                continue
            name = attribute["name"]
            data[name] = getattr(self.w.ui, name).get()
        return data

    def show(self):
        self.w.show()

    def documentWindowToFront(self, sender=None):
        self.w.makeKey()

def do(sender):
    controller = getController()
    controller.runCode() # runt je script opnieuw.

def getController():
    document = AppKit.NSDocumentController.sharedDocumentController().currentDocument()
    print(document)

    if not document:
        raise DrawBotError("There is no document open")
    controller = document.vanillaWindowController
    try:
        controller._variableController.buildUI(variables)
        controller._variableController.show()
    except:
        controller._variableController = VariableController(variables, controller.runCode, document)

    return controller

w = Window((978, 388, 400, 400), 'Test Vanilla in DrawBot')
w.button = Button((10, 10, 150, 30), 'Do', callback=do)
w.checkbox = CheckBox((10, 150, 150, 30), 'Check', callback=do)
w.open()
