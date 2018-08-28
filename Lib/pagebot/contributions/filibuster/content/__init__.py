# -*- coding: UTF-8 -*-
#
"""
        history
        This is the init code for the Content package.
        No user servicable parts inside.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'contexnt' allowed per module
        this limitation is to speed up loading
4.0    - changes due to the fact that Content is now a submodule of the
        new ContentWriter package. (jvr)
4.0     2016 public release
"""

import glob
import os, string
import traceback

_version__ = '4.0'

#__path__ == __file__ #@NoEffect


DEBUG=1

_contentCache = None


def clearCache():
    global _contentCache
    _contentCache = None


def content():
    """Return one dictionary that contains all dictionaries of the
    module. By making a function rather than part of the namespace,
    the content can be updated dynamically. Should not make any
    difference in speed for normal use."""

    global _contentCache

    if _contentCache is not None:
        return _contentCache

    # import each time by looking at the files
    mods = glob.glob1(__path__[0], '*.py')
    _contentCache = content = {}

    for m in mods:
        if m[:2] == '__':
            continue
        modname = __name__ + '.' + m[:-3]
        path = modname.split('.')
        module = __import__(modname)
        # find the deepest submodule
        for modname in path[1:]:
            module = getattr(module, modname)
        if hasattr(module, 'content'):
            content.update(module.content)
            continue
        else:
            if DEBUG:
                print(__name__, 'submodule ', module, 'misses a content dictionary.')
    return content

def index(tagname):
    """Return the name of the submodule that tagname is defined in,
    as well as a list of modules and keys in which this tagname is used."""
    mods = glob.glob1(__path__[0], '*.py')
    keys = []
    usedin = {}

    for m in mods:
        if m[:2] == '__':
            continue
        modname = __name__ + '.' + m[:-3]
        path = modname.split('.')
        module = __import__(modname)

        # find the deepest submodule
        for modname in path[1:]:
            try:
                module = getattr(module, modname)
            except Exception as e:
                print('Could not import module at path, %s, mod %s, name %s' % (path, module, modname))
                traceback.format_exc()
                return

        if hasattr(module, 'content'):
            c = module.content
            for k in c.keys():
                if k == tagname:
                    keys.append(m)
                for item in c[k]:
                    if string.find(item, tagname) !=  -1:
                        usedin[(m, k)] = 1
    return keys, usedin.keys()

#if __name__ == "__main__":
#    print(content())

