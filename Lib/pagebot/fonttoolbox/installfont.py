#!/usr/bin/env python
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
#     installfont.py
#
import CoreFoundation
import CoreText


def _makeURL(path):
    url = CoreFoundation.CFURLCreateWithFileSystemPath(
        CoreFoundation.kCFAllocatorDefault,
        path,
        CoreFoundation.kCFURLPOSIXPathStyle, False)
    return url


_installScopes = dict(
    none=CoreText.kCTFontManagerScopeNone,
    process=CoreText.kCTFontManagerScopeProcess,
    user=CoreText.kCTFontManagerScopeUser,
    session=CoreText.kCTFontManagerScopeSession,
)

class FontInstallError(Exception): pass


def installFontFile(path, scope="process"):
    assert scope in _installScopes, ("scope must be one of %s" %
            sorted(_installScopes.keys()))
    scope = _installScopes[scope]
    fontURL = _makeURL(path)
    res, error = CoreText.CTFontManagerRegisterFontsForURL(
            fontURL, CoreText.kCTFontManagerScopeProcess, None)
    if error:
        raise FontInstallError(error)


def uninstallFontFile(path, scope="process"):
    assert scope in _installScopes, ("scope must be one of %s" %
            sorted(_installScopes.keys()))
    scope = _installScopes[scope]
    fontURL = _makeURL(path)
    res, error = CoreText.CTFontManagerUnregisterFontsForURL(
        fontURL, CoreText.kCTFontManagerScopeProcess, None)
    if error:
        raise FontInstallError(error)


def _test():
    r"""
        >>> import AppKit
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("Condor-Bold.otf")
        >>> f = AppKit.NSFont.fontWithName_size_("Condor-Bold", 12)
        >>> f is not None
        False
        >>> installFontFile(path)
        >>> f = AppKit.NSFont.fontWithName_size_("Condor-Bold", 12)
        >>> f is not None
        True
        >>> uninstallFontFile(path)
        >>> f = AppKit.NSFont.fontWithName_size_("Condor-Bold", 12)
        >>> #f is not None  # This fails, yet in DrawBot one can see the font no longer works
        False
        >>> path = getFontPath("SaunaPro-RegularItalicMerged.ttf")
        >>> f = AppKit.NSFont.fontWithName_size_(u'-', 12)
        >>> f is not None
        False
        >>> installFontFile(path)
        >>> # If we *don't* test with NSFont here, we see that the uninstall indeed works
        >>> #f = AppKit.NSFont.fontWithName_size_(u'-', 12)
        >>> #f is not None
        True
        >>> uninstallFontFile(path)
        >>> f = AppKit.NSFont.fontWithName_size_(u'-', 12)
        >>> f is not None
        False
    """


def _runDocTests():
    import doctest
    return doctest.testmod()

from pagebot.contexts import defaultContext as c
if __name__ == "__main__":
    if True:
        import sys
        sys.exit(_runDocTests()[0])
    else:
        # Test to be run in DrawBot
        from tnTestFonts import getFontPath
        path = getFontPath("Condor-Bold.otf")
        try:
            installFontFile(path)
        except FontInstallError, error:
            print "font probably already installed"
            #print error
        c.font("Condor-Bold")
        c.fontSize(200)
        c.text("Hallo", (100, 100))
        # uninstallFontFile(path)
