#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Made for usage in PageBot, www.pagebot.pro
#
# Copied from <https://github.com/waylan/Python-Markdown>
"""
Literature Extension for Python-Markdown
=======================================

Adds literature handling to Python-Markdown.

See <https://pythonhosted.org/Markdown/extensions/footnotes.html>
for documentation.

Copyright The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern
from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor
from markdown.util import etree
from collections import OrderedDict
import re

LIT_BACKLINK_TEXT = "AAzz1337820767766393qq"
NBSP_PLACEHOLDER = "qq3936677670287331zzAA"
DEF_RE = re.compile(r'[ ]{0,3}\[\=([^\]]*)\]:\s*(.*)')
TABBED_RE = re.compile(r'((\t)|(    ))(.*)')


class LiteratureExtension(Extension):
    """ Literature Extension. """

    def __init__(self, *args, **kwargs):
        """ Setup configs. """

        self.config = {
            'PLACE_MARKER':
                ["///Literature Goes Here///",
                 "The text string that marks where the literature references go"],
            'UNIQUE_IDS':
                [False,
                 "Avoid name collisions across "
                 "multiple calls to reset()."],
            "BACKLINK_TEXT":
                ["&#8617;",
                 "The text string that links from the literature reference "
                 "to the reader's place."]
        }
        super(LiteratureExtension, self).__init__(*args, **kwargs)

        # In multiple invocations, emit links that don't get tangled.
        self.unique_prefix = 0

        self.reset()

    def extendMarkdown(self, md, md_globals):
        """ Add pieces to Markdown. """
        md.registerExtension(self)
        self.parser = md.parser
        self.md = md
        # Insert a preprocessor before ReferencePreprocessor
        md.preprocessors.add(
            "literature", LiteraturePreprocessor(self), "<reference"
        )
        # Insert an inline pattern before ImageReferencePattern
        LITERATURE_RE = r'\[\=([^\]]*)\]'  # blah blah [^1] blah
        md.inlinePatterns.add(
            "literature", LiteraturePattern(LITERATURE_RE, self), "<reference"
        )
        # Insert a tree-processor that would actually add the literatures div
        # This must be before all other treeprocessors (i.e., inline and
        # codehilite) so they can run on the the contents of the div.
        md.treeprocessors.add(
            "literature", LiteratureTreeprocessor(self), "_begin"
        )
        # Insert a postprocessor after amp_substitute oricessor
        md.postprocessors.add(
            "literature", LiteraturePostprocessor(self), ">amp_substitute"
        )

    def reset(self):
        """ Clear literature references on reset, and prepare for distinct document. """
        self.literatures = OrderedDict()
        self.unique_prefix += 1

    def findLiteraturesPlaceholder(self, root):
        """ Return ElementTree Element that contains Literature placeholder. """
        def finder(element):
            for child in element:
                if child.text:
                    if child.text.find(self.getConfig("PLACE_MARKER")) > -1:
                        return child, element, True
                if child.tail:
                    if child.tail.find(self.getConfig("PLACE_MARKER")) > -1:
                        return child, element, False
                child_res = finder(child)
                if child_res is not None:
                    return child_res
            return None

        res = finder(root)
        return res

    def setLiterature(self, id, text):
        """ Store a literature for later retrieval. """
        self.literatures[id] = text

    def get_separator(self):
        if self.md.output_format in ['html5', 'xhtml5']:
            return '-'
        return ':'

    def makeLiteratureId(self, id):
        """ Return literature link id. """
        if self.getConfig("UNIQUE_IDS"):
            return 'lit%s%d-%s' % (self.get_separator(), self.unique_prefix, id)
        else:
            return 'lit%s%s' % (self.get_separator(), id)

    def makeLiteratureRefId(self, id):
        """ Return literature back-link id. """
        if self.getConfig("UNIQUE_IDS"):
            return 'litref%s%d-%s' % (self.get_separator(),
                                     self.unique_prefix, id)
        else:
            return 'litref%s%s' % (self.get_separator(), id)

    def makeLiteraturesDiv(self, root):
        """ Return div of literatures as et Element. """

        if not list(self.literatures.keys()):
            return None

        div = etree.Element("div")
        div.set('class', 'literature')
        etree.SubElement(div, "hr")
        ol = etree.SubElement(div, "ol")

        for id in self.literatures.keys():
            li = etree.SubElement(ol, "li")
            li.set("id", self.makeLiteratureId(id))
            self.parser.parseChunk(li, self.literatures[id])
            backlink = etree.Element("a")
            backlink.set("href", "#" + self.makeLiteratureRefId(id))
            if self.md.output_format not in ['html5', 'xhtml5']:
                backlink.set("rev", "literature")  # Invalid in HTML5
            backlink.set("class", "literature-backref")
            backlink.set(
                "title",
                "Jump back to literature %d in the text" %
                (self.literatures.index(id)+1)
            )
            backlink.text = LIT_BACKLINK_TEXT

            if list(li):
                node = li[-1]
                if node.tag == "p":
                    node.text = node.text + NBSP_PLACEHOLDER
                    node.append(backlink)
                else:
                    p = etree.SubElement(li, "p")
                    p.append(backlink)
        return div


class LiteraturePreprocessor(Preprocessor):
    """ Find all literature references and store for later use. """

    def __init__(self, literatures):
        self.literatures = literatures

    def run(self, lines):
        """
        Loop through lines and find, set, and remove literature definitions.

        Keywords:

        * lines: A list of lines of text

        Return: A list of lines of text with literature definitions removed.

        """
        newlines = []
        i = 0
        while True:
            m = DEF_RE.match(lines[i])
            if m:
                lit, _i = self.detectTabbed(lines[i+1:])
                lit.insert(0, m.group(2))
                i += _i-1  # skip past literature
                self.literatures.setLiterature(m.group(1), "\n".join(lit))
            else:
                newlines.append(lines[i])
            if len(lines) > i+1:
                i += 1
            else:
                break
        return newlines

    def detectTabbed(self, lines):
        """ Find indented text and remove indent before further proccesing.

        Keyword arguments:

        * lines: an array of strings

        Returns: a list of post processed items and the index of last line.

        """
        items = []
        blank_line = False  # have we encountered a blank line yet?
        i = 0  # to keep track of where we are

        def detab(line):
            match = TABBED_RE.match(line)
            if match:
                return match.group(4)

        for line in lines:
            if line.strip():  # Non-blank line
                detabbed_line = detab(line)
                if detabbed_line:
                    items.append(detabbed_line)
                    i += 1
                    continue
                elif not blank_line and not DEF_RE.match(line):
                    # not tabbed but still part of first par.
                    items.append(line)
                    i += 1
                    continue
                else:
                    return items, i+1

            else:  # Blank line: _maybe_ we are done.
                blank_line = True
                i += 1  # advance

                # Find the next non-blank line
                for j in range(i, len(lines)):
                    if lines[j].strip():
                        next_line = lines[j]
                        break
                else:
                    break  # There is no more text; we are done.

                # Check if the next non-blank line is tabbed
                if detab(next_line):  # Yes, more work to do.
                    items.append("")
                    continue
                else:
                    break  # No, we are done.
        else:
            i += 1

        return items, i


class LiteraturePattern(Pattern):
    """ InlinePattern for literature markers in a document's body text. """

    def __init__(self, pattern, literatures):
        super(LiteraturePattern, self).__init__(pattern)
        self.literatures = literatures

    def handleMatch(self, m):
        id = m.group(2)
        if id in self.literatures.literatures.keys():
            sup = etree.Element("literatureref")
            a = etree.SubElement(sup, "a")
            sup.set('id', self.literatures.makeLiteratureRefId(id))
            a.set('href', '#' + self.literatures.makeLiteratureId(id))
            if self.literatures.md.output_format not in ['html5', 'xhtml5']:
                a.set('rel', 'literature')  # invalid in HTML5
            a.set('class', 'literature-ref')
            a.text = '['+id+']'
            return sup
        else:
            return None


class LiteratureTreeprocessor(Treeprocessor):
    """ Build and append literature div to end of document. """

    def __init__(self, literatures):
        self.literatures = literatures

    def run(self, root):
        literaturesDiv = self.literatures.makeLiteraturesDiv(root)
        if literaturesDiv is not None:
            result = self.literatures.findLiteraturesPlaceholder(root)
            if result:
                child, parent, isText = result
                ind = list(parent).index(child)
                if isText:
                    parent.remove(child)
                    parent.insert(ind, literaturesDiv)
                else:
                    parent.insert(ind + 1, literaturesDiv)
                    child.tail = None
            else:
                root.append(literaturesDiv)


class LiteraturePostprocessor(Postprocessor):
    """ Replace placeholders with html entities. """
    def __init__(self, literatures):
        self.literatures = literatures

    def run(self, text):
        text = text.replace(
            LIT_BACKLINK_TEXT, self.literatures.getConfig("BACKLINK_TEXT")
        )
        return text.replace(NBSP_PLACEHOLDER, "&#160;")


def makeExtension(*args, **kwargs):
    """ Return an instance of the LiteratureExtension """
    return LiteratureExtension(*args, **kwargs)
