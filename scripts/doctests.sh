#!/bin/bash
set -ev
export PWD="Lib/pagebot"

python3 $PWD/__init__.py

python3 $PWD/base/__init__.py
python3 $PWD/base/article.py
python3 $PWD/base/composer.py
python3 $PWD/base/typesetter.py

# Conditions.
python3 $PWD/conditions/__init__.py
python3 $PWD/conditions/align.py
python3 $PWD/conditions/columns.py
python3 $PWD/conditions/condition.py
python3 $PWD/conditions/floating.py
python3 $PWD/conditions/flow.py
python3 $PWD/conditions/score.py
python3 $PWD/conditions/text.py
python3 $PWD/constants.py

# Contexts.
python3 $PWD/contexts/__init__.py
python3 $PWD/contexts/basecontext/abstractcontext.py
python3 $PWD/contexts/basecontext/babelstring.py
python3 $PWD/contexts/basecontext/babelrun.py
python3 $PWD/contexts/basecontext/basebeziercontour.py
python3 $PWD/contexts/basecontext/basebezierpath.py
python3 $PWD/contexts/basecontext/basebezierpoint.py
python3 $PWD/contexts/basecontext/basebuilder.py
python3 $PWD/contexts/basecontext/basecontext.py
python3 $PWD/contexts/basecontext/baseimageobject.py
python3 $PWD/contexts/basecontext/beziercontour.py
python3 $PWD/contexts/basecontext/bezierpath.py
python3 $PWD/contexts/flatcontext/flatbuilder.py
python3 $PWD/contexts/flatcontext/flatbezierpath.py
python3 $PWD/contexts/flatcontext/flatcontext.py
python3 $PWD/contexts/markup/htmlbuilder.py
python3 $PWD/contexts/markup/htmlcontext.py
python3 $PWD/contexts/markup/sitebuilder.py
python3 $PWD/contexts/markup/svgbuilder.py
python3 $PWD/contexts/markup/svgcontext.py
python3 $PWD/contexts/markup/xmlbuilder.py
python3 $PWD/contexts/sketchcontext/sketchcontext.py
python3 $PWD/contexts/sketchcontext/sketchbuilder.py

#TODO: add rest of contributions.
#python3 $PWD/contributions/adobe/__init__.py
#python3 $PWD/contributions/adobe/kerndump/__init__.py.py
#python3 $PWD/contributions/adobe/kerndump/dumpKerningFeatureFromOTF.py
#python3 $PWD/contributions/adobe/kerndump/getKerningPairsFromOTF.py
#python3 $PWD/contributions/filibuster/__init__.py
python3 $PWD/contributions/filibuster/blurb.py
python3 $PWD/contributions/filibuster/blurbwriter.py
#python3 $PWD/contributions/filibuster/example.py
#python3 $PWD/contributions/filibuster/test.py
#python3 $PWD/contributions/filibuster/titlecase.py
#python3 $PWD/contributions/markdown/__init__.py
#python3 $PWD/contributions/markdown/footnotes.py
#python3 $PWD/contributions/markdown/inline.py
#python3 $PWD/contributions/markdown/literature.py

python3 $PWD/document.py

# Elements.
python3 $PWD/elements/alignments.py
python3 $PWD/elements/artboard.py
python3 $PWD/elements/clippath.py
python3 $PWD/elements/codeblock.py
python3 $PWD/elements/conditions.py
python3 $PWD/elements/element.py
python3 $PWD/elements/flow.py
python3 $PWD/elements/galley.py
python3 $PWD/elements/group.py
python3 $PWD/elements/image.py
#python3 $PWD/elements/image2.py
python3 $PWD/elements/imaging.py
python3 $PWD/elements/line.py
python3 $PWD/elements/oval.py
python3 $PWD/elements/page.py
python3 $PWD/elements/placer.py
python3 $PWD/elements/polygon.py
python3 $PWD/elements/quire.py
python3 $PWD/elements/rect.py
python3 $PWD/elements/ruler.py
python3 $PWD/elements/shrinking.py
python3 $PWD/elements/table.py
python3 $PWD/elements/template.py
python3 $PWD/elements/text.py
python3 $PWD/elements/textalignments.py
python3 $PWD/elements/textconditions.py
python3 $PWD/elements/dating/__init__.py
python3 $PWD/elements/dating/calendarmonth.py
#python3 $PWD/elements/designspacegraph/designspacegraph.py
python3 $PWD/elements/newspapers/__init__.py
#python3 $PWD/elements/newspapers/articles.py
python3 $PWD/elements/newspapers/headers.py
python3 $PWD/elements/paths/__init__.py
python3 $PWD/elements/paths/glyphpath.py
#python3 $PWD/elements/paths/pbpaths.py
#python3 $PWD/elements/ui/....py
python3 $PWD/elements/variablefonts/animationframe.py
python3 $PWD/elements/variablefonts/basefontshow.py
python3 $PWD/elements/variablefonts/bezieranimation.py
python3 $PWD/elements/variablefonts/bio.py
python3 $PWD/elements/variablefonts/cube.py
python3 $PWD/elements/variablefonts/fittowidth.py
python3 $PWD/elements/variablefonts/fonticon.py
python3 $PWD/elements/variablefonts/glyphdimensions.py
python3 $PWD/elements/variablefonts/glyphset.py
#python3 $PWD/elements/variablefonts/paragraphs.py
python3 $PWD/elements/variablefonts/sampler.py
#python3 $PWD/elements/variablefonts/specimen.py
#python3 $PWD/elements/variablefonts/stacked.py
#python3 $PWD/elements/variablefonts/title.py
python3 $PWD/elements/variablefonts/typeramps.py
python3 $PWD/elements/variablefonts/variablecircle.py
python3 $PWD/elements/variablefonts/variablecube.py
python3 $PWD/elements/variablefonts/variablecube2.py
python3 $PWD/elements/variablefonts/variableglyphs.py
python3 $PWD/elements/variablefonts/variablescatter.py
#python3 $PWD/elements/variablefonts/waterfall.py
python3 $PWD/elements/variablefonts/widths.py
python3 $PWD/elements/views/__init__.py
python3 $PWD/elements/views/baseview.py
python3 $PWD/elements/views/gitview.py
python3 $PWD/elements/views/googleappsview.py
python3 $PWD/elements/views/googlecloudview.py
python3 $PWD/elements/views/htmlview.py
python3 $PWD/elements/views/mampview.py
python3 $PWD/elements/views/pageview.py
python3 $PWD/elements/views/pagemapview.py
python3 $PWD/elements/views/siteview.py
#python3 $PWD/elements/web/....py

python3 $PWD/errors.py

python3 $PWD/fonttoolbox/objects/family.py
python3 $PWD/fonttoolbox/objects/font.py
python3 $PWD/fonttoolbox/objects/fontinfo.py
python3 $PWD/fonttoolbox/objects/glyph.py
python3 $PWD/fonttoolbox/objects/prevarfamily.py
python3 $PWD/fonttoolbox/otlTools.py
python3 $PWD/fonttoolbox/ttftools.py
python3 $PWD/fonttoolbox/unicodes/unicoderanges.py

python3 $PWD/gradient.py
python3 $PWD/mathematics/__init__.py
python3 $PWD/mathematics/transform3d.py
python3 $PWD/filepaths.py

python3 $PWD/publications/typespecimens/__init__.py
python3 $PWD/publications/typespecimens/basetypespecimen.py
python3 $PWD/publications/typespecimens/simplespecimen.py
python3 $PWD/publications/typespecimens/specimens.py
python3 $PWD/publications/typespecimens/typespecimen.py
python3 $PWD/publications/typespecimens/proofing/__init__.py
python3 $PWD/publications/typespecimens/proofing/pagewide.py
python3 $PWD/publications/typespecimens/proofing/proof.py
python3 $PWD/publications/typespecimens/proofing/tx.py
python3 $PWD/publications/websites/nanosite/nanosite.py
python3 $PWD/publications/newspapers/basenewspaper.py
# TODO: add rest of publications...
# ...
python3 $PWD/publications/calendars/basecalendar.py

python3 $PWD/readers/__init__.py
python3 $PWD/readers/mdreader.py
python3 $PWD/readers/rereader.py
python3 $PWD/readers/xmlreader.py

python3 $PWD/server/__init__.py
# Hangs on server process.
# python3 $PWD/server/baseserver.py

python3 $PWD/style.py
python3 $PWD/stylelib.py

python3 $PWD/templates/__init__.py
# ...

python3 $PWD/themes/__init__.py
python3 $PWD/themes/backtothecity.py
python3 $PWD/themes/basetheme.py
python3 $PWD/themes/businessasusual.py
python3 $PWD/themes/fairytales.py
python3 $PWD/themes/freshandshiny.py
python3 $PWD/themes/happyholidays.py
python3 $PWD/themes/intothewoods.py
python3 $PWD/themes/seasoningthedish.py
python3 $PWD/themes/somethingintheair.py
python3 $PWD/themes/wordlywise.py

python3 $PWD/toolbox/color.py
python3 $PWD/toolbox/columncalc.py
python3 $PWD/toolbox/dating.py
python3 $PWD/toolbox/hyphenation.py
python3 $PWD/toolbox/markers.py
python3 $PWD/toolbox/timemark.py
python3 $PWD/toolbox/units.py
