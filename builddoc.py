#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     builddoc.py
#
#
#    Run through the entire PageBot source tree. Run all .py for unit-test
#    errors.  Create TOC.md and TOC.pdf in every folder, with descriptions of
#    all code in that folder. The docs contains an HTML with all PageBot info.
#
#    If scripts make images in the local gallery folder with the same name as
#    the script, then use that image in the example.
#
import runpy
import os, pkgutil, traceback
from shutil import copyfile
from types import *
import sys, getopt, inspect
import doctest
import pagebot
from pagebot.publications.publication import Publication

try:
    import drawBot
    db = dir(drawBot)
except ImportError:
    db = None

SKIP = ('app', '_export', 'resources', 'pagebotapp', 'contributions', 'OLD',
        'scripts-in-progress', 'examples-in-progress',
        'pagebotdoc.py')
ALLOWED_BUILTINS = ('init', 'repr', 'len', 'getitem', 'setitem')
SKIP_DOCGEN = ['TMP_Xierpa3_builders', 'builders', 'contributions']

CONFIG = 'mkdocs.yml'
DOCS = 'Docs'
INDENT = '    '
NEWLINE = '\n'


class Node:
    """The *Node* class is used to build the PageBot file tree, for cleaning
    doc-building and unit tests.

    >>> import pagebot
    >>> rootPath = pagebot.getRootPath()
    >>> node = Node(rootPath)
    >>> print(node)
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
        self.pagebotBase = 'Lib/pagebot'
        self.pagebotDocs = self.pagebotRoot.replace('Lib', DOCS)
        self.packages = {}
        self.classes = {}
        self.folders = None

    def buildNode(self, node, level=0):
        print('\t'*level + str(node))
        for child in sorted(node.nodes):
            self.build(child, level+1)

    def build(self):
        # Collect data from all folders.
        rootPath = pagebot.getRootPath()
        rootNode = self.testDocs(rootPath)
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
                print(' * Removed %s' % filePath)
                continue

    def testDocs(self, path=None, node=None, logFile=None):
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
                self.testDocs(filePath, child)

            # Runs tests on all Python files inside out module.
            if filePath.endswith('.py'):
                try:
                    runpy.run_path(filePath)
                    relPath = self.pagebotBase + filePath.split(self.pagebotBase)[-1]
                    d = doctest.testfile(relPath)
                except Exception as e:
                    # TODO: write to file.
                    print('doctest: an error occurred, file path is %s' % filePath)
                    print(traceback.format_exc())

        return node

    def scanPackage(self, m):
        u"""Loads modules into packages and classes dictionaries."""
        p = m.__path__
        self.packages['index'] = m

        for loader, module_name, is_pkg in pkgutil.walk_packages(p):
            skip = False

            for substring in SKIP_DOCGEN:
                if substring in module_name:
                    skip = True

            if skip is True:
                continue

            try:
                mod = loader.find_module(module_name).load_module(module_name)

                if is_pkg:
                    self.packages[module_name] = mod
                else:
                    self.classes[module_name] = mod
            except Exception as e:
                print('scanPackage: an error occurred, modulename is %s' % module_name)
                print(traceback.format_exc())

    def writeDocs(self, m, folder=None, level=0, logFile=None):
        """Writes config file including menu, traverses module to parse
        docstrings for all files."""
        self.copyFiles()
        self.scanPackage(m)
        f = open(CONFIG, 'w')
        f.write('site_name: PageBot\n')
        f.write('repo_url: https://github.com/typenetwork/PageBot/\n')
        f.write('repo_name: PageBot\n')
        f.write('theme: readthedocs\n')
        f.write('docs_dir: %s\n' % DOCS)
        f.write('pages:\n')
        f.write(" - 'Home': 'index.md'\n")
        f.write(" - 'How To': 'howto.md'\n")
        #f.write(" - 'About': 'about.md'\n")
        self.folders = self.buildDocsMenu(m, f)
        f.write(" - 'License': 'license.md'\n")
        f.close()
        self.writeDocsPages(self.folders)

    def copyFiles(self):
        u"""Copies hand edited files."""
        copyfile('README.md', '%s/index.md' % DOCS)
        copyfile('LICENSE.md', '%s/license.md' % DOCS)
        copyfile('Examples/Howto/TOC.md', '%s/howto.md' % DOCS)

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
            skip = False

            for skipped in SKIP_DOCGEN:
                if skipped in parts:
                    skip = True

            if skip is True:
                print('skipping %s' % folder)
                continue

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
        #indent = '    ' * level

        for k in folders.keys():
            # Folder header.
            yml.write(" - '%s':\n" % k)

            for x in folders[k].keys():
                # Links to files.
                if x == 'files':
                    for folder in folders[k]['files']:
                        yml.write("    - '%s/%s.md'\n" % (k, folder))
                else:
                    self.writeDocsMenu({k + '/' + x: folders[k][x]}, yml, level=level)

            level += 1

    def writeDocsPages(self, folders, level=0):
        u"""Writes a doc page for each item in the menu."""
        for k in sorted(folders.keys()):
            for x in sorted(folders[k].keys()):
                if x == 'files':
                    # Makes a doc page from a Python file.
                    for f in folders[k][x]:
                        path = k + '/' + f
                        modName = self.path2ModName(path)

                        if modName in self.classes:
                            mod = self.classes[modName]
                        elif modName in self.packages:
                            mod = self.packages[modName]

                        try:
                            self.writeDocsPage(path, mod)
                        except Exception as e:
                            print('WriteDocsPages: an error occurred, path is %s' % path)
                            print(traceback.format_exc())
                else:
                    # Creates new folders if they do not exists yet;
                    # recurse.
                    folder = DOCS + '/' + k + '/' + x

                    if not os.path.exists(folder):
                        os.mkdir(folder)

                    self.writeDocsPages({k + '/' + x: folders[k][x]})

    def writeDocsPage(self, path, m):
        u"""Writes a page for a module."""
        f = open(DOC + '/%s.md' % path, 'w')
        f.write('# %s\n\n' % m.__name__)

        self.writeIndexMenu(f, path, m)
        self.writeDocStrings(f, path, m)

    def getTypeString(self, value):
        u"""Converts the type to a string."""
        t = None

        if isinstance(value, FunctionType):
            t = 'def'
        elif isinstance(value, MethodType):
            t = 'def'
        elif isinstance(value, int):
            t = 'int'
        elif isinstance(value, str):
            t = 'str'
        elif isinstance(value, UnicodeType):
            t = 'unicode'
        elif isinstance(value, dict):
            t = 'dict'
        elif isinstance(value, float):
            t = 'float'
        elif isinstance(value, tuple):
            t = 'tuple'
        elif isinstance(value, list):
            t = 'list'
        elif isinstance(value, set):
            t = 'set'
        elif isinstance(value, ModuleType):
            t = 'module'
        elif isinstance(value, TypeType):
            t = 'class'
        elif isinstance(value, InstanceType):
            t = 'instance'
        elif isinstance(value, property):
            t = 'property'
        elif isinstance(value, NoneType):
            pass
        else:
            t = str(type(value))
            t = t.replace("<type '", '')
            t = t.replace("<class '", '')
            t = t.replace("'>", '')

        return t

    def writeDocStrings(self, f, path, m):
        u"""Writes docstring contents for all classes in the file."""
        for key, value in inspect.getmembers(m):
            self.writeDocString(f, key, value)

        f.close()

    def inIgnores(self, key):
        if key.startswith('__'):
            return key.replace('__', '') not in ALLOWED_BUILTINS
        elif key.startswith('NS'):
            return True
        elif key in sys.modules.keys():
            return True
        elif key in db:
            return True
        else:
            return False

    def writeDocString(self, f, key, value, level=0):
        if level > 1:
            return

        if self.inIgnores(key):
            return

        t = self.getTypeString(value)
        t1 = key.replace('_', '\_')
        argString = None

        if t == 'def':
            extra = False
            args, varargs, kwargs, defaults = inspect.getargspec(value)
            argString = '('

            if varargs is not None or kwargs is not None:
                extra = True

            if defaults is not None:
                diff = len(args) - len(defaults)

                for i in range(0, diff):
                    if i == len(args) - 1 and not extra:
                        argString += '%s)' % args[i]
                    else:
                        argString += '%s, ' % args[i]

                j = 0

                for i in range(diff, len(args)):
                    if i == len(args) - 1 and not extra:
                        argString += '%s=%s)' % (args[i], defaults[j])
                    else:
                        argString += '%s=%s, ' % (args[i], defaults[j])
                    j += 1
            else:
                for i in range(len(args)):
                    if i == len(args) - 1 and not extra:
                        argString += '%s)' % args[i]
                    else:
                        argString += '%s, ' % args[i]

            if varargs is not None and kwargs is None:
                argString += '*args)'
            elif varargs is not None:
                argString += '\*args, '

            if kwargs is not None:
                argString += '\*\*kwargs)'

            if argString == '(':
                argString += ')'

        if argString:
            t1 = t1 + argString

        if t:
            t = t.replace('_', '\_')
            title = '### %s %s\n' % (t, t1)
        else:
            title = '### %s\n' % t1

        f.write(title)

        if value is not None:
            if '__doc__' in dir(value):
                s = value.__doc__
                if s is None:
                    return

                s = s.strip().replace('    ', '')
                lines = s.split('\n')
                isDocTest = False

                for line in lines:
                    if line.startswith('>>>'):
                        line = INDENT + line

                        if not isDocTest:
                            line = NEWLINE + line

                        isDocTest = True
                    else:
                        if isDocTest:
                            line = INDENT + line
                            isDocTest = False

                    try:
                        f.write('%s  \n' % line.encode('utf-8'))
                    except Exception as e:
                        print('An error occurred writing a doc file %s, (%s %s)' % (f, key, value))
                        print(traceback.format_exc())

        if isinstance(value, TypeType):
            level += 1
            for k, v in inspect.getmembers(value):
                self.writeDocString(f, k, v, level=level)


    def writeIndexMenu(self, f, path, m):
        u"""If index (__init__.py), writes links to class files and
        submodules.

        """

        if path.endswith('index'):
            folders = self.getFolderContents(path)

            if 'files' in folders:
                f.write('## %s\n\n' % 'Related Classes')
                v = folders['files']

                for x in v:
                    if x == 'index':
                        continue

                    n = m.__name__

                    if not n.startswith('pagebot'):
                        n = 'pagebot.' + n

                    n = '%s.%s' % (n, x)
                    f.write('* [%s](%s)\n' % (n, x))

            hasModules = False

            if 'files' in folders:
                if len(folders) > 1:
                    hasModules = True
            else:
                if len(folders) > 0:
                    hasModules = True

            if hasModules:
                f.write('\n## %s\n\n' % 'Related Modules')

                for k, v in folders.items():
                    if k != 'files':
                        n = m.__name__

                        if not n.startswith('pagebot'):
                            n = 'pagebot.' + n

                        n = '%s.%s' % (n, k)
                        f.write('* [%s](%s)\n' % (n, k))
            else:
                f.write(NEWLINE)

    def path2ModName(self, path):
        modName = path.replace('/', '.')
        modName = modName.replace('pagebot.', '')
        return modName.replace('.index', '')

    def getFolderContents(self, path):
        u"""Returns names of files and folders."""
        parts = path.split('/')[:-1]
        folders = self.folders

        for part in parts:
            if part in folders:
                folders = folders[part]

        return folders

def printOpts():
    print('./builddoc.py -ctwho')
    print('-h, --help: prints this listing.')
    print('-c, --clear: clears .pyc files.')
    print('-w, --write: writes the markdown files to the doc folder.')
    print('-d, --doctest: runs doctests on the pagebot module and HowTo files.')
    print('-l, --log: outputs to log, takes log file name as argument.')

def main(argv):
    fileName = 'log.txt'
    clearOpts = ('-c', '--clear')
    testOpts = ('-d', '--doctest')
    writeOpts = ('-w', '--write')
    helpOpts = ('-h', '--help')
    logOpts = ('-l', '--log')
    doClear = False
    doTest = False
    doWrite = False
    logFile = None

    try:
        opts, args = getopt.getopt(argv, "cdwhl:", ['clear', 'doctest', 'write', 'help', 'log='])
    except getopt.GetoptError('missing arguments'):
        printOpts()
        sys.exit(2)

    if len(opts) == 0:
        printOpts()
        return

    for o, v in opts:
        if o in helpOpts:
            printOpts()
        if o in clearOpts:
            doClear = True
        if o in testOpts:
            doTest = True
        if o in writeOpts:
            doWrite = True
        if o in logOpts:
            fileName = v
            logFile = open(fileName, 'w', 1)

    d = PageBotDoc()

    if doClear:
        d.clearPyc()
        print('Cleared .pyc files')

    if doWrite:
        d.writeDocs(pagebot, logFile=logFile)
        print('Wrote docs')

    if doTest:
        try:
            d.testDocs(logFile=logFile)
        except Exception as e:
            traceback.format_exc()

if __name__ == '__main__':
    main(sys.argv[1:])
