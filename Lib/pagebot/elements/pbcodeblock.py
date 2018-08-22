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
#     codeblock.py
#
from pagebot.elements.element import Element
from pagebot.constants import ORIGIN
from pagebot.toolbox.units import pointOffset

class CodeBlock(Element):

    def __init__(self, code, **kwargs):
        Element.__init__(self, **kwargs)
        self.code = code

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):
        """Execute the code block. Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with
        ~~~Python
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries
        convert this codeblock to
        <pre><code class="Python">
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        </code></pre>
        This way authors can run PageBot generators controlled by content.
        Content result dictionary (per codeblock) is stored in self.codeBlocks[codeId].

        >>> from pagebot.document import Document
        >>> doc = Document(size=(500, 500))
        >>> view = doc.view
        >>> page = doc[1]
        >>> script = 'print(100 * 200)'
        >>> cb = CodeBlock(script, parent=page)
        >>> page.build(view)
        ('CodeBlock', 'print(100 * 200)')
        """
        context = self.context # Get current context and builder.

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        print('CodeBlock', self.code)
        return

        result = dict(view=view)
        if execute and node.text:
            if not self.tryExcept:
                if self.verbose:
                     print(u'Globals: %s' % result)
                     print(u'Typesetter: %s' % node.text)
                exec(node.text, result) in result # Exectute code block, where result goes dict.
                codeId = result.get('cid', codeId) # Overwrite base codeId, if defined in the block.
                del result['__builtins__'] # We don't need this set of globals in the returned results.
            else:
                error = None
                try:
                    exec(node.text, result) in result # Exectute code block, where result goes dict.
                    codeId = result.get('cid', codeId) # Overwrite base codeId, if defined in the block.
                    del result['__builtins__'] # We don't need this set of globals in the results.
                except TypeError:
                    error = u'TypeError'
                except NameError:
                    error = 'NameError'
                except SyntaxError:
                    error = 'SyntaxError'
                except AttributeError:
                    error = 'AttributeError'
                result['__error__'] = error
                if self.verbose and error is not None:
                    print(u'### %s ### %s' % (error, node.text))

        # doc, page or box may have changed, store them back into the typesetter,
        # so they are available for the execution of a next code block.
        self.doc = result.get(self.globalDocName)
        self.page = result.get(self.globalPageName)
        self.box = result.get(self.globalBoxName)
        # TODO: insert more possible exec() errors here.

        # For convenience, store the source code of the block in the result dict.
        if '__code__' not in result:
            result['__code__'] = node.text

        # Store the result dict as code block. Global values have become dict entries.
        # Make sure that we have a unique codeId (it may have been defined in different
        # markdown files, so sequential index it no guarantee.)
        if codeId in self.codeBlocks:
            n = 0
            codeIdTmp = codeId
            while codeIdTmp in self.codeBlocks:
                codeIdTmp = '%s_%d' % (codeId, n)
                n += 1
            codeId = codeIdTmp # We have a codeId now that does not already exist.
        # Store the result dict in self.codeBlocks under the unique name.
        self.codeBlocks[codeId] = result
        return codeId, result

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
