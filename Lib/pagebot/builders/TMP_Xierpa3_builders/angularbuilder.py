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
#   angularbuilder.py
#
from builder import Builder

class AngularBuilder(Builder):

    #    @@@ Under development

    # Get Constants->Config as class variable, so inheriting classes can redefine values.
    C = Builder.C 

    # Used for dispatching component.build_sass, if components want to define builder dependent behavior.
    ID = 'angular'

    def build(self, descriptor, components):
        pass
