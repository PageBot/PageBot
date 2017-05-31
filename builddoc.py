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
import os, pkgutil, traceback
import sys, getopt
import doctest
import drawBot
import pagebot
from pagebot.publications.publication import Publication

SKIP = ('app', '_export', 'resources', 'pagebotapp', 'contributions', 'OLD',
        'scripts-in-progress', 'examples-in-progress', 'canvas3d',
        'pagebotdoc.py')

CONFIG = 'mkdocs.yml'

class Node(object):
    """The *Node* class is used to build the PageBot file tree, for cleaning
    doc-building and unit tests.

    >>> import pagebot
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
        self.pagebotRoot = pagebot.getRootPath()
        self.pagebotBase = 'src/pagebot'
        self.pagebotDocs = self.pagebotRoot.replace('src', 'docs')
        self.packages = {}
        self.classes = {}
        self.db = dir(drawBot) # TODO: global.

    def buildNode(self, node, level=0):
        print '\t'*level + `node`
        for child in sorted(node.nodes):
            self.build(child, level+1)

    def build(self):
        # Collect data from all folders.
        rootPath = pagebot.getRootPath()
        rootNode = self.docTest(rootPath)
        self.buildNode(rootNode)

    def clearPyc(self, path=None):
        u"""Recursively removes all .pyc files."""
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
                print ' * Removed', filePath
                continue

    def docTest(self, path=None, node=None):
        u"""Calls runpy and doctest.testfile on all .py files in our module.
        """
        if path is None:
            path = self.pagebotRoot

        if node is None:
            node = Node('root')

        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.startswith('.') or fileName in SKIP:
                continue

            child = node.append(filePath)

            if os.path.isdir(filePath):
                self.docTest(filePath, child)

            # Runs tests on all Python files inside out module.
            if filePath.endswith('.py'):
                try:
                    runpy.run_path(filePath)
                    relPath = self.pagebotBase + filePath.split(self.pagebotBase)[-1]
                    d = doctest.testfile(relPath)
                except Exception, e:
                    # TODO: write to file.
                    print 'Found error in file %s' % filePath
                    print traceback.format_exc()

        return node

    def writeDocs(self, m, folder=None, level=0):
        u"""Writes config file including menu, traverses module to parse
        docstrings for all files."""
        self.scanPackage(m)
        print self.classes.keys()
        f = open(CONFIG, 'w')
        f.write('site_name: PageBot\n')
        f.write('repo_url: https://github.com/typenetwork/PageBot/\n')
        f.write('repo_name: PageBot\n')
        f.write('theme: readthedocs\n')
        f.write('pages:\n')
        f.write(" - 'Home': 'index.md'\n")
        f.write(" - 'How To': 'howto.md'\n")
        f.write(" - 'About': 'about.md'\n")
        folders = self.buildDocsMenu(m, f)
        f.close()
        self.writeDocsPages(folders)

    def buildDocsMenu(self, m, yml):
        u"""Extracts menu from module structure."""
        p = m.__path__[0]
        base = p.split('/')
        base = ('/').join(base[:-1]) + '/'
        folders = {}

        for root, dirs, files in os.walk(p):
            parent = folders
            folder = root.replace(base, '')#, dirs, files
            parts = folder.split('/')

            for part in parts:
                if part not in parent:
                    parent[part] = {'files': []}

                parent = parent[part]

            for f in files:
                if f.endswith('.py'):
                    f = f.replace('.py', '')
                    if f == '__init__':
                        f = 'index'
                    parent['files'].append(f)

        self.writeDocsMenu(folders, yml)
        return folders

    def writeDocsMenu(self, folders, yml, level=0):
        u"""Writes the menu structure to YAML config file."""
        indent = '    ' * level

        for k in folders.keys():
            yml.write(" - '%s.md':\n" % k)

            for x in folders[k].keys():
                if x == 'files':
                    for folder in folders[k]['files']:
                        yml.write("    - '%s/%s.md'\n" % (k, folder))
                else:
                    yml.write("    - '%s.md'\n" % x)
                    self.writeDocsMenu({k + '/' + x: folders[k][x]}, yml, level=level)

            level += 1

    def scanPackage(self, m):
        p = m.__path__

        for loader, module_name, is_pkg in pkgutil.walk_packages(p):
            try:
                mod = loader.find_module(module_name).load_module(module_name)

                if is_pkg:
                    self.packages[module_name] = mod
                else:
                    self.classes[module_name] = mod
            except Exception, e:
                print e

    def writeDocsPages(self, folders, level=0):
        u"""Writes a doc page for each item in the menu."""

        for k in sorted(folders.keys()):
            for x in sorted(folders[k].keys()):
                if x == 'files':
                    for f in folders[k]['files']:
                        path = k + '/' + f
                        modName = path.replace('/', '.')
                        modName = modName.replace('index', '__init__')
                        modName = modName.replace('pagebot.', '')
                        if modName in self.classes:
                            mod = self.classes[modName]
                            try:
                                self.writeDocsPage(path, mod)
                            except Exception, e:
                                print e, path
                else:
                    folder = 'docs/' + k + '/' + x

                    if not os.path.exists(folder):
                        os.mkdir(folder)

                    self.writeDocsPages({k + '/' + x: folders[k][x]})

    def writeDocsPage(self, path, m):
        # Module index.
        #f = open('docs/%s/index.md' % m.__name__, 'w')
        f = open('docs/%s.md' % path, 'w')
        f.write('# %s\n' % m.__name__)
        '''
        f.write('## %s\n' % 'Modules')

        for packageName in sorted(packages.keys()):
            mod = packages[packageName]
            if len(packageName.split('.')) == 1:
                f.write('* [%s.%s](%s/%s)\n' % (m.__name__, packageName, m.__name__, packageName.replace('.', '/')))

        f.write('## %s\n' % 'Classes')

        for className in sorted(classes.keys()):
            if len(className.split('.')) == 1:
                mod = classes[className]
                f.write('* [%s.%s](%s/%s)\n' % (m.__name__, className, m.__name__, className.replace('.', '/')))
        '''

        f.write('## %s\n' % 'Functions')

        d = m.__dict__

        for key, value in d.items():
            if key.startswith('__') or key in sys.modules.keys() or key in self.db:
                print ' * skipping %s' % key
                continue

            if value is not None:
                f.write('### %s\n' % key)
                if value.__doc__:
                    s = value.__doc__
                    s = s.strip().replace('    ', '')
                    f.write(u'%s\n' % s)

        f.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ctwh")
    except getopt.GetoptError:
        print 'test.py -c -t -w -h'
        sys.exit(2)

    doClear = False
    doTest = False
    doWrite = False

    for o, _ in opts:
        if o == '-c':
            doClear = True
        if o == '-t':
            doTest = True
        if o == '-w':
            doWrite = True

    d = PageBotDoc()

    if doClear:
        d.clearPyc()
        print 'Cleared .pyc files'

    if doTest:
        import sys
        f = 'log.txt'
        sys.stdout = open(f, 'w', 1)
        d.docTest()
        sys.stdout = sys.__stdout__
        print 'Wrote results to %s' % f


    if doWrite:
        d.writeDocs(pagebot)
        print 'Wrote docs'

if __name__ == '__main__':
    main(sys.argv[1:])
