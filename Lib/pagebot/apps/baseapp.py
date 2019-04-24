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
#     baseapp.py
#
#from pagebot.publications.publication import Publication

#class BaseApp(Publication):
class BaseApp():
    """The BaseApp class implements generic functions for more specialize App classes.
    The main function of apps is to create applications (with window UI) that
    offer an interface to PageBot publication building scripts. Without scripting.
    This way apps can be stored as standalone desktop applications, offering more
    interactive feedback to non-scripting users.
    Also it hides code form the user, just presenting a coherent set of choices,
    that then build into PDF documents, websites, InDesign documents or identity stationary.

    Note that the BaseApp inherits from Elements, so UI elements can be used
    to define the inteface layout at it can be used present itself inside other
    elements, such as a page.
    """
    # NsApp callbacks.

    def terminate(self):
        pass

    def new(self):
        print('something new')

    def close(self):
        print('close something')

    def saveAs(self):
        pass

    def save(self):
        print('save something')

    def cut(self):
        print('cut something')

    def copy(self):
        print('copy something')

    def paste(self):
        print('paste something')

    def delete(self):
        print('delete something')

    def undo(self):
        print('undo something')

    def redo(self):
        print('redo something')
