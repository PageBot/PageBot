# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     validator.py
#
#     (For now) experimental approach. 
#     A validator contains a set of condition, that may (partially) be in conflict.
#     The validation takes a theshold value for the minimum “quality level” of all
#     conditions together, when applied on a container tree of elements.
#     This was validations can work on a page layout as a whole, but also on the
#     content of single containers.
#
class Validator(object):
    def __init__(self, conditions):
        self.conditions = conditions

    def evaluate(self, root, e):
        u"""Evaluate the content of element e with the total sum of conditions."""
        validationLevel = 0
        for condition in self.conditions:
            validationLevel += e.evaluate(root, condition)
        return validationLevel
         