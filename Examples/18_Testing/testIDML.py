#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testIDML.py
#
# Test InDesign Markup Language.
#
import traceback
from pagebot import getResourcesPath

IDML = False

try:
    from simple_idml import idml
    IDML = True
except:
    print(traceback.format_exc())

def testIDML():
    path = getResourcesPath() + "/templates/test.idml"
    pkg = idml.IDMLPackage(path)
    print(pkg.font_families)
    l = [e.get("Name") for e in pkg.font_families]
    print(l)
    print(pkg.spreads)
    print(pkg.stories)
    xml = pkg.xml_structure
    from lxml import etree
    s = etree.tostring(xml, pretty_print=True)
    print(s)

    #with pkg.prefix("main") as f:


if IDML:
    testIDML()

