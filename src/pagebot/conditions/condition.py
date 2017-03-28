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
#     condition.py
#
class Condition(object):
    def __init__(self, value=1, tolerance=1, errorFactor=-10, verbose=False):
    	self.value = value # Value to answer if the condition is valid
        self.tolerance = tolerance
        self.errorFactor = errorFactor
        self.verbose = verbose

    def __repr__(self):
    	return '<Condition %s>' % self.transformations
