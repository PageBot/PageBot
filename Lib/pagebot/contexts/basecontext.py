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
class BaseContext(object):
    u"""A BaseContext instance combines the specific functions of a platform, 
    such as DrawBot, Flat or HTML. This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""
    
    # In case of specific builder addressing, callers can check here.
    isDrawBot = False
    isFlat = False

    # To be redefined by inheriting context classes.
    STRING_CLASS = None
    NEW_STRING = None

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new styles BabelString(HtmlString) instance from s (converted to plain unicode string), 
        using e or style. Ignore and answer s if it is already a FsString."""
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.NEW_STRING(u'%s' % s, context=self, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        assert isinstance(s, self.STRING_CLASS)
        return s

    #   V A R I A B L E

    def Variable(self, ui, globals):
        """Offers interactive global value manipulation in DrawBot. Probably to be ignored in other contexts."""
        pass
