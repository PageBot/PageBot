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
#     babelstring.py
#
class BabelString(object):
    u"""BabelString is the base class of various types of (formatted) string representations 
    needed for different builder classes."""

    def __init__(self, s, context):
        self.context = context # Store the context, in case we need it.
        self.s = s # Enclose the Flat string in this wrapper.

    def __repr__(self):
        return u'%s' % self.s

    def __add__(self, s):
        self.append(s)
        return self

    def __mul__(self, d):
        s = self.s
        for n in range(d-1):
            s += self.s
        self.s = s
        # Something to do with the html? 
        return self

    def __len__(self):
        return len(self.s)

    def append(self, s):
        u"""Append the BabelString content or plain string to self.s. Note that the type of
        string depends on the inheriting class."""
        if isinstance(s, BabelString): # This must be kind of BabelString, add the attribute string
            self.s += s.s
        else:
            self.s += s

    def type(self):
        u"""Answer the id of the class, in case a caller wants to know what kind of 
        BabelString this is."""
        return self.BABEL_STRING_TYPE

