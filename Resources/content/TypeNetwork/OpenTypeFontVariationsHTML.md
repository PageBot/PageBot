<style>
body {font: 100% Helmet, Freesans, sans-serif;}

body, select, input, textarea {color: #222;}

a {
	color: #f33;
	text-decoration: none;
	transition: 0.25s color;
}
a:hover {
	color: #d00;
	text-decoration: underline;
}

::-moz-selection{background: #fcd700; color: #fff; text-shadow: none;}
::selection {background: #fcd700; color: #fff; text-shadow: none;}

ins {background-color: #fcd700; color: #000; text-decoration: none;}
mark {background-color: #fcd700; color: #000; font-style: italic; font-weight: bold;}

input:-moz-placeholder { color:#a9a9a9; }
textarea:-moz-placeholder { color:#a9a9a9; }

blockquote {padding: 1rem; background: #eee;}

@font-face {
  font-family: "MomentumSans-VF";
  src: url("/assets_content/fonts/MomentumSans-VF.ttf");
  /* wght 10, 115, 220 */
  /* wdth  533, 769, 769 */
  /* opsz 12, 12, 72 */ 
}

@font-face {
  font-family: "AmstelvarAlpha-VF";
  src: url("/assets_content/uploads/AmstelvarAlpha-VF.ttf");
}

body {
	--max-content-width: 50rem;
	font-family: "MomentumSans-VF";
	font-size: 1rem;
	font-variation-settings: "wght" 100, "wdth" 769, "opsz" 16;
	font-weight: normal;
}

body b {
	font-variation-settings: "wght" 180, "wdth" 769, "opsz" 16;
}

.brochure-header {
	align-items: center;
	background-color: #ff3333;
	background-image: url(/assets_content/brochures/TN_OFV_header-bg.svg);
	display: flex;
	height: 24rem;
	padding: 1rem;
}

.brochure-header-title {
	--header-font-width: 500;
	color: #fff;
	font-family: "MomentumSans-VF";
	font-size: 2.25rem;
	font-variation-settings: "wght" 220, "wdth" var(--header-font-width), "opsz" 36;
	letter-spacing: 0.25rem;
	text-align: center;
	text-transform: uppercase;
	width: 100%;
	word-spacing: 16rem;
}

.brochure-nav-toc ol {
	color: #f33;
	list-style-type: decimal;
	font-size: 0.875rem;
	font-variation-settings: "wght" 180, "wdth" 769, "opsz" 12;
	margin-left: 1.5rem;
}

.brochure-nav-toc ol li {
	margin-bottom: 1rem;
}

.brochure-nav-toc ol li>ol {
	font-variation-settings: "wght" 115, "wdth" 769, "opsz" 16;
	list-style-type: lower-roman;
	margin-top: 1rem;
}

.brochure-section-alert {
	background-color: #ffffdc;
background-image: repeating-linear-gradient(-45deg, transparent, transparent 2rem, rgba(253, 253, 188, .5) 2rem, rgba(253, 253, 188, .5) 4rem);		border-radius: 0.5rem;
	font-size: 0.875rem;
	line-height: 1.4rem;
	margin: 2rem 0 1rem;
	padding: 1rem;
}

@supports (font-variation-settings: "wght" 100, "wdth" 769, "opsz" 16) {
	
	.brochure-section-alert {
		display: none;
	}
	
}

.brochure-section {
	padding: 2rem 1rem;
}

.brochure-section:target {
  padding-top: 4rem;
}

.brochure-section-alt-one {
	background-color: #eee;
}

.brochure-section-content {
	margin: 0 auto;
	max-width: var(--max-content-width);
}

.brochure-section-header {
	font-size: 0.875rem;
	font-variation-settings: "wght" 180, "wdth" 769, "opsz" 12;
	margin: 0 auto 2rem;
	max-width: var(--max-content-width);
	text-transform: uppercase;
}

.brochure-section-introduction {
	font-family: "AmstelvarAlpha-VF", serif;
	font-size: 1.125rem;
	font-variation-settings: "wght" 88, "wdth" 402, "opsz" 16, "XOPQ" 88, "XTRA" 402, "YOPQ" 50, "YTLC" 500, "YTSE" 18;
	line-height: 133%;
	margin: 0 auto 2rem;
	max-width: var(--max-content-width);
}

.brochure-section-module {
	margin-bottom: 2rem;
}

.brochure-section-module-thumb {
	border-radius: 0.5rem;
	height: auto;
	margin-bottom: 1rem;
	width: 100%;	
}

.brochure-section-font-animation {
  margin: 2rem 0;
}

.brochure-section-module-slug, .brochure-section-module-link {
	font-size: 0.75rem;
	font-variation-settings: "wght" 180, "wdth" 769, "opsz" 12;
	margin-bottom: 0.5rem;
	text-transform: uppercase;	
}

.brochure-section-module-title {
	font-size: 1rem;
	font-variation-settings: "wght" 180, "wdth" 769, "opsz" 24;
	line-height: 133%;
	margin-bottom: 1rem;
}

.brochure-section-module-deck {
	font-size: 0.875rem;
	line-height: 133%;
	margin-bottom: 0.5rem;
}

.brochure-footer {
	background-color: #222;
	color: #eee;
	font-size: 0.75rem;
	padding: 1rem;
}

.brochure-footer p {
	margin: 0 auto;
	max-width: var(--max-content-width);
}

/* Media queries
-------------------------------------------------------------------------------*/

@media screen and (min-width: 30rem) {
	
	.brochure-header-title {
		--header-font-width: 600;
		word-spacing: normal;
	}
	
	.brochure-section {
		padding: 2rem;
	}
	
}

@media screen and (min-width: 40rem) {
	
	.brochure-header-title {
		--header-font-width: 700;
	}

	.brochure-section {
		padding: 2rem 1rem;
	}

	.brochure-nav-toc {
		column-count: 2;
		column-gap: 2rem;
		margin: auto;
		max-width: var(--max-content-width);
	}
	
	.brochure-section-grid-content {
		display: grid;
		grid-column-gap: 1.5rem;
	}
	
	.brochure-section-three-up {
		grid-template-columns: repeat(3, 1fr);
	}
	
	.brochure-section-three-up .brochure-section-story-module {
		margin-right: 0.5rem;
	}
	
	.brochure-section-two-up {
		grid-template-columns: repeat(2, 1fr);
	}	
	
}

@media screen and (min-width: 50rem) {
	
	.brochure-section {
		padding: 3rem 0;
	}
	
	.brochure-section-alert {
		margin: 2rem auto 1rem;
		max-width: var(--max-content-width);
	}
		
}
</style>

<div class="wrapper">

	<header class="brochure-header">

		<h1 class="brochure-header-title">OpenType Font Variations</h1>

	</header>
	
	<article>
		
		<section class="brochure-section">
			
			<h2 class="brochure-section-header">Contents</h2>
			
			<nav class="brochure-nav-toc">
	
				<ol>
					<li><a href="#introduction">Introduction</a></li>
					<li><a href="#variable-fonts-historical-context">Variable fonts: historical context</a>
						<ol>
							<li><a href="https://www.typenetwork.com/news/article/when-lines-roamed-the-earth/preview">When lines roamed the earth</a></li>
							<li><a href="https://www.typenetwork.com/news/article/when-line-to-curve-to-ruled-the-world/preview">When Line-to Curve-to ruled the world</a></li>
							<li><a href="https://www.typenetwork.com/news/article/when-fonts-started-a-new-world/preview">When fonts started a new world</a></li>
						</ol></li>
					<li><a href="#variations-font-advantages">Advantages of variable fonts</a></li>
					<li><a href="#opacity">Opacity</a></li>
					<li><a href="https://www.typenetwork.com/news/article/colophon/preview">Colophon</a></li>
					<li><a href="#variable-font-amstelvar">Variable font: Amstelvar</a></li>
					<li><a href="#variable-font-decovar">Variable font: Decovar</a></li>
				</ol>
	
			</nav>
			
			<div class="brochure-section-alert">
				<h3>This page uses Variable Fonts!</h3>
				<p>To see the page as intended, follow these instructions to download and configure a compatible browser.</p>
<h4>Chrome</h4>
<ol><li>Download <a href="https://www.google.com/chrome/browser/canary.html">Chrome Canary</a>.</li>
<li>Go to the URL <b>chrome://flags</b></li>
<li>Enable “Experimental Web Platform Features”</li></ol>
<h4>Firefox</h4>
<ol><li>Download <a href="https://www.mozilla.org/firefox/channel/desktop/">Firefox Developer Edition</a> (recommended) OR <a href="https://www.mozilla.org/firefox/channel/desktop/">Firefox Nightly</a>.</li>
<li>Go to the URL about:config</li>
<li>Set <code>layout.css.font-variations.enabled</code> to <b>true</b>.</li>
<li>Set <code>gfx.downloadable_fonts.keep_variation_tables</code> to <b>true</b>.</li>
<li>Set <code>gfx.downloadable_fonts.otl_validation</code> to <b>false</b>.</li></ol>
			</div>
			
		</section>
		
		<section id="introduction" class="brochure-section brochure-section-alt-one">

			<h2 class="brochure-section-header">Introduction</h2>
				
			<p class="brochure-section-introduction">We're excited to present the second installment of our publications related to Variable Fonts. In our first installment, the stories of Amstelvar and Decovar, we began working with variable fonts, imagining, designing, and producing them. Since then, we’ve got browsers and web code, and so we’ve started using them. So naturally, thinking and writing about variations in the context of history and the future can’t be far behind...</p>
		
		</section>
		
		<section id="variable-fonts-historical-context" class="brochure-section">
			
			<h2 class="brochure-section-header">Variable Fonts: Historical Context</h2>
			
			<div class="brochure-section-content brochure-section-grid-content brochure-section-three-up">
	
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<a href="https://www.typenetwork.com/news/article/when-lines-roamed-the-earth/preview"><img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_STRY_typecase.jpg" alt="Type Case"></a>
					</div>
					
					<div class="brochure-section-module-content">
						<p class="brochure-section-module-slug">Chapter i</p>
						<h3 class="brochure-section-module-title"><a href="https://www.typenetwork.com/news/article/when-lines-roamed-the-earth/preview">When lines roamed the earth</a></h3>
						<p class="brochure-section-module-deck">Not very much of letterpress may seem virtual to us today, but the Gutenberg invention of separating the formation of letters from the document they were formed on was a step toward abstraction. Otmar Mergenthaler’s Linotype machine added a second layer of virtuality to type, especially text type, to serve the needs of a new kind of immediacy demanded in the second half of the 19th century.</p>
						<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/news/article/when-lines-roamed-the-earth/preview">Read More</a></p>
					</div>
					
				</div>
				
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<a href="https://www.typenetwork.com/news/article/when-line-to-curve-to-ruled-the-world/preview"><img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_STRY_matrix.jpg" alt="Font Matrix"></a>
					</div>
					
					<div class="brochure-section-module-content">
						<p class="brochure-section-module-slug">Chapter ii</p>
						<h3 class="brochure-section-module-title"><a href="https://www.typenetwork.com/news/article/when-line-to-curve-to-ruled-the-world/preview">When Line-to Curve-to ruled the world</a></h3>
						<p class="brochure-section-module-deck">The transition between analog methods and Desktop PC with PostScript, is sometimes called the “Propriety Age” of graphic design — the fonts were digital, but the equipment they were used on was still a mishmash of proprietary, mutually incompatible industrial machines.</p>
						<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/news/article/when-line-to-curve-to-ruled-the-world/preview">Read More</a></p>
					</div>
					
				</div>
				
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<a href="https://www.typenetwork.com/news/article/when-fonts-started-a-new-world/preview"><img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_FPO.png" alt="Font Matrix"></a>
					</div>
					
					<div class="brochure-section-module-content">
						<p class="brochure-section-module-slug">Chapter iii</p>
						<h3 class="brochure-section-module-title"><a href="https://www.typenetwork.com/news/article/when-fonts-started-a-new-world/preview">When fonts started a new world</a></h3>
						<p class="brochure-section-module-deck">The advent of variable fonts means <i>doing nothing,</i> or <i>everything,</i> or <i>something in between</i> for font users and type designers. Superficially, everything that worked before, works now. All existing fonts retain their quality, functionality and performance, but deep down, OpenType variations technology can change everything about type. Here we’re putting this historic development into some perspective, looking both backward at how type technology has evolved, and forward toward where the new tools may take us...</p>
						<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/news/article/when-fonts-started-a-new-world/preview">Read More</a></p>
					</div>
					
				</div>
				
			</div>
			
		</section>
		
		<!-- 3. Variations Font Advantages -->
		
		<section id="variations-font-advantages" class="brochure-section brochure-section-alt-one">
			
			<h2 class="brochure-section-header">Variations Font Advantages</h2>
				
			<div class="brochure-section-content brochure-section-grid-content brochure-section-two-up">
	
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_adv_one.svg" alt="Improved functionality">
					</div>
					
					<div class="brochure-section-module-content">
						<h3 class="brochure-section-module-title">Improved performance and functionality</h3>
						<p class="brochure-section-module-deck">The technology of OpenType Variations improves the performance and functionality of an existing library or repertoire of fonts, converting it into a smaller number of smaller files with exactly the same functionality, less file herding, and the benefits of interpolation on the fly by the operating system for unlimited sizes, weights, and widths.</p>
					</div>
					
				</div>
				
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_adv_two.svg" alt="FPO">
					</div>
					
					<div class="brochure-section-module-content">
						<h3 class="brochure-section-module-title">Responsive typography on the fly</h3>
						<p class="brochure-section-module-deck">With nearly every parameter that exists in traditional fonts becoming a variable, type can now respond to variations in layout with harmonious variations of its own, specified at the same granularity as responsive typography used in responsive design.</p>
					</div>
					
				</div>
				
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_adv_three.svg" alt="FPO">
					</div>
					
					<div class="brochure-section-module-content">
						<h3 class="brochure-section-module-title">Development of fonts for multiple languages and writing systems</h3>
						<p class="brochure-section-module-deck">In international typeface development or acquisition and deployment, variable fonts can smooth out the appearance of mixed scripts, like Chinese and Latin, or properly align a sans serif variable font with a particular emoji, or a logo.</p>
					</div>
					
				</div>
				
				<div class="brochure-section-module">
					
					<div class="brochure-section-module-image">
						<img class="brochure-section-module-thumb" src="/assets_content/brochures/TN_OFV_adv_four.svg" alt="FPO">
					</div>
					
					<div class="brochure-section-module-content">
						<h3 class="brochure-section-module-title">Fewer use issues with fonts</h3>
						<p class="brochure-section-module-deck">In editorial, in design, in production, and among readers, OpenType variable fonts simplify the way fonts work and make them easier to use, with fewer complications.</p>
					</div>
					
				</div>
				
			</div>
			
		</section>
		
		<section id="opacity" class="brochure-section">
			
			<h2 class="brochure-section-header">Opacity</h2>
			
			<div class="brochure-section-content">

				<a href="#"><img class="brochure-section-font-animation" src="/assets_content/brochures/TN_OFV_opacity.svg" alt="Opacity Illustration"></a>

				<p class="brochure-section-introduction">In the beginning of digital outline fonts, people were not quite sure whether the line being drawn was opaque or transparent. In analog type development, the punchcutter, and later the letter-drawer whose work drove puchcutting machinery, first created a transparent, or white, line around the opaque or black, and then cut away what would be white, leaving the punch ready to make impressions in softer metal, called matrices, into which lead could be poured to make printable letters.</p>
				
				<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/news/article/opacity-for-all/preview">Read the full essay</a></p>
				
			</div>
			
		
		</section>
		
		<!-- 5. Variations Font Advantages -->
		
		<section id="variable-font-amstelvar" class="brochure-section brochure-section-alt-one">
			
			<h2 class="brochure-section-header">Variable font: Amstelvar</h2>
			
			<div class="brochure-section-content">
			
				<a href="https://www.typenetwork.com/brochure/opentype-variable-fonts-moving-right-along/"><img class="brochure-section-font-animation" src="/assets_content/brochures/TN_OFV_amstelvar-title.gif" alt="Amstelvar Animation"></a>
				
				<p class="brochure-section-introduction">After the announcement of OpenType variable fonts at ATypI Warsaw, Font Bureau took on an extreme font development challenge for Google: developing Amstelvar, a serif demo font that could demonstrate the possibilities inherent with the OpenType Font Variations. Amstelvar’s design axes have the ability to adjust, with extreme granularity, the black and white spaces that comprise the features controlling weight, width, size, x-height, and serif shape.</p>
				
				<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/brochure/opentype-variable-fonts-moving-right-along/">Read More about Amstelvar</a></p>
				
			</div>
		
		</section>
		
		<section id="variable-font-decovar" class="brochure-section brochure-section-alt-one">
			
			<h2 class="brochure-section-header">Variable font: Decovar</h2>
			
			<div class="brochure-section-content">
				
				<a href="https://www.typenetwork.com/brochure/decovar-a-decorative-variable-font-by-david-berlow"><img class="brochure-section-font-animation" src="/assets_content/brochures/TN_OFV_decovar-title.gif" alt="Decovar Animation"></a>
				
				<p class="brochure-section-introduction">David Berlow developed Decovar, a multistyle decorative variable font, at Google’s request, to show off how a single display font could change its appearance in dramatic ways within a single interpolation space. Decovar sports three variation axes for its underlying skeleton, and seven for its terminals, which together give it a mind-blowing amount of visual variety.</p>
				
				<p class="brochure-section-module-link"><a href="https://www.typenetwork.com/brochure/decovar-a-decorative-variable-font-by-david-berlow">View the Interactive Brochure</a></p>
				
			</div>
		
		</section>

	</article>

	<div class="brochure-footer">

		<p>&copy; Copyright Type Network 2017. All Rights Reserved.</p>

	</div>

</div>