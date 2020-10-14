#!/bin/bash
set -ev
export PWD="Lib/pagebot"
export PY="python3"

$PY $PWD/__init__.py

$PY $PWD/base/__init__.py
$PY $PWD/base/article.py
$PY $PWD/base/composer.py
$PY $PWD/base/typesetter.py

# Conditions.
$PY $PWD/conditions/__init__.py
$PY $PWD/conditions/align.py
$PY $PWD/conditions/columns.py
$PY $PWD/conditions/condition.py
$PY $PWD/conditions/floating.py
$PY $PWD/conditions/flow.py
$PY $PWD/conditions/score.py
$PY $PWD/conditions/text.py
$PY $PWD/constants.py

# Contexts.
$PY $PWD/contexts/__init__.py
$PY $PWD/contexts/basecontext/abstractcontext.py
$PY $PWD/contexts/basecontext/babelstring.py
$PY $PWD/contexts/basecontext/babelrun.py
$PY $PWD/contexts/basecontext/basebeziercontour.py
$PY $PWD/contexts/basecontext/basebezierpath.py
$PY $PWD/contexts/basecontext/basebezierpoint.py
$PY $PWD/contexts/basecontext/basebuilder.py
$PY $PWD/contexts/basecontext/basecontext.py
$PY $PWD/contexts/basecontext/baseimageobject.py
$PY $PWD/contexts/basecontext/beziercontour.py
$PY $PWD/contexts/basecontext/bezierpath.py
$PY $PWD/contexts/flatcontext/flatbuilder.py
$PY $PWD/contexts/flatcontext/flatbezierpath.py
$PY $PWD/contexts/flatcontext/flatcontext.py
$PY $PWD/contexts/markup/htmlbuilder.py
$PY $PWD/contexts/markup/htmlcontext.py
$PY $PWD/contexts/markup/sitebuilder.py
$PY $PWD/contexts/markup/svgbuilder.py
$PY $PWD/contexts/markup/svgcontext.py
$PY $PWD/contexts/markup/xmlbuilder.py
$PY $PWD/contexts/sketchcontext/sketchcontext.py
$PY $PWD/contexts/sketchcontext/sketchbuilder.py

#TODO: add rest of contributions.
#$PY $PWD/contributions/adobe/__init__.py
#$PY $PWD/contributions/adobe/kerndump/__init__.py.py
#$PY $PWD/contributions/adobe/kerndump/dumpKerningFeatureFromOTF.py
#$PY $PWD/contributions/adobe/kerndump/getKerningPairsFromOTF.py
#$PY $PWD/contributions/filibuster/__init__.py
$PY $PWD/contributions/filibuster/blurb.py
$PY $PWD/contributions/filibuster/blurbwriter.py
#$PY $PWD/contributions/filibuster/example.py
#$PY $PWD/contributions/filibuster/test.py
#$PY $PWD/contributions/filibuster/titlecase.py
#$PY $PWD/contributions/markdown/__init__.py
#$PY $PWD/contributions/markdown/footnotes.py
#$PY $PWD/contributions/markdown/inline.py
#$PY $PWD/contributions/markdown/literature.py

$PY $PWD/document.py

# Elements.
$PY $PWD/elements/alignments.py
$PY $PWD/elements/artboard.py
$PY $PWD/elements/clippath.py
$PY $PWD/elements/codeblock.py
$PY $PWD/elements/conditions.py
$PY $PWD/elements/element.py
$PY $PWD/elements/flow.py
$PY $PWD/elements/galley.py
$PY $PWD/elements/group.py
$PY $PWD/elements/image.py
#$PY $PWD/elements/image2.py
$PY $PWD/elements/imaging.py
$PY $PWD/elements/line.py
$PY $PWD/elements/oval.py
$PY $PWD/elements/page.py
$PY $PWD/elements/placer.py
$PY $PWD/elements/polygon.py
$PY $PWD/elements/quire.py
$PY $PWD/elements/rect.py
$PY $PWD/elements/ruler.py
$PY $PWD/elements/shrinking.py
$PY $PWD/elements/table.py
$PY $PWD/elements/template.py
$PY $PWD/elements/text.py
$PY $PWD/elements/textalignments.py
$PY $PWD/elements/textconditions.py
$PY $PWD/elements/showings.py
$PY $PWD/elements/dating/__init__.py
$PY $PWD/elements/dating/calendarmonth.py
#$PY $PWD/elements/designspacegraph/designspacegraph.py
$PY $PWD/elements/newspapers/__init__.py
#$PY $PWD/elements/newspapers/articles.py
$PY $PWD/elements/newspapers/headers.py
$PY $PWD/elements/glyphpath.py
$PY $PWD/elements/paths.py
#$PY $PWD/elements/ui/....py
$PY $PWD/elements/variablefonts/animationframe.py
$PY $PWD/elements/variablefonts/basefontshow.py
$PY $PWD/elements/variablefonts/bezieranimation.py
$PY $PWD/elements/variablefonts/bio.py
$PY $PWD/elements/variablefonts/cube.py
$PY $PWD/elements/variablefonts/fittowidth.py
$PY $PWD/elements/variablefonts/fonticon.py
$PY $PWD/elements/variablefonts/glyphdimensions.py
$PY $PWD/elements/variablefonts/glyphset.py
#$PY $PWD/elements/variablefonts/paragraphs.py
$PY $PWD/elements/variablefonts/sampler.py
#$PY $PWD/elements/variablefonts/specimen.py
#$PY $PWD/elements/variablefonts/stacked.py
#$PY $PWD/elements/variablefonts/title.py
$PY $PWD/elements/variablefonts/typeramps.py
$PY $PWD/elements/variablefonts/variablecircle.py
$PY $PWD/elements/variablefonts/variablecube.py
$PY $PWD/elements/variablefonts/variablecube2.py
$PY $PWD/elements/variablefonts/variableglyphs.py
$PY $PWD/elements/variablefonts/variablescatter.py
#$PY $PWD/elements/variablefonts/waterfall.py
$PY $PWD/elements/variablefonts/widths.py
$PY $PWD/elements/views/__init__.py
$PY $PWD/elements/views/baseview.py
$PY $PWD/elements/views/gitview.py
$PY $PWD/elements/views/googleappsview.py
$PY $PWD/elements/views/googlecloudview.py
$PY $PWD/elements/views/htmlview.py
$PY $PWD/elements/views/mampview.py
$PY $PWD/elements/views/pageview.py
$PY $PWD/elements/views/pagemapview.py
$PY $PWD/elements/views/siteview.py
#$PY $PWD/elements/web/....py

$PY $PWD/errors.py

$PY $PWD/fonttoolbox/objects/family.py
$PY $PWD/fonttoolbox/objects/font.py
$PY $PWD/fonttoolbox/objects/fontinfo.py
$PY $PWD/fonttoolbox/objects/glyph.py
$PY $PWD/fonttoolbox/objects/prevarfamily.py
$PY $PWD/fonttoolbox/otlTools.py
$PY $PWD/fonttoolbox/ttftools.py
$PY $PWD/fonttoolbox/unicodes/unicoderanges.py

$PY $PWD/gradient.py
$PY $PWD/mathematics/__init__.py
$PY $PWD/mathematics/transform3d.py
$PY $PWD/filepaths.py

$PY $PWD/publications/publication.py
$PY $PWD/publications/typespecimens/__init__.py
$PY $PWD/publications/typespecimens/basetypespecimen.py
#$PY $PWD/publications/typespecimens/fontographer35keymap.py
$PY $PWD/publications/typespecimens/simplespecimen.py
$PY $PWD/publications/typespecimens/specimens.py
$PY $PWD/publications/typespecimens/typespecimen.py
$PY $PWD/publications/typespecimens/proofing/__init__.py
$PY $PWD/publications/typespecimens/proofing/pagewide.py
$PY $PWD/publications/typespecimens/proofing/proof.py
$PY $PWD/publications/typespecimens/proofing/tx.py
$PY $PWD/publications/websites/nanosite/nanosite.py
$PY $PWD/publications/newspapers/basenewspaper.py
# TODO: add rest of publications...
# ...
$PY $PWD/publications/calendars/basecalendar.py

$PY $PWD/readers/__init__.py
$PY $PWD/readers/mdreader.py
$PY $PWD/readers/rereader.py
$PY $PWD/readers/xmlreader.py

$PY $PWD/server/__init__.py
# Hangs on server process.
# $PY $PWD/server/baseserver.py

$PY $PWD/style.py
$PY $PWD/stylelib.py

$PY $PWD/templates/__init__.py
# ...

$PY $PWD/themes/__init__.py
$PY $PWD/themes/backtothecity.py
$PY $PWD/themes/basetheme.py
$PY $PWD/themes/businessasusual.py
$PY $PWD/themes/fairytales.py
$PY $PWD/themes/freshandshiny.py
$PY $PWD/themes/happyholidays.py
$PY $PWD/themes/intothewoods.py
$PY $PWD/themes/seasoningthedish.py
$PY $PWD/themes/somethingintheair.py
$PY $PWD/themes/wordlywise.py

$PY $PWD/toolbox/color.py
$PY $PWD/toolbox/columncalc.py
$PY $PWD/toolbox/dating.py
$PY $PWD/toolbox/hyphenation.py
$PY $PWD/toolbox/markers.py
$PY $PWD/toolbox/timemark.py
$PY $PWD/toolbox/units.py
