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
#   cssbuilder.py
#
import os
from xierpa3.builders.sassbuilder import SassBuilder

class CssBuilder(SassBuilder):
    u"""
    Used for dispatching component.build_sass, if components want to define builder dependent behavior.
    """
    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = SassBuilder.C 

    ID = C.TYPE_CSS # Also the default extension of the output format
    EXTENSION = ID
    ATTR_POSTFIX = ID # Postfix of dispatcher and attribute names above generic names.
    # DEFAULT_PATH inherits from SassBuilder
    
    # Compile by Sass, style is defined by /csstype-<styleType>
    def initialize(self):
        SassBuilder.initialize(self)
        self.css = None

    def save(self, component, path=None, root=None, styleType=None):
        u"""
        Style type is one of ['nested', 'expanded', 'compact', 'compressed'].
        Given by the url parameter "/css-nested".
        """
        # Is there a server environment, then overwrite the style type.
        if self.e is not None: 
            styleType = self.e.form[self.C.PARAM_CSSTYPE] or styleType or 'expanded'
        if not styleType in self.C.SASS_STYLES:
            styleType = self.C.SASS_DEFAULTSTYLE
        if path is None: # Allow full overwrite of complete path.
            assert root is not None # Always needs external root path defined.
            path = self.getFilePath(component, root)
        scssPath = path.replace('.css', '.scss')
        SassBuilder.save(self, component, path=scssPath)
        # Call external sass application to always compile SCSS into CSS
        os.system('sass --trace %s %s --style %s; chmod a+r %s' % (scssPath, path, styleType, path))
        # Read the compiled CSS into self.css to be answered as result of this builder.
        f = open(path, 'r')
        self.css = f.read()
        f.close()
        return path
    
    def getResult(self):
        u"""If there is any compiled result from SASS to CSS, then answer it.
        Otherwise answer the result of @self.popResult()@."""
        if self.css is not None:
            return self.css
        return self.popResult()
