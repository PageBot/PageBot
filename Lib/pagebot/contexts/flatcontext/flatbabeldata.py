#!/usr/bin/env python3
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
#     flatbabeldata.py
#
import flat

class FlatBabelData:
    """Class to store cached information in BabelString._cs."""

    def __init__(self, doc, page, paragraphs, runs):
        self.doc = doc # Flat.document instance
        self.page = page # Flat.page instance
        self.paragraphs = paragraphs
        self.txt = flat.text(paragraphs)
        self.pt = page.place(self.txt) # Flat.placedText instance
        self.runs = runs # List of FlatRunData instances
    def __repr__(self):
        spans = [span.string for p in self.paragraphs for span in p.spans]
        # Show plain string accumulate string, compatible to DrawBotFormattedString
        return ' '.join(spans)
