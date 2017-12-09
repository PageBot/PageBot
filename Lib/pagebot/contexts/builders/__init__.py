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
from drawbotbuilder import drawBotBuilder # Instance with functions, not a class
from flatbuilder import flatBuilder # Instance with functions, not a class
# Future alternative builders? https://skia.org

from basebuilder import BaseBuilder
from xmlbuilder import XmlBuilder
from htmlbuilder import HtmlBuilder
from webbuilder import WebBuilder

from buildinfo import BuildInfo # Container with builder flags.

# Future developments Python --> JS ??
#
# http://stromberg.dnsalias.org/~strombrg/pybrowser/python-browser.html
# http://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html
# https://www.nativescript.org/nativescript-example-application?utm_medium=referral&utm_source=documentation&utm_campaign=getting-started
# http://pyjs.org
# http://www.infoworld.com/article/3033047/javascript/4-tools-to-convert-python-to-javascript-and-back-again.html
# 