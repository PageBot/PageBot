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
#     pagebot/contexts/__init__.py
#
import os
from pagebot.style import DISPLAY_BLOCK

class BaseContext(object):
    u"""A BaseContext instance combines the specific functions of a platform, 
    such as DrawBot, Flat or HTML. This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""
    
    # In case of specific builder addressing, callers can check here.
    isDrawBot = False
    isFlat = False
    isSvg = False

    # To be redefined by inheriting context classes.
    STRING_CLASS = None

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    
    #   S C R E E N

    def screenSize(self):
        u"""Answer the current screen size in DrawBot. Otherwise default is to do nothing."""
        return None

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        u"""Create a new styles BabelString instance of self.STRING_CLASS from s 
        (converted to plain unicode string), using e or style as typographic parameters. 
        Ignore and just answer s if it is already a self.STRING_CLASS instance.
        """
        print(self.STRING_CLASS)
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.newString(u'%s' % s, context=self, e=e, style=style, w=w, h=h, 
                pixelFit=pixelFit)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def newText(self, textStyles, e=None, w=None, h=None, newLine=False):
        u"""Answer the BabelString, as combination of all text and style in textStyles, which is supposed to
        have format [(baseString, style), (baseString, style), ...]. Add return \n to the string is the
        newLine attribute is True or if a style has style.get('display') == DISPLAY_BLOCK."""
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
        u"""If the path starts width "_export" make sure it exits, otherwise create it.
        The _export folders are used to local export documents, without saving them into git.
        The _export name is included in the git .gitignore file.

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
        """Offers interactive global value manipulation in DrawBot. 
        Probably to be ignored in other contexts."""
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
