# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
# #     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     pagebotapp.py
#
import drawBot

class PageBotApp(object):
    u"""Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self, window):
        self.window = window
