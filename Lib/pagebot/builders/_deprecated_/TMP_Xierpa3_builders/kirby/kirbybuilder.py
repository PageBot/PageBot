# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
# 	xierpa server
# 	(c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
# 	X I E R P A  3
# 	No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#   phpbuilder.py
#
from xierpa3.builders.cssbuilder import CssBuilder
from xierpa3.builders.htmlbuilder import HtmlBuilder

class XXXKirbyBuilder(HtmlBuilder): 

    # Default usage is to run the Kirby PHP application under MAMP.
    PATH_ROOT = '/Applications/MAMP/htdocs/'
    DIRECTORIES = (
        'assets/css/', 'content/', 'kirby/', 'panel/', 
        'site/templates/', 'site/snippets/',
    )  
    def theme(self, component):
        pass
    
    def _theme(self, component):
        pass
    
    def page(self, component):
        self.clear() # Clear the output stream for next theme page
        
    def _page(self, component):
        pass
        
    def getRootPath(self): 
        return self.PATH_ROOT
    
    def setRootPath(self, path):
        self.PATH_ROOT = path
        
    def getStylePath(self, component):
        u"""Answer the relative local path to the CSS file."""
        return 'assets/css/style.css'
        
    def getTemplatePath(self, component):
        u"""Answer the relative local oath to the template of **component**."""
        return 'site/templates/%s.php' % component.name
    
    def XXXgetCmsPath(self):
        return self.getRootPath() + 'panel/defaults/blueprints/%.php'

    #   S A V E 
    
    def save(self, theme, path=None, makeDirectory=True):
        u"""Create all necessery Kirby directories. Then call the CssBuilder and
        HtmlBuilder to generate the site files. Note that the special PHP syntax in
        the HTML output is entirely caused by the KirbyAdapter, generating the
        PHP code instead of fixed content."""
        if path is None:
            path = self.getRootPath() + theme.root.name.lower() + '/'
        self.makeDirectory(path)
        for directory in self.DIRECTORIES:
            self.makeDirectory(path + directory)
        # Output CSS as single .scss and convert to .css
        builder = CssBuilder()
        builder.save(theme, path + self.getStylePath(theme))
        # Output HTML pages
        builder = HtmlBuilder()
        builder.save(theme, path + self.getTemplatePath(theme))
        
    #   B L O C K
    
    def snippet(self, component, name):
        u"""Allows inheriting (PHP) classes to save the block code to another snippet file,
        by redefining this method. Default behavior is to do nothing"""
        self.tabs()
        self.text(self.adapter.getSnippet(name))
        self.pushResult(name=name) # Divert the output, so we can save the block content in the snippet file.
        
    def _snippet(self, component):
        u"""Store the snippet block content in the snippet file."""
        name, block = self.popNameResult()
        print name, block
