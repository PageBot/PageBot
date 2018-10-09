#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#    02_Sass.py
#

from pagebot import getResourcesPath
import shutil

def testSass():
    import sass

    # Testing Sass.
    css = sass.compile(string='a { b { color: blue; } }')
    print(css)
    path = getResourcesPath() + '/templates/test.scss'
    import os.path
    print(os.path.exists(path))
    css = sass.compile(filename=path)
    print(css)

    #test_scss = open('test.scss', 'w')
    import os, os.path

    for f in ('css', 'sass'):
        if not os.path.exists(f):
            os.mkdir(f)
    shutil.copy(path, 'sass')
    sass.compile(dirname=('sass', 'css'), output_style='compressed')
    with open('css/test.css') as example_css:
        print(example_css)

    # Export with HtmlBuilder.
    from pagebot.contexts.builders.htmlbuilder import HtmlBuilder
    hb = HtmlBuilder()
    print(hb)
    hb.compileScss(path, cssPath = 'css/testHtmlBuilder.css')

testSass()
