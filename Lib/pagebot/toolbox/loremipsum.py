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
#     pip install python-lorem
#     https://pypi.org/project/python-lorem/
# -----------------------------------------------------------------------------
#
#     loremipsum.py
#
#     Answers a random lorem ipsum text.
#
#

from random import shuffle

def loremIpsum(doShuffle=False, words=None):
    """Answer random lorem ipsum text. Default is not to shuffle,
    self doc test always gets the same result.

    >>> loremIpsum()[:50]
    'Lorem ipsum dolor sit amet, consectetur adipiscing'
    >>> loremIpsum(words=4) # Cutting of at word count, always ending with a period.
    'Lorem ipsum dolor sit.'
    """
    lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et sapien tempor, tincidunt turpis tincidunt, bibendum arcu. Proin nec erat ut dui auctor aliquam egestas sit amet urna. Fusce auctor varius viverra. Morbi augue sapien, auctor et egestas vitae, venenatis et mi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin bibendum diam id dapibus maximus. Curabitur et odio tincidunt, fermentum velit eget, iaculis augue. Duis faucibus sapien id massa facilisis pretium ut non tortor.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ullamcorper laoreet arcu at semper. Donec hendrerit eros quis nulla auctor, a feugiat quam viverra. Morbi urna tortor, mattis et volutpat non, auctor non turpis. Maecenas maximus justo eget eros feugiat ultrices. Sed enim enim, dictum non bibendum vel, tincidunt faucibus eros. Sed id felis viverra, feugiat urna et, suscipit ipsum. Praesent laoreet nunc eros, et hendrerit elit vestibulum vel. Aliquam in malesuada sapien. Etiam sit amet lorem eget diam consectetur malesuada.
Suspendisse potenti. Integer faucibus quam non scelerisque blandit. Mauris sollicitudin facilisis ex mollis accumsan. Aenean ligula diam, condimentum et lacus sed, iaculis cursus ligula. Maecenas vestibulum varius tellus, at auctor diam placerat at. Vivamus vel urna ligula. Ut turpis nunc, pharetra non arcu in, tincidunt sagittis lectus. Proin aliquet purus vitae nulla tincidunt, placerat sollicitudin mauris tempus. Quisque sapien turpis, auctor ac blandit id, hendrerit et enim. Cras condimentum dolor in fringilla dapibus.
Cras ac ligula molestie, condimentum nunc vel, luctus massa. In elementum semper fermentum. Fusce porttitor non ex mollis laoreet. Fusce aliquam ultricies enim vitae consequat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam vitae fringilla risus. Etiam suscipit suscipit ante, at ultrices urna ullamcorper in. Integer ac felis volutpat, sollicitudin augue a, tincidunt est. Mauris varius velit est, vitae facilisis tortor viverra id. Donec et nisl quam. Aliquam erat volutpat. Praesent eu consequat risus, sed dapibus erat. Aenean ullamcorper, lorem et viverra consequat, mauris arcu luctus arcu, sed interdum elit nisl ac purus.
Lorem ipsum dolor sit turpis dui, lacinia sed mattis nec, suscipit nec massa. Mauris enim nulla, elementum et sapien eget, ultrices dictum lorem. Vestibulum ornare porttitor interdum. Quisque finibus consectetur purus a tincidunt. Nullam elit tortor, porttitor sit amet pellentesque vel, posuere vel sapien. Suspendisse euismod orci sed congue pretium. In convallis dictum nibh lobortis volutpat.
Vivamus a nibh non lectus ullamcorper finibus et sit amet arcu. Ut vel dapibus ante. Etiam sit amet leo ac nulla commodo molestie id sit amet neque. Nunc aliquam egestas massa, eu hendrerit tellus malesuada et. Pellentesque gravida, sapien sed cursus euismod, nisi mauris aliquam justo, a tristique risus velit in diam. Aenean sit amet mollis quam. Phasellus id nisl pretium, dignissim erat sit amet, lobortis tellus. Donec consequat ut magna vitae pellentesque. Mauris vitae nulla vel massa facilisis consectetur in ut elit. Praesent imperdiet magna non dignissim cursus. Phasellus rutrum enim vitae sapien facilisis, ut rhoncus nunc hendrerit. Maecenas eleifend rhoncus libero, sed ornare lacus ultrices in. Curabitur malesuada vel tortor varius rhoncus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
Nunc porta massa vel elit pretium, non convallis mauris maximus. Proin volutpat ex et turpis cursus gravida. Pellentesque maximus nisl ac dictum luctus. Nulla accumsan tincidunt mi. Mauris euismod tellus eget eros euismod fringilla. Suspendisse tincidunt, purus quis tempus aliquet, justo quam congue nulla, ut elementum felis nisi eget eros. Aliquam tempor ipsum id quam interdum ornare. Aenean accumsan est elit, maximus mattis nulla hendrerit in. Ut luctus, metus id rutrum volutpat, nibh leo condimentum nisi, a vulputate purus mauris non arcu. Pellentesque ut tortor dolor. Sed fringilla commodo dapibus. Duis eget aliquam mauris. Mauris iaculis leo sollicitudin metus maximus, quis euismod elit volutpat. Nullam lobortis tempor nisi, ac posuere est mollis vel. Suspendisse ullamcorper leo vel mollis semper. Vivamus eget quam posuere, ultricies lacus non, placerat augue.
Mauris in arcu purus. Etiam euismod eros nec eros ultrices accumsan. Morbi auctor, odio ac posuere sollicitudin, ex lectus porttitor turpis, vitae finibus arcu nibh sit amet dolor. Morbi non sagittis libero, vitae feugiat tellus. Cras maximus nisi consequat odio pellentesque vestibulum. Etiam feugiat sem vel ullamcorper sollicitudin. Aliquam cursus quam vitae ipsum tempus dapibus. Phasellus eu tincidunt metus. Fusce eu pharetra nisi. Praesent enim purus, pharetra sit amet molestie id, fringilla at elit. Praesent et enim nunc.
Pellentesque blandit at diam sed suscipit. Curabitur dapibus feugiat dolor quis tempor. Donec laoreet ex sed venenatis rutrum. Nullam nec ultricies magna. Nullam rutrum risus in euismod pharetra. Quisque velit orci, hendrerit eu porta nec, mollis ut ante. Suspendisse potenti. Cras faucibus sed lorem ac gravida.
Morbi id tincidunt sapien, eget molestie neque. Phasellus bibendum venenatis leo ultrices facilisis. Nam vitae dui leo. Nunc posuere efficitur tellus, eu aliquam diam vulputate a. Proin faucibus aliquet mi, ac cursus odio viverra facilisis. Fusce commodo nisi id maximus mollis. Vivamus iaculis augue non magna ullamcorper, eu blandit libero tincidunt."""

    if doShuffle:
        lines = lorem.replace('\n', ' \n').split('. ')
        shuffle(lines)
        lorem = '. '.join(lines)+'.'
        while lorem.startswith('\n'):
            lorem = lorem[1:]

    if words is not None:
        lorem = ' '.join(lorem.split(' ')[:words])
        if not lorem.endswith('.'):
            lorem += '.'
    return lorem

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
