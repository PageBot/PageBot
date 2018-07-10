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
#     basecontext.py
#
import os
from pagebot.style import DISPLAY_BLOCK

class BaseContext(object):
    """A BaseContext instance abstracts the specific functions of a platform
    (for instance DrawBot, Flat or HTML), thus hiding e.g. the type of
    BabelString instance needed, and the type of HTML/CSS file structure to be
    created."""

    # In case of specific builder addressing, callers can check here.
    isDrawBot = False
    isFlat = False
    isSvg = False
    isInDesign = False

    # To be redefined by inheriting context classes.
    STRING_CLASS = None
    EXPORT_TYPES = None

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    #   S C R E E N

    def screenSize(self):
        """Answers the current screen size."""
        return None

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from s
        (converted to plain unicode string), using e or style as typographic parameters.
        Ignore and just answer s if it is already a self.STRING_CLASS instance.
        """
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.newString(u'%s' % s, context=self, e=e, style=style, w=w, h=h,
                pixelFit=pixelFit)
            print(s)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def fitString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from s
        assuming that style['font'] is a Variable Font instnace, or a path
        pointing to one.  If the for is not a VF, then behavior is the same as
        newString.  (converted to plain unicode string), using e or style as
        typographic parameters.  Ignore and just answer s if it is already a
        self.STRING_CLASS instance.
        """
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.fitString(u'%s' % s, context=self, e=e, style=style, w=w, h=h,
                pixelFit=pixelFit)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def newText(self, textStyles, e=None, w=None, h=None, newLine=False):
        """Answers the BabelString, as combination of all text and style in
        textStyles, which is supposed to have format [(baseString, style),
        (baseString, style), ...]. Add return \n to the string is the newLine
        attribute is True or if a style has style.get('display') ==
        DISPLAY_BLOCK."""
        assert isinstance(textStyles, (tuple, list))
        s = None
        for t, style in textStyles:
            if newLine or (style and style.get('display') == DISPLAY_BLOCK):
                t += '\n'
            bs = self.newString(t, style=style, e=e, w=w, h=h)
            if s is None:
                s = bs
            else:
                s += bs
        return s

    #   P A T H

    def checkExportPath(self, path):
        """If the path starts with "_export" make sure it exists, otherwise
        create it. The _export folders are used to export documents locally,
        without saving them to git. The _export name is included in the git
        .gitignore file.

        >>> context = BaseContext()
        >>> context.checkExportPath('_export/myFile.pdf')
        >>> os.path.exists('_export')
        True
        """
        if path.startswith('_export'):
            dirPath = '/'.join(path.split('/')[:-1])
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
        

    #   V A R I A B L E

    def Variable(self, ui, globals):
        """Offers interactive global value manipulation in DrawBot. Probably
        to be ignored in other contexts."""
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
