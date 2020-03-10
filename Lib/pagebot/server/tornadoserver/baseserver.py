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
#     BaseServer.py
#
#     Using: https://www.tornadoweb.org
#
#     Testing available parameters on the url page call.
#     This example server shows how different paths (detected by regular expressions)
#     are connected to different handlers, ranging from a simple request, reading a static
#     html page file, getting specific URL arguments (http://localhost:8886/query/aaa?n=100)
#     or disassembling the URL path by regular expressions.
#     This means that "parts" of the site can use different handlers than other parts.
#
#     http://localhost:8888
#     http://localhost:8888/blog
#     http://localhost:8888/query?n=100
#     http://localhost:8888/query/aaa?n=100
#     http://localhost:8888/resource/1234
#     http://localhost:8888/resource/abcd-200/xyz-100/page.html

import os
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

from pagebot.constants import ALL_FILE_TYPES
from pagebot.toolbox.transformer import asIntOrValue

class RequestData:
    """Answer data instance that holds parsed request data from url/path.
    There are two types of arguments that can be mixed:
    The traditional format: /a/b/c/d.html?c=100
    And format where parameters are embedded as "directory names": /a/b/c-100/d.html

    >>> rd = RequestData('/a/b/c/d') # path with implicit index.html
    >>> rd.path
    '/a/b/c/d/index.html'
    >>> rd.filePath
    'index.html'
    >>> rd.dirPath
    '/a/b/c/d'
    >>> rd.dirs # Unchanged "directory" path
    ['', 'a', 'b', 'c', 'd']
    >>> rd.args # No arguments in the path
    {}

    >>> rd = RequestData('/a/b/c/d.html') # Explicit file path
    >>> rd.path
    '/a/b/c/d.html'
    >>> rd.filePath
    'd.html'
    >>> rd.dirPath
    '/a/b/c'
    >>> rd.dirs
    ['', 'a', 'b', 'c', 'd.html']

    >>> rd = RequestData('/a/b/c/d.jpg')
    >>> rd.path
    '/a/b/c/d.jpg'
    >>> rd.filePath
    'd.jpg'

    >>> rd = RequestData('/a/b/c/d.pdf')
    >>> rd.path
    '/a/b/c/d.pdf'
    >>> rd.filePath
    'd.pdf'

    >>> rd = RequestData('/a/b/c-xyz/c-100/d.html') # Filter path parameters, converted to int.
    >>> rd.path
    '/a/b/d.html'
    >>> rd.filePath
    'd.html'
    >>> rd.args # Args can have mutiple values, in order of path
    {'c': ['xyz', 100]}

    >>> rd = RequestData('/a/b/c/d.html?e=100&e=xyz') # Filter path parameters, converted to int.
    >>> rd.path
    '/a/b/c/d.html'
    >>> rd.filePath
    'd.html'
    >>> rd.args # Args can have mutiple values, in order of path
    {'e': [100, 'xyz']}

    >>> rd = RequestData('/a/b/c-100/c-/d.html?c=200&c=xyz&c') # Mixing parameter types.
    >>> rd.path
    '/a/b/d.html'
    >>> rd.filePath
    'd.html'
    >>> rd.args # Args can have mutiple values, in order of path
    {'c': [100, 1, 200, 'xyz', 1]}
    """
    INDEX_HTML = 'index.html' # Default file path

    def __init__(self, uri):

        self.uri = uri
        self.dirs = [] # List of "dictionaries", in url/path order
        self.args = {}

        queryPaths = uri.split('?')
        mainPathParts = queryPaths[0].split('/')
        for part in mainPathParts:
            if '-' in part:
                argKey = part.split('-')[0]
                argValue = '-'.join(part.split('-')[1:])
                if not argValue: # In case of /a/b/c-/d, default is 1
                    argValue = 1
                if not argKey in self.args:
                    self.args[argKey] = []
                self.args[argKey].append(asIntOrValue(argValue))
            else:
                self.dirs.append(part)
        if len(queryPaths) > 1:
            for queryPath in queryPaths[1:]:
                for queryPart in queryPath.split('&'):
                    queryKeyValue = queryPart.split('=')
                    queryKey = queryKeyValue[0]
                    if len(queryKeyValue) == 1:
                        queryValue = 1
                    else:
                        queryValue = '='.join(queryKeyValue[1:])
                    if not queryKey in self.args:
                        self.args[queryKey] = []
                    self.args[queryKey].append(asIntOrValue(queryValue))

    def __repr__(self):
        return '<%s uri=%s>' % (self.__class__.__name__, self.uri)
        
    def _get_path(self):
        path = '/'.join(self.dirs)
        # Test on valid extension
        if not self.dirs[-1].split('.')[-1].lower() in ALL_FILE_TYPES:
            path += '/' + self.INDEX_HTML
        return path
    path = property(_get_path)

    def _get_filePath(self):
        return self.path.split('/')[-1]
    filePath = property(_get_filePath)

    def _get_dirPath(self):
        return '/'.join(self.path.split('/')[:-1])
    dirPath = property(_get_dirPath)

    def _get_fileExists(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]
        return os.path.exists(path)
    fileExists = property(_get_fileExists)

class BasicRequestHandler(RequestHandler):

    def get(self, *args):
        """Figure out how or handle the request and where to get content from.
        """
        #print('=====', self.request)
        #print('+++++', self.path_args)
        #print('-----', self.request.host)
        #print('#####', self.path_kwargs)
        requestData = RequestData(self.request.uri) # Split path parts and arguments
        self.write('<h1>Hello, world</h1>')
        self.write('<h2>%s</h2>' % self.request.host)
        self.write('<h3>%s</h3>' % self.request)
        self.write('<h3>%s</h3>' % self.request.__dict__)
        self.write('requestData.uri: %s' % str(requestData.uri))
        self.write('<br>')
        self.write('requestData.dirs: %s' % str(requestData.dirs))
        self.write('<br>')
        self.write('requestData.filePath: %s' % requestData.filePath)
        self.write('<br>')
        self.write('requestData.dirPath: %s' % requestData.dirPath)
        self.write('<br>')
        self.write('requestData.path: %s' % requestData.path)
        self.write('<br>')
        self.write('requestData.args: %s' % str(requestData.args))
        self.write('<br>')
        self.write('requestData.fileExists: %s' % str(requestData.fileExists))

    def data_received(self):
        pass

"""
class StaticRequestHandler(RequestHandler):
    def get(self):
        self.render('templates_html/index.html')

class QueryRequestHandler(RequestHandler):
    def get(self):
        n = self.get_argument('n')
        self.write('Argument is "%s"' % n)

class ResourceRequestHandler(RequestHandler):
    def get(self, id):
        self.write('<h2>Querying path with id "%s"</h2>' % id)

class PathRequestHandler(RequestHandler):
    def get(self, *args):
        for arg in args:
            self.write('<h2>Querying path item "%s"</h2>' % arg)
"""
class BaseServer:
    PORT = 8895
    REQUEST_HANDLERS = [('/(.*)', BasicRequestHandler)]

    def __init__(self, requestHandlers=None, publication=None, port=None):
        if requestHandlers is None:
            requestHandlers = self.getRequestHandlers() # http://localhost:8889/<args>
        self.requestHandlers = requestHandlers
        self.publication = publication # PageBot Publication instance, e.g, Website
        self.port = port or self.PORT

    def getRequestHandlers(self):
        return self.REQUEST_HANDLERS

    def run(self, port=None):
        app = Application(self.requestHandlers)
        app.listen(self.port)
        print('Start server %s on port %d' % (self.__class__.__name__, self.port))
        IOLoop.current().start()

    def stop(self):
        print('Stop server %s on port %d' % (self.__class__.__name__, self.port))
        IOLoop.current().stop()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    server = BaseServer(port=8990)
    server.run()
