# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#   javascriptbuilder.py
#
from xierpa3.builders.builder import Builder

class JavaScriptBuilder(Builder):
    u"""The JavaScriptBuilder implements the basic behavior of generating JavaScript output."""

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Builder.C 
    
    def comment(self, s):
        if s is not None:
            if isinstance(s, (tuple, list)):
                s = ', '.join(s)
            self.output('/* %s */\n' % s)
