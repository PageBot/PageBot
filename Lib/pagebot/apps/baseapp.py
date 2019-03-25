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

class BaseApp:

    def __init__(self):
        print('BaseApp init()')

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
