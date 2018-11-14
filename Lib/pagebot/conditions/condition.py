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
#     condition.py
#
class Condition:
    def __init__(self, value=1, tolerance=1, error=-10, verbose=False):
        self.value = value # Value to answer if the condition is valid
        self.tolerance = tolerance
        self.error = error
        self.verbose = verbose

    def evaluate(self, e, score):
        """Answers the value between 0 and 1 to the level where the element is
        left aligned with the left margin of the parent."""
        parent = e.parent
        self.addScore(parent is not None and self.test(e), e, score)

    def addScore(self, success, e, score):
        if success:
            score.result += self.value
        else:
            score.result += self.error
            score.fails.append((self, e))

    def evaluateAll(self, e, conditions, score):
        result = 0
        for conditionClass in conditions:
            conditionClass(self.value, self.tolerance, self.error, self.verbose).evaluate(e, score)

    def solveAll(self, e, conditions, score):
        result = 0
        for conditionClass in conditions:
            conditionClass(self.value, self.tolerance, self.error, self.verbose).solve(e, score)

    def __repr__(self):
        return self.__class__.__name__
