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
#     uigroup.py
#
from pagebot.elements.element import Element

class UIGroup(Element):
    """
    """
    def build(self, view, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        assert nsParent is not None
        group = self.context.group(x=self.x, y=self.y, w=self.w, h=self.h)
        setattr(nsParent, self.name or 'untitledGroup', group)
        for  e in self.elements:
            e.build(view, nsParent=group, **kwargs)
            
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
