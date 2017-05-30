#!/usr/bin/python
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     builddoc.py
#
#
#    Run through the entire PageBot source tree. Run all .py for unit-test errors.
#    Create TOC.md and TOC.pdf in every folder, with descriptions of all code in
#    that folder. The docs contains an HTML with all PageBot info.
#    If scripts make images in the local gallery folder with the same name as the
#    script, then use that image in the example.
#    Note that this applications script is an example of PageBot functions in itself.
#
import runpy

import os, pkgutil
import pagebot
from pagebot.publications.publication import Publication

SKIP = ('app', '_export', 'resources', 'pagebotapp', 'contributions', 'OLD', 'scripts-in-progress',
    'examples-in-progress', 'canvas3d', 'pagebotdoc.py')

class Node(object):
    """The *Node* class is used to build the PageBot file tree, for cleaning doc-building
    and unit tests.

    >>> improt pagebot
    >>> rootPath = pagebot.getRootPath()
    >>> node = Node(rootPath)
    >>> print node
    """
    def __init__(self, path=None):
        self.path = path
        self.nodes = []
        extension = None
        if path is not None and not os.path.isdir(path):
            extension = path.split('.')[-1]
        self.extension = extension # If filled, it's a folder. otherwise it's a file.

    def __repr__(self):
        return self.path

    def append(self, path):
        node = Node(path)
        self.nodes.append(node)
        return node

    def __eq__(self, node):
        return self.path == node.path

    def __ne__(self, node):
        return self.path != node.path

    def __le__(self, node):
        return self.path <= node.path

    def __lt__(self, node):
        return self.path < node.path

    def __ge__(self, node):
        return self.path >= node.path

    def __gt__(self, node):
        return self.path > node.path

class PageBotDoc(Publication):

    def __init__(self):
        Publication.__init__(self)

    def buildNode(self, node, level=0):
        print '\t'*level + `node`
        for child in sorted(node.nodes):
            self.build(child, level+1)

    def build(self):
        # Collect data from all folders.
        rootPath = pagebot.getRootPath()
        rootNode = self.processPath(rootPath)
        self.buildNode(rootNode)

    def clearPyc(self, path=None):
        if path is None:
            path = pagebot.getRootPath()
        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.startswith('.') or fileName in SKIP:
                continue
            if os.path.isdir(filePath):
                self.clearPyc(filePath)
            elif fileName.endswith('.pyc'):
                os.remove(filePath)
                print '#### Removed', filePath
                continue

    def processPath(self, path=None, node=None):
        if path is None:
            path = pagebot.getRootPath()
        if node is None:
            node = Node('root')

        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.startswith('.') or fileName in SKIP:
                continue
            child = node.append(filePath)
            if os.path.isdir(filePath):
                self.processPath(filePath, child)
            if filePath.endswith('.py'):
                try:
                    runpy.run_path(filePath)
                except:
                    print 'Run', filePath
                    runpy.run_path(filePath)

        return node

    def writeModuleDoc(self, m, folder=None, level=0):
        u"""
        TODO: maybe sort (global variables, global functions, hidden
        functions).
        """
        import sys, drawBot

        if hasattr(m, '__path__'):
            print 'path', m.__path__
        elif hasattr(m, '__file__'):
            print 'file', m.__file__
        else:
            print 'no path or file'

        try:
            p = m.__path__
        except Exception, e:
            #print 'cannot find path', m
            #print dir(m)
            #print m.__file__
            return

        d = m.__dict__
        db = dir(drawBot)
        submodules = {}

        if level > 2:
            return

        for loader, module_name, is_pkg in  pkgutil.walk_packages(p):
            try:
                mod = loader.find_module(module_name).load_module(module_name)
                submodules[module_name] = mod

            except Exception, e:
                print e, loader

        print folder

        if level == 0:
            f = open('docs/%s.md' % m.__name__, 'w')

            f.write('# %s\n' % m.__name__)

            for module_name in submodules:
                f.write('* [%s](%s/%s)\n' % (module_name, m.__name__, module_name))

            for key, value in d.items():
                if key.startswith('__') or key in sys.modules.keys() or key in db:
                    print ' * skipping %s' % key
                    continue

                if value is not None:
                    f.write('## %s\n' % key)
                    if value.__doc__:
                        s = value.__doc__
                        s = s.strip().replace('    ', '')
                        f.write('%s\n' % s)

            f.close()

        for modname, mod in submodules.items():
            if folder is None:
                f = m.__name__ + '/' + modname
            else:
                f = folder + '/' + modname
            self.writeModuleDoc(mod, folder=f, level=level+1)





# TODO: pass as argument.
DO_CLEAR = False
CHECK_ERRORS = False
RUN_MODULES = True
DOCTEST = True

if __name__ == '__main__':
    # Execute all cleaning, docbuilding and unittesting here.
    pbDoc = PageBotDoc()

    if DO_CLEAR:
        pbDoc.clearPyc()

    if CHECK_ERRORS:
        pbDoc.processPath()

    if RUN_MODULES:
        pbDoc.writeModuleDoc(pagebot)

    print 'Done'

