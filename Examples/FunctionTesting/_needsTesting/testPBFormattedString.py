from drawBot.context.baseContext import FormattedString

class PBFormattedString(FormattedString):
    def __init__(self, txt=None, style=None, **kwargs):
        self.styles = []
        self.styles.append(style) # Can be None, needs sync with lines/runs
        self._mergeStyle(style, **kwargs)
        FormattedString.__init__(self, txt, **kwargs)

    def _mergeStyle(self, style, **kwargs):
        if style is not None:
            for name, value in style.items():
                if not name in kwargs:
                    kwargs[name] = value
      
fs = PBFormattedString('aaa', style=dict(fill=(1,0,0), font='Verdana', fontSize=62))
        
print 3333, fs

text(fs, (100, 100))
print fs.styles

