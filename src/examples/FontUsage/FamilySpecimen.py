# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FBFamilySpecimen.py
#
from pagebot.fonttoolbox.objects.family import getFamilies
from pagebot.publications.typespecimen import TypeSpecimen
# Page and Template instances are holding all elements of a page together.
from pagebot.page import Page, Template
from pagebot import getFormattedString
# Use Erik & Jonathan’s Filibuster to create random imaginary headlines. 
from pagebot.contributions.filibuster.blurb import blurb

DEBUG = False # Make True to see grid and element frames.

LIB_PATH = '/Library/Fonts/'
SOME_SYSTEM_FONTS = {
    # Let's try some plain OSX system fonts, while they are still there (not variable font yet).
    'Georgia': dict(Regular=LIB_PATH+'Georgia.ttf', Bold=LIB_PATH+'Georgia Bold.ttf', 
                    Italic=LIB_PATH+'Georgia Italic.ttf', BoldItalic=LIB_PATH+'Georgia Bold Italic.ttf'),
    'Verdana': dict(Regular=LIB_PATH+'Verdana.ttf', Bold=LIB_PATH+'Verdana Bold.ttf', 
                    Italic=LIB_PATH+'Verdana Italic.ttf', BoldItalic=LIB_PATH+'Verdana Bold Italic.ttf'),
}
# Inherit all behavior from the generic TypeSpecimen publication class
class FBFamilySpecimen(TypeSpecimen):

    def makeTemplate(self, rs):
        # Template for the main page.
        template = Template(style=rs) # Create second template. This is for the main pages.
        # Show grid columns and paddings if rootStyle.showGrid or 
        # rootStyle.showGridColumns are True.
        # The grid is just a regular element, like all others on the page. Same parameters apply.
        template.grid()  
        # Add named text box to template for main specimen text.
        template.cTextBox('', 0, -1, 6, 1, eId=self.titleBoxId)       
        template.cTextBox('', 0, 0, 6, 6, eId=self.specimenBoxId)       
        # Some lines, positioned by vertical and horizontal column index.
        template.cLine(0, 0, 6, 0, stroke=0, strokeWidth=0.25)       
        #template.cLine(0, 1, 6, 0, style=rs, stroke=0, strokeWidth=0.25)       
        template.cLine(0, 7, 6, 0, stroke=0, strokeWidth=0.25)       
        return template
        
    def buildPages(self, doc):
        # Build the pages, one page per family. Composition is one fitting line from random words.
        # Get the current page of the document, created automatic with template.
        # Using the first page as cover (to be filled...)

        # Collect the families, style names and their font paths, even when installed in DrawBot.
        families = getFamilies(SOME_SYSTEM_FONTS)        
        # Now we collected a families and styles in the OS, create one page per family.
        for familyName, family in sorted(families.items()): # For all the sorted family collections...
            family.install() # Install the fonts in DrawBot is not there already.
            # Create a new page for the this family, using the default template.
            page = doc.newPage() 
            print family.fonts.keys()   
            self.buildFamilySpecimenPage(page, family)

    def buildFamilySpecimenPage(self, page, family):
        box = page[self.specimenBoxId][0]
        fontSize = 500
        while not box.getOverflow():
            sportsHeadline = ' '.join(blurb.getBlurb('news_headline').split(' ')[:choice((2,2,3,3,4))])+'\n'
            styleKey = choice(('Regular', 'Bold', 'Italic', 'BoldItalic'))
            fs = getFormattedString(sportsHeadline, self, style=dict(font=family[styleKey].installedName, 
                fontSize=fontSize))
            fsWidth = fs.size()[0]
            fittingFontSize = fontSize * box.w / fsWidth
            # Make new formatted string with fitting font size.
            fs = getFormattedString(sportsHeadline, self, style=dict(font=family[styleKey].installedName, 
                leading=0, fontSize=fittingFontSize, textColor=0))
            box.append(fs)
            print '###', page, family, sportsHeadline
                
# Create a new specimen publications and add the list of system fonts.
familySpecimen = FBFamilySpecimen(showGrid=DEBUG) 
# Build the pages of the publication, interpreting the font list.
familySpecimen.build()
# Export the document of the publication to PDF in the _export directory.
# Create the dictionary if it is does not exist. All _export directories are ignored in git.
familySpecimen.export('FamilySpecimen.pdf')
