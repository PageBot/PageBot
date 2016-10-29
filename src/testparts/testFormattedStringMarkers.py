import re

def getMarker(markerId, args=None):
    u"""Answer a formatted string with markerId that can be used as non-display marker. 
    This way the Composer can find the position of markers in text boxes, after
    FS-slicing has been done. Note there is always a very small "white-space"
    added to the string, so there is a potential difference in width that matters.
    For that reason markers should not be changed after slizing (which would theoretically
    alter the flow of the FormattedString in an box) and the markerId and amount/length 
    of args should be kept as small as possible."""
    marker = '==%s--%s==' % (markerId, args or '') 
    return FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)  

FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_]*)\-\-([^=]*)\=\=')

def findMarkers(fs):
    u"""Answer a dictionary of markers with their arguments that exist in a given FormattedString."""
    markers = {}
    for markerId, args in FIND_FS_MARKERS.findall(`fs`):
        if not markerId in markers:
            markers[markerId] = []
        markers[markerId].append(args)
    return markers

fs = FormattedString('AAAAA', fontSize=40) + getMarker('MultipleMarkers', 'a,b,c,d') + FormattedString('CCCC', fontSize=40) + getMarker('AnImageReference', '/filePath') + getMarker('MultipleMarkers', 'xyz') + FormattedString('DDDDD', fontSize=40) + getMarker('MarkerWithoutArguments') + FormattedString('EEEEE', fontSize=40)

textBox(fs, (10, 10, 300, 300))
print getMarkers(fs)
