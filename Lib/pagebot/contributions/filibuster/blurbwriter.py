# coding: UTF-8

import re
import random
from pagebot.contributions.filibuster.titlecase import titlecase

choice = random.choice


"""
26 12 99         added support for 'article' in tags:
            'this_demonstrates_articles':    ['<#article, demo_fruit#>'],
            'demo_fruit':    ['pear', 'apple', 'olive']
            #a pear
            #an apple
            #a pear
            #an olive

30 12 99         fixed replacecode - now it will interpret identical tags in one line individually

4 jan 99        added support for inline style references
            <#!bold, company#>    will label this for bold, it depends on the styledict
                                how it is formatted in the end
            <#!bold, !uppercase, company#> - multiple styles should be possible as well, no?
            in theory yes, but somehow netscape doesn't draw the uppercase - odd?
            - tag = name of an entry from the Content module
            - formatdict is a dictionary in which style
                commands that are used in Content are mapped
                to any arbitrary outside defined stylename.
                This is to prevent pollution from outside formatting stuff
                in the content module.
                For instance, a content tag can say <#!bold, company#>
                the formatdict can look like this: {'bold':    'CSS_my_specific_bold'}
                If the style cmd from the tag can be found in the provided formatdict
                format func is used to format the final resulting text.
                    def formatfunc(text, tagname)
                This means that Writer and Content should also be able to be used
                to make RTF, or any other kind of formatted text without making
                the modules specific to any kind of format, or platform.


3.0            added support for the Content package, added some UI
17 1 2000

3.1            Writer can now handle nested tags, opening a whole world of metaprogramming
evb

3.2            messed with the caching mechanism
evb

3.3            now the write() method also accepts tagged entries, simpler code, more flexible
evb            w.write('<#name#>') and w.write('name') have the same results

3.4            added simpler support for initial capitals. Write '<#^,word#> for a capital of the first letter
evb

4.0             Removed string module import. Added some tests.
"""

__version__ = '4.0'

opentag = '<#'
closetag = '#>'

DEBUG = 0

# filter tabs, newline, returns, double spaces, but leave single spaces.
FILTERWHITESPACE = 1

randint = random.randint
vowels = 'aeiuoAEIUO'

class BlurbWriter:

    '''A very unspecific recursive compiler and randomizer for text.
    '''

    def __init__(self, content, debug=False):
        self.DEBUG = debug
        self.data = {}
        self._cache = {}
        self.formatdict = None
        self.formatfunc = None
        self.lasttag = 'no last tag'    # last processed tag, useful when debugging loops
        self.choicetree = []
        p = '\<#(?P<tagname>.*)#\>'
        #p = '\<#(?P<tagname>.*?)#\>'
        self.tag = re.compile(p, re.IGNORECASE)
        p = '\<-(?P<tagname>.*?)-\>'
        self.pstatement = re.compile(p, re.IGNORECASE)
        self.allkeys = self.keys()

        self.importcontent(content)

    def importcontentPy2(self, contentdict):
        '''make all strings unicode here?'''
        for k, v in contentdict.items():
            self.data[k] = [name for name in v]

        dk = list(self.data.keys())
        dk.sort()
        self.keywords = dk

    def importcontent(self, contentdict):
        for k, v in contentdict.items():
            bb = []

            for name in v:
                bb.append(name)

            self.data[k] = [name for name in v]

        dk = list(self.data.keys())
        dk.sort()
        self.keywords = dk

    def keyindex(self, key):
        if key in self.allkeys:
            return list(self.allkeys).index(key)
        else:
            return -1

    def keys(self):
        k = list(self.data.keys())
        #return k.sort()
        return self.data.keys()

    def has_key(self, key):
        if key in self._cache:
            return 1
        if key in self.data:
            return 1
        return 0

    def alternatives(self, key):
        return self[key]

    def choice(self, cached, key):
        if self.has_key(cached):
            return 1, self[cached][0]
        items = self[key]
        if items:
            i = randint(0, len(items)-1)
            self.choicetree.append((self.keyindex(key), i))
            return i, items[i]
        else:
            self.choicetree.append((-1, -1))
            return -1, ''

    def getvalue(self, key):
        return self[key]

    def __getitem__(self, key):
        if key in self._cache:
            return self._cache[key]
        if key in self.data:
            return self.data[key]
        return '__' + key + '__'

    def define(self, key, value):
        if DEBUG:
            print('hard define', key, value)
        self._cache[key] = [value]

    def softdefine(self, key, value):
        if DEBUG:
            print('soft define', key, value)
        if not key in self._cache:
            self._cache[key] = [value]

    def clearcache(self, key=None):
        if not key:
            self._cache = {}
        else:
            if key in self._cache:
                del self._cache[key]

    def parsetag(self, tag):
        hard=0
        # check for styles
        parts = tag.split(',')
        if len(parts)>1:
            name = parts[-1].strip()
            cmd = parts[0:-1]
            variable = None
            return name, cmd, variable, hard
        # check for hard definition
        parts = tag.split('=')
        if len(parts)>1:
            hard = 1
            name = parts[-1].strip()
            cmd = []
            variable = u"".join(parts[0:-1]).strip()
            return name, cmd, variable, hard
        # check for soft definition
        parts = tag.split(':')
        if len(parts)>1:
            hard=0
            name = parts[-1].strip()
            cmd = []
            variable = ''.join(parts[0:-1]).strip()
            return name, cmd, variable, hard
        # rest
        else:
            hard=0
            name = tag.strip()
            cmd = []
            variable = None
            return name, cmd, variable, hard

    def write(self, tag, formatdict=None, formatfunc=None):
        '''this assumes tag to be a direct entry in content'''
        return self.writetag(opentag+tag+closetag, formatdict, formatfunc)

    def writetag(self, tag, formatdict=None, formatfunc=None):
        '''this will evaluate tag directly, use writetag if you want to more tags in one line to be processed.
        this is the main interface to the writer class'''
        self.allkeys = self.keys()
        self.choicetree = []
        if not formatdict:
            self.formatdict = {}
        else:
            self.formatdict = formatdict
        self.formatfunc = formatfunc
        _, item = self.replacetag(0, tag) # ok, item
        _, item = self.replacecode(item) # ok, item
        if FILTERWHITESPACE:
            return ' '.join(item.split())
        return item

    def replacecode(self, text):
        m = 1
        pend= 0
        while m != None:
            m = self.pstatement.search(text, pend)
            if m == None:
                return 0, text
            tag = m.group('tagname')
            if not tag:
                raise 'Error in blurb code' # Better make it crash to show the error
                return 0, '__empty tag__'
            try:
                result = eval(tag)
            except:
                result = '__error('+tag+')__'
            if not isinstance(result, str):
                result = str(result)
            parts = text.split('<-' + tag + '->')
            text = parts[0] + result + ('<-' + tag + '->').join(parts[1:])
        return 1, text

    def capsentence(self, s):
        ss = s.split('. ')
        new = []
        for i in ss:
            new.append(i[0].upper() + i[1:])
        return new.join('. ')

    def nextopen(self, pos, text):
        return text.find(opentag, pos)

    def nextclosed(self, pos, text):
        return text.find(closetag, pos)

    def nexttag(self, pos, text):
        start = self.nextopen(pos, text)
        stop = self.nextclosed(pos, text)
        if start == -1:
            if stop == -1:
                return -1, -1
            return 0, stop
        if start < stop and start != -1:
            return 1, start
        else:
            return 0, stop

    def findtag(self, text):
        p = -1
        last = None,None
        spinning = 0
        while 1:
            spinning += 1
            if spinning > 1000:
                if self.DEBUG:
                    print("spinning", text)
                return None, None
            kind, p = self.nexttag(p+1, text)
            if last[0]==1 and kind==0:
                if self.DEBUG:
                    print(text[last[1]+len(opentag): p])
                return last[1]+len(opentag), p
            if (kind, p) == (-1, -1):
                break
            last=kind, p
        return None, None

    def replacetag(self, level, text):
        level = level + 1
        if level > 100:
            raise('Blurbwriter.replacetag: Recursion error? too many nested instructions! last tag: %s' % self.lasttag)
        #pend = 0
        m = 1
        while m != None:
            start, stop = self.findtag(text)
            if start == None:
                return 0, text
            tag = text[start:stop]
            if not tag:
                raise 'Blurbwriter.replacetag: Error in blurb code' # Better make it crash to show the error
                return 0, '__empty tag__'

            # do the meta-recursive tag-tagging thing here
            metatext = text
            metatag = tag
            while tag.find(opentag) != -1:
                _, metatag = self.replacetag(level, tag) # ok, metalog
                parts = metatext.split(tag)
                if len(parts) > 1:
                    tag = parts.join(metatag)
                else:
                    tag = metatag
                return self.replacetag(level, tag)

            tagname, cmd, variable, hard = self.parsetag(tag)
            # process in-tag commands, if any
            cacheThis = False    # whether results should be cached
            setArticle = False    # prepare an article ( 'a' or 'an' )
            makeUpperCase = False    # make first character uppercase
            makeTitleCase = False   # makeTitlecase
            makeAllCaps = False      # make all caps
            makeLowercase = False     # make all characters lowercase
            space_to_underscore = False # convert spaces to underscores
            nonletter_remove = False    # remove whitespace
            formatcmds = []
            for i in cmd:
                si = i.strip()
                #print('si', si)
                if not si:
                    continue
                if 'article' in si:
                    setArticle = True
                if '!' in si:        # it's a format command!
                    formatcmds.append(si[1:])
                if '^' in si:        # make first character uppercase
                    capped = si.count(u"^")
                    if capped == 1:
                        makeUpperCase = True
                    elif capped == 2:
                        makeTitleCase = True
                    elif capped == 3:
                        makeAllCaps = True
                if '~' in si:        # make first character uppercase
                    makeLowercase = True
                if '_' in si :        # make whitespace underscore
                    space_to_underscore = True
                if '@' in si :        # remove whitespace
                    nonletter_remove = True

            parts = text.split(opentag + tag + closetag)
            if self.has_key(tagname):
                _, selection = self.choice(variable, tagname) # ci, selection
                _, c = self.replacetag(level, selection) # ok, c
            else:
                _, c = self.replacetag(level, '__' + tagname + '__') # ok, c
            self.lasttag = c

            # take care of the article command
            art = ''
            if c:
                if setArticle:
                    if c[0] in vowels:
                        art = 'an '
                    else:
                        art = 'a '
                if makeUpperCase:
                    c = c[0].upper()+c[1:]
                elif makeTitleCase:
                    c = titlecase(c)
                elif makeAllCaps:
                    c = c.upper()
                elif makeLowercase:
                    c = c.lower()
                if nonletter_remove:
                    #print('before', c)
                    c = c.replace(u" ", u"")
                    c = c.replace(u".", u"")
                    c = c.replace(u"-", u"")
                    c = c.replace(u"_", u"")
                    #print('after', c)
                elif space_to_underscore:
                    c = c.replace(u" ", u"_")

            #print('cacheThis', cacheThis, 'makeUpperCase', makeUpperCase, 'makeLowercase', makeLowercase, 'space_to_underscore', space_to_underscore, 'nonletter_remove', nonletter_remove)

            # format the line if necessary
            if formatcmds and self.formatfunc:
                for fc in formatcmds:
                    if DEBUG:
                        print('writerformatting before:', fc, c)
                    if not fc in self.formatdict:
                        continue
                    c = self.formatfunc(c, self.formatdict[fc])
                    if DEBUG:
                        print('writerformatting after:', fc, c)

            # build the new line
            vardef = c
            if variable:
                c = ''
            try:
                text = parts[0] + art + c + (opentag + tag + closetag).join(parts[1:])
            except:
                print('Hm, a problem occurred. Nested quite deep, I think should just stop. Sorry!')
                return 0, text
            # store the result in the cache
            # note: it is storing the stylised version
            if variable or cacheThis:
                if variable:
                    tg = variable
                else:
                    tg = tagname
                if hard:
                    self.define(tg, vardef)
                else:
                    self.softdefine(tg, vardef)
        return 0, text


def test():
    u"""
    >>> # replace a single tag
    >>> content = { 'pattern1': ['a']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern1')
    'a'

    >>> # replace a tag
    >>> content = { 'pattern2': ['a'], 'pattern1': ['<#pattern2#>']}
    >>> bw = BlurbWriter(content)

    >>> bw.write('pattern2')
    'a'
    >>> bw.write('pattern1')
    'a'

    >>> # to lowercasee
    >>> content = { 'pattern2': ['AA'], 'pattern1': ['<#~,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'AA'
    >>> bw.write('pattern1')
    'aa'

    >>> # white space to underscore
    >>> content = { 'pattern2': ['A A'], 'pattern1': ['<#_,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'A A'
    >>> bw.write('pattern1')
    'A_A'

    >>> # remove nonletters
    >>> content = { 'pattern2': ['A. A-'], 'pattern1': ['<#@,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'A. A-'
    >>> bw.write('pattern1')
    'AA'

    >>> # white space to underscore and first cap
    >>> content = { 'pattern2': ['a a'], 'pattern1': ['<#^_,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'a a'
    >>> bw.write('pattern1')
    'A_a'

    >>> # make title case
    >>> content = { 'pattern2': ['aa aa'], 'pattern1': ['<#^^,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'aa aa'
    >>> bw.write('pattern1')
    'Aa Aa'

    >>> # make allcaps
    >>> content = { 'pattern2': ['aa aa'], 'pattern1': ['<#^^^,pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'aa aa'
    >>> bw.write('pattern1')
    'AA AA'

    >>> # generate a random number
    >>> content = { 'pattern1': ['<-randint(1, 20)->']}
    >>> bw = BlurbWriter(content)
    >>> result = bw.write('pattern1')
    >>> assert 1 <= int(result) <= 20

    >>> # detect spinning because of a malformed tag
    >>> content = { 'pattern2': ['a'], 'pattern1': ['<#pattern2>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'a'
    >>> bw.write('pattern1')
    '<#pattern2>'

    >>> # replace a tag, variable
    >>> # '<#_aname=name#><#_aname#>’s
    >>> content = { 'pattern2': ['a'], 'pattern1': ['<#varName=pattern2#>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'a'
    >>> bw.write('pattern1')
    ''

    >>> # replace a tag, whitespace
    >>> content = { 'pattern2': ['a'], 'pattern1': ['<#    pattern2    #>']}
    >>> bw = BlurbWriter(content)
    >>> bw.write('pattern2')
    'a'
    >>> bw.write('pattern1')
    'a'

    # >>> # prefix an / a article for a result based on consonant / vowel
    # >>> content = { 'pattern2': ['a'], 'pattern1': ['<#article, pattern2#>'],  'pattern4': ['b'], 'pattern3': ['<#article, pattern4#>']}
    # >>> bw = BlurbWriter(content)
    # >>> bw.write('pattern1')
    # 'an a'
    # >>> bw.write('pattern3')
    # 'a b'

    # >>> # replace a nested tag
    # >>> content = { 'pattern2': ['pattern'], 'pattern1': ['<#<#pattern2#>3#>'], 'pattern3': ['b']}
    # >>> bw = BlurbWriter(content)
    # >>> bw.write('pattern1')
    # 'b'

    # >>> # capitalisation of first character
    # >>> content = { 'pattern1': ['<#^,pattern2#>'], 'pattern2': ['aa aa']}
    # >>> bw = BlurbWriter(content)
    # >>> bw.write('pattern1')
    # 'Aa aa'

    # >>> # unicode content
    # >>> content = { 'pattern1': ['üößé']}
    # >>> bw = BlurbWriter(content)
    # >>> bw.write('pattern1')
    # 'üößé'

    # # '\\xfc\\xf6\\xdf\\xe9'

    # # not sure if that is the right way

    # >>> # replace a tag
    # >>> content = { 'pattern2': ['a'], 'pattern1': ['<#pattern2#>']}
    # >>> bw = BlurbWriter(content, debug=True)
    # >>> bw.write('pattern2')
    # pattern2
    # 'a'
    # >>> bw.write('pattern1')
    # pattern1
    # pattern2
    # 'a'
    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
