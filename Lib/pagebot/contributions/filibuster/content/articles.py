# -*- coding: UTF-8 -*-
#
"""
        history
        Article pieces
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""

__version__ = '4.0'



content = {

    '_headline': ['<#news_headline#>',],
    '_section': ['<#portal_anyshortname#>',],
    '_ankeiler': ['<#article_ankeiler#>',],
    '_summary': ['<#article_summary#>',],

    'creditarticle' : ['<p class="writer"> <#article_writer#></p><#article_content#> '],
    'article' : ['<#article_content#>'],
    'article_ankeiler': [
        '<#article_p1#> ','<#article_p2#> ','<#article_p3#> ',
        '<#article_p4#> ','<#article_p5#> ','<#article_p6#> ',
        '<#article_p7#> ','<#article_p8#> ','<#article_p9#> ',
        '<#article_p10#> ',
    ],
    'article_caption': [
        '<#^,article_p1#> ', '<#^,article_p2#> ', '<#^,article_p3#> ', '<#^,article_p4#> ',
        '<#^,article_p5#> ', '<#^,article_p6#> ', '<#^,article_p7#> ', '<#^,article_p8#> ',
        '<#^,design_sentence#> ', '<#^,design_sentence#> ', '<#^,design_sentence#> ',
        '<#^,odd_action#> ', '<#^,HEADLINE_market#> ', '<#^,politics_headline#> ',
    ],
    'article_shortcaption': [
        '<#^,com_bylines#> ', '<#^,odd_action#> ', '<#^,sports_section#> ',
        '<#^,portal_anyname#> ', '<#^,university#> ', '<#^,j_thing#> ', '<#^,i_host_edu#> ',
        '<#^,event_construct#> ', '<#^,name#> ', '<#^,realestate_shortheadline#> ',
        '<#^,book_headline#> '
    ],
    'article_summary': [
        '<p class="start summary"><#article_start#> </p><p><#article_p1#> <#article_p3#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p2#> <#article_p4#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p3#> <#article_p5#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p4#> <#article_p6#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p5#> <#article_p7#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p6#> <#article_p8#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p7#> <#article_p9#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#article_p8#> <#article_p10#> </p>',
        '<p class="start summary"><#article_start#> </p><p><#da_text#> <#article_p10#> </p>', # Fake design text once in a while.
    ],
    'article_shortsummary': [
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p1#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p2#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p3#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p4#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p5#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p6#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p7#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p8#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p9#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#article_p10#> </p>',
        '<p class="start shortsummary"><#article_start#> </p><p><#da_text#> </p>', # Fake design text once in a while.
    ],
    'article_deck': [
        '<#article_start#>',
     ],
    'article_content' : [
        u"""<p class="start"><#article_start#></p> <#article_paragraphs#> <p class="end"><#article_end#></p>""",
        u"""<p class="start"><span class="place"><#city#> (<#tv#>)</span> <#article_start#></p> <#article_paragraphs#> <p class="end"><#article_end#></p>""",
        u"""<p class="start"><span class="place">(<#tv#>)</span> <#article_start#></p> <#article_paragraphs#> <p class="end"><#article_end#></p>""",
    ],
    'article_paragraphs' : [
        '<p><#article_p1#> </p><p><#article_p2#> </p><p><#article_p3#> </p><p><#article_p4#> </p> <#article_pullquote#> <p><#article_p5#></p><p><#article_p6#></p>',
        '<p><#article_p1#> </p><p><#article_p3#> </p><p><#article_p5#> </p><p><#article_p6#> </p>',
        '<p><#article_p1#> </p><p><#article_p2#> </p> <#article_pullquote#> <p><#article_p3#> <#article_p5#></p>',
        '<p><#article_p3#> </p><p><#article_p4#> </p><p><#article_p6#> <#article_p9#> </p>',
        '<p><#article_p1#> </p><p><#article_p6#> <#article_p7#> </p><p><#article_p10#> </p>',
        '<p><#article_p2#> </p><p><#article_p3#> <#article_p4#> </p><p><#article_p7#></p><p><#article_p9#> </p><p><#article_p10#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> <#article_p3#> <#article_p4#> </p> <#article_pullquote#> <p><#article_p6#></p><p><#article_p7#></p><p><#article_p8#></p><p><#article_p9#></p>',
        '<p><#article_p1#> <#article_p2#> <#article_p3#></p><p><#article_p5#> </p><p><#article_p6#> </p><p><#article_p7#> <#article_p8#> <#article_p10#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> <#article_p3#> <#article_p5#> </p> <#article_pullquote#> <p><#article_p6#> <#article_p8#></p><p><#article_p9#></p><p><#article_p10#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> <#article_p3#> <#article_p5#> </p> <#article_pullquote#> <p><#article_p6#></p><p><#article_p8#> <#article_p9#></p><p><#article_p10#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> <#article_p3#> <#article_p4#> </p><p><#article_p5#> </p><p><#article_p6#></p><p><#article_p8#> <#article_p9#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> <#article_p3#> </p><p><#article_p4#></p><p><#article_p7#></p><p><#article_p8#></p><p><#article_p9#></p><p><#article_p10#></p>',
        '<p><#article_p1#> </p><p><#article_p2#> </p><p><#article_p3#> </p> <#article_pullquote#> <p><#article_p4#></p><p><#article_p7#></p><p><#article_p8#></p><p><#article_p9#></p><p><#article_p10#></p>',
    ],
    'article_writer': ['By <#name#>'],
    'article_pullquote': [
        '<blockquote class="pullquote"><#^,review#></blockquote>',
        '<blockquote class="pullquote"><#^,quotation#></blockquote>',
        '<blockquote class="pullquote"><#^,quotation#></blockquote>',
    ],
    'article_start': [
        u'<#^,medical_headline#>',
        u"""The tiny island nation of <#towns_USgeneric#> is one of the most isolated, troubled and beautiful places on the planet.
        Once one of the wealthiest places on the globe, today it’s now one of the poorest. What happened?""",
        u"""<#tv#> Report blog: Who is <#name#>?""",
        u"""The long-awaited golf showdown between President <#names_first#> and House Speaker <#name#> is underway:
        The pair, along with with Vice President <#name#> and GOP <#state_name#> Gov. <#name#>, hit the links around <#time_workhours#> <#time_days#> at <#city#>.""",
        u"""<#tv#>’s schedule: “Online Warriors of the <#nationality_major#> Spring,” premieres <#time_days#>, <#time_months#> <#time_monthdays#>,
        <#time_workhours#>. It will re-air <#time_days#>, June <#time_monthdays#>, at <#time_workhours#> and <#time_workhours#>""",
        u"""Routers and <#j_adjective#> network-enabled laptops can link together to form a network enabling individuals to send messages along these
        linked “nodes” to create a local system that allows individuals within a group to communicate.""",
        u"""Speak to Tweet is a joint project between <#i_socialmedia#> and <#i_socialmedia#> that was first used during the <#nationality_major#> revolution when the
        <#names_last#> regime shut down access to the Internet.""",
        u"""A computer problem that grounded <#air_carrier#> flights across the country has been repaired, the airline announced early <#time_days#>.""",
        u"""A viral <#j_adjective#> video showing <#num_card_multiple#> men horsing around in an empty airport is getting a lot of laughs and attention online but also
        raising questions about security at <#cities_USmajor#> International Airport.""",
        u"""“My father’s chosen career was carpentry. For as long as I can remember I watched him build things and dedicate himself to his craft.
        He built my childhood home, the kitchen cabinets within and even my pinewood derby car.”""",
        u"""One summer I worked with him on one of his jobs and that was a pivotal moment in understanding the concept of craftsmanship.
        I marveled at the pride he took in his work.”""",
        u"""Granted my craft is different, the same pride and attention to detail goes into what I do today and have my whole career.
        My father made me a wooden knife block seven years ago when I was at Per Se; it is now in my kitchen in <#cities_USmajor#>,
        and every time I grab for one of my knives, I think of him.""",
        u"""“We have some very delicate china in <#cities_USmajor#> and my father created beveled oak boxes for the different pieces.
        It is a nice way that we have bridged our <#num_card_multiple#> specialties.”""",
        u"""“While my father worked for <#time_age#> years, he instilled in me that there is more to life than just work.
        What mattered most was creating something you are proud of that will endure, create memories and bring joy to others.”""",
        u"""“While I am not creating something that will last the tests of time in a physical sense at the restaurant,
        my goal with each dish, with each dining experience is to bring joy to our guests and create a memory to remember.”""",
        u"""“It was my dream when I was a culinary arts student to become a chef. I knew my end goal was to work with <#nationality_major#>
        cuisine in <#cities_USmajor#>. Chef <#names_last#> has been one of my greatest supporters and encouraged me 1<#figs#> years
        ago to challenge myself, move to <#cities_USmajor#> and work there.”""",
        u"""With his help I worked in <#cities_USmajor#> restaurants and eventually had the opportunity to spearhead Per Se.
        When I decided to step away from Per Se and take on this new challenge of opening the restaurant, he was there again to support me.""",
        u"""It’s one thing to hear waves lap the shore of a nearby beach, quite another to hear them rumbling beneath you while you sleep.""",
        u"""Welcome to the world of the “floating hotel” – encompassing all manner of lodgings built on floats, boats, rafts or even stilts.""",
        u"""Escorted within the pristine Great Rainforest on the scarily remote western coast of <#country#>, the
        lodge is in fact a towering four-decker barge towed to the harbor of <#island#> every year from <#time_months#> to <#time_months#>."""
        u"""The “<#mountain#>” hovers across a mile-long coast of coral reef and is accessible only by a <#figs_rand_2digit#>-minute boat
        ride from the nearest town on the rather unfortunately named <#island#>."""
        u"""Lab analyses showed that this influenza virus was genetically and antigenically very different from other influenza viruses circulating among people.""",
        u"""Epidemiological information provided by <#country#> demonstrated person-to-person transmission.""",
        u"""Clinical information, especially from <#country#>, indicated this virus also could cause severe disease and death.""",
        u"""At the time, those reports did not indicate a pandemic situation, but taken together sent a very strong warning to WHO and other public health authorities to be ready for one.""",
        u"""As the pandemic evolved, clinicians identified a very severe form of primary viral pneumonia, which was rapidly progressive and frequently fatal.""",
        u"""On <#time_date#>, WHO reported lab confirmed cases in <#figs_rand_2digit#> countries.""",
        u"""<#nationality_major#> government vows to hold oil city.""",
        u"""<#figs_multiple#> scenarios for <#country#> after <#name#>""",
        u"""Phone-hacking scandal.""",
        u"""Hacking whistle-blower found dead.""",
        u"""<#names_first#>'s Sun paper hit by hackers.""",
        u"""Hacking scandal's far-reaching tentacles.""",
    ],
    'article_binder':['Meanwhile,','On the other hand,','Also,','Ignoring the fact that','This enhances the idea that','Furthermore,',
        'Considering the fact that', 'Maybe that is true, but', '<#article_question#> It seems a valid assumption, but',
        'Additionally,','But who could have thought that','But who could never have assumed that','On another level',
        'This contradicts the general assumption that','As mentioned before,','As stated,','As previously discussed,',
        'Not ignoring the fact that','Unfortunately,','On the contrary,','Although','Despite the fact that',
        '<#article_question#> By following the path that','Still,','Starting in <#time_months#>,','Ending in <#time_months#>,',
        'Starting in a couple of weeks,','Lasting for a while,','It went as predicted,','With the same state of mind','Accordingly to that,',
        'It happened as expected,','The subject seems harmless enough. But with closer investigation','With the given situation that',
        '<#article_question#> Watching the subject from a different perspective,','Not underestimating',
    ],
    'article_question': ['How can we achieve that?','What about it?','How to deal with that fact?','How to increase that awareness?',
        'How to get there?','Wondering how?','What are the implications of that?','And why?','Why?','Does that happen often?',
        'Can you elaborate on that?','What does that phrasing mean?','Would it happen again?', 'What if there is no such thing?',
    ],
    'article_p1': [
        u"""The 12-hour lay-over in <#country#>’s <#city#> International Airport is a whiz-bang.
        I find myself shopping for crystal unicorns and staring at duty-free liquor.
        Two entire shifts of employees come and go while I down <#amount_small#> shots of espresso.""",
        u"""The game was first suggested by then-White House Press Secretary <#name#> shortly after Republicans officially
        took control of the House in <#time_months#>. <#names_last#> signed on that month, saying he’d be happy to play 18 holes with the president -
        although, he told one interviewer, he was "sure I'll have to give the President 18 strokes!""",
        u"""Political revolutions in <#country#> and <#country#> not only inspired other regional uprisings – they sparked a
        flurry of ideas about how to help revolutionaries better communicate when their governments pull the plug on the World Wide Web.""",
        u"""If one individual within the <#j_adjective#> network is able to connect to the outside world, that person can share
        the connection with others on the network.""",
        u"""<#article_binder#> protesters in <#country#> call for the return of the Internet on <#time_months#> 1st after the government shut it down.""",
        u"""The <#cities_USmajor#>-based airline blamed the computer malfunction on "a network connectivity issue" <#time_days#> night.""",
        u"""The clip, called "STUCK," was posted this week on <#i_host_users#> by a user identifying himself as <#name#>.""",
        u"""With his unending support I had the courage to make the big moves in my career, and I always had a clear vision of where I wanted to end up.”""",
        u"""Often only accessible from the sea, these so-called “floatels” are the sailing equivalent of a roadside inn, only much cooler.""",
        u"""But <#name_male#> also urged <#legal_professions#> to set up an oversight council, and makers to set up an of monitoring and addressing
        systematic risks “may exceed the capacity of any individual supervisor.”""",
        u"""For Gov. <#name_female#> of <#town_us#>, the challenges of the coming year could clinch her reputation as a political superstar—or puncture it.""",
        u"""The neighborhood has emerged as a launching pad for all kinds of immigrants, not just <#nationality_major#>, who are seeking a
        foothold on the economy’s bottom rung.""",
        u"""For <#figs_rand_3digit#> students in <#town_us#>, some of whom may be unable to see or move, the <#town_us#> School has long served as a refuge.""",
        u"""<#name_female#> is often on patrol in the Mount <#county_US#> section of the borough, calling the city’s
        <#figs_nonzero#><#figs#><#figs#> line about a pothole, an abandoned vehicle or a missing stop sign.""",
    ],
    'article_p2': [
        u"""<#article_binder#> <#^,company#> goes behind the scenes of the world’s major transport hubs, revealing the logistics
        that keep goods and people moving.""",
        u"""<#name#>, founder of <#^,news_company#>, has a plan to give freedom-seeking individuals the ability to link up
        and form their own life raft to “make what no government can ever block.”""",
        u"""<#article_binder#> the new <#j_adjective#> network technology is not new, nor is it the only work-around to disabled wireless and Internet communications.""",
        u"""U.S. Secretary of State <#name#> said restrictions on Internet activity that prohibit free expression are among the most worrisome trends concerning human rights.""",
        u"""<#article_binder#> the problem, "was resolved through troubleshooting procedures and restored at midnight," wrote <#air_carrier#> spokesman <#name#> in an e-mail to <#tv#>.""",
        u"""<#article_binder#> long lines of people could be seen at airports in cities across the country, including <#cities_USmajor#>, <#cities_USmajor#> and
        <#cities_USmajor#>. Many passengers sat on the floor as they waited.""",
        u"""“While on our way home from Formula Drift <#towns_USgeneric#>, <#name#> and I found ourselves stranded over night in the
        <#cities_USmajor#> International Airport as our flights home were canceled. The following is a brief summary of the events that took
        place that night,” the user writes.""",
        u"""<#names_last#> is now an executive chef in his own right at his first solo project, The <#event_type#> Restaurant, in <#city#>.""",
        u"""“<#^,num_card_010_019#> years ago I started working for <#names_first#> at <#town_us#> Tavern. He taught me about the importance of
        sourcing local ingredients and supporting local farmers, producers and purveyors, before it was widely popular.""",
        u"""<#article_binder#> facing out onto the <#sea#> with the <#country#> Rainforest on its tail, the lodge consists of nine immaculately crafted
        huts carefully balanced over the water on thin but, we’re assured, sturdy wooden stilts.""",
        u"""<#article_binder#> developed with the eco-conscious traveler in mind, the “<#mountain#>” Resort is built from local materials – with thickly-layered
        palm-leaf roofs – is powered entirely by solar energy, has its own sewage-treatment plant, and protects <#figs_rand_3digit#> acres of rain and
        mangrove forest into the bargain.""",
    ],
    'article_p3': [ # Still __empty tag__ error in this one
        u"""It’s <#figs_nonzero#><#figs#> hours from <#state_name#> to <#country#>, then one more flight to <#towns_USgeneric#>.
        Where? Exactly. <#island#> a tiny island nation about <#figs_rand_3digit#> miles from eastern <#country#>.
        It’s in the deepest part of the <#ocean#>, beyond <#air_crashsites#>, beyond <#towns_USgeneric#>. If the world were flat, this might be the last stop before you fell off.""",
        u"""Ever wondered how long it takes from the time a rose grower cuts the stem in <#country#> to when it hits the stalls at your local florist?
        Or how cocoa from <#continents_parts#> ends up in <#city#>’s port warehouses, ready for distribution to <#continents#>’s chocolate makers? The Gateway reveals all.""",
        u"""But <#names_last#> and fellow tech entrepreneur <#name#> are providing a space where online activists in the world’s hot spots can come together to share their ideas.""",
        u"""Yet as governments become more savvy in their attempts to repress freedom of expression on the Internet,
        their citizens have become cyber-sleuths, creating innovative technologies to circumvent censors and authorities tracking their Internet activities.""",
        u"""<#article_binder#> <#^,company#> is an innovative, 21st-century technology company. So why is its stock trading at a valuation similar to companies from an industry that had its roots in the early 1800s?""",
        u"""“The airline issued a waiver policy permitting customers on affected flights to cancel or rebook their itineraries without penalty,”
        <#names_last#> said. “<#air_carrier#> apologizes for the disruption caused to travelers at affected airports and is re-accommodating travelers where necessary.”""",
        u"""<#article_binder#> the video shows the men racing through airport’s empty terminal corridors in airport wheelchairs while a janitor who is vacuuming gives them a puzzled look.""",
        u"""“<#cities_USmajor#> Airport, together with its security partners, maintains a high level of security at all times, and at no time did the filmmakers’
        activities present any level of danger or threat to flight safety. And by the way, they also picked up after themselves, including the restroom.”""",
        u"""The video did point out the need to better secure the restaurant seen in the clip, and that issue is being addressed immediately, the airport said.""",
        u"""<#article_binder#> a member of airport’s board of directors expressed unease about the prank to <#tv#> affiliate local <#tv#> in <#cities_USmajor#>.""",
        u"""<#article_binder#> chef <#name#> has worked in the kitchens of culinary notables like <#name#> and <#name#>, and he willingly acknowledges the
        lessons he learned from them have been integral in his own success - from <#name#> Awards to a “Best New Chef” title.""",
        u"""He stressed the importance and responsibility for finding a use for every part of an animal or fish.
        <#names_first#> had an artisanal cheese program at <#towns_USgeneric#> that featured over <#num_card_010_090#> cheeses.""",
    ],
    'article_p4': [
        u"""<#towns_USgeneric#> first hit my radar as the last country that <#tv#> report waited on to complete <#newspapers#>,
        a race to net a story from every nation on the planet.""",
        u"""<#article_binder#> it was impressive then to see the <#age_worker#>-year-old <#names_last#> has so far shown no signs of scar tissue from <#names_first#>.
        Playing alongside <#name#>, who had his own disaster in this very event last year, and the five-time runner-up <#name#>,
        the grouping is made for TV. But while the other <#num_card_multiple#> got beaten up by the course, <#names_last#> managed
        to hit 17 out of 18 greens, dropping no shots, and accumulating <#num_card#> birdies.""",
        u"""<#article_binder#> a regime-changing wave of protests started in <#country#>, inspired by demonstrators in neighboring
        <#country#> who ousted their president in a popular uprising.""",
        u"""<#article_binder#> activists in <#country#> and <#island#> told <#tv#> about five technologies that have been most useful in getting around government-imposed blockades.""",
        u"""<#article_binder#> the computer malfunction brought <#air_carrier#>’s system of scheduling departures, reservations and processing passengers
        to a halt at airports across <#country#>. The problem left passengers stranded for hours in grounded planes, airport lobbies and security lines.""",
        u"""<#article_binder#> <#name#> and his wife, <#name_female#>, became stranded at <#cities_USmajor#> International Airport while
        waiting on a connecting flight to <#cities_USmajor#>.""",
        u"""<#article_binder#> they also try out the public address system at <#air_carrier#> Gate A<#figs_rand_2digit#> and pound the keyboard of one of its computers.
        One of the men even does a handstand in the background. They throw soap at each other in a bathroom and spin on the moving handrails of escalators.""",
        u"""At the restaurant, we are working with a cuisine so firmly rooted in tradition and history, that we focus on not fussing,
        manipulating or changing but buying the best that we can and treating the ingredients with respect.""",
        u"""“Many of our menus highlight the farms/purveyors we are sourcing from, because our relationship is of such value to us in the kitchen.
        Without their products we cannot do what we do.”""",
        u"""Highlight: <#animals#> sneaking up to your veranda to share your breakfast in the morning.""",
    ],
    'article_p5': [
        u"""Soon, <#towns_USgeneric#> will also hold the chair of the U.N. Alliance of Small Island States, a group of
        <#figs_nonzero#><#figs#> countries working together to slow climate change.""",
        u"""<#article_binder#> assessing his performance, the <#nationality_major#> was keen not to get carried away by this opening effort:
        “I don’t think conditions were that easy. I just managed to keep the ball in the fairway and find a lot of greens,
        and that was basically how I shot that score.” Golf commentators were not quite as circumspect, with conversations
        on  <#i_host_users#>’s forums speculating a new era of <#name#>-like dominance is starting.""",
        u"""The <#politics_euro_nationality#> government shut down the Internet for <#num_card_010_019#> days during the protests,
        so <#nationality_major#>s used satellite connections, dial-up modems and land lines to call Internet service
        providers in other countries to get online.""",
        u"""<#article_binder#> <#^,tonic_disorders#> is a circumvention tool that allows users to access censored information online, by bouncing communications among
        a network of users around the world, ultimately enabling its users to maintain anonymity online.""",
        u"""<#article_binder#> the application allows individuals to call a phone number and leave a voice mail, which is automatically
        translated into a tweet with a hashtag from the country of origin.""",
        u"""<#name#>, who was on an airplane at <#cities_USmajor#> when the problem occurred, said it became apparent
        something was wrong as the flight was taxiing.""",
        u"""But in one of the video’s most talked-about scenes, they enter a closed restaurant, and one of the men appears
        to pour himself a glassful of beer on tap, which he drinks in one gulp. The <#num_card_multiple#> men do not face any legal
        trouble, <#names_last#> added.""",
        u"""The kitchen at <#towns_USgeneric#> was at that time, and still is to this day, an amazing school for young chefs not
        only for their technique but also on the relationships behind each dish. That same philosophy exists in the dining room.""",
    ],
    'article_p6': [
        u"""It’s a new role for <#towns_USgeneric#> and its <#figs_nonzero#><#figs#>,000-some inhabitants.
        They’ll be the voice of places like <#island#> and <#island#>, tiny islands that might well be erased by rising oceans;
        tiny islands trying to make the case to the world at large to cut emissions and extend the <#country#> Protocol, lest the ocean swallow them up.""",
        u"""Bear in mind how difficult the set-up of a typical <#cities_UK#> Open course is, typically lengthened to over <#figs_rand_4digit#>
        yards and change, with narrow fairways, punishing rough and fast greens with tricky pins and then consider how
        it was reduced by <#names_last#> as he went in search of birdies, according to <#paper_financial#>.""",
        u"""<#^,tonic_disorders#> technology would have enabled those connected to share their connections along the network.""",
        u"""<#article_binder#> the program has also been used in <#country#>. You can listen to the messages on <#i_socialmedia#> through @speak2tweet.""",
        u"""HTTPS Everywhere encrypts communications between its users and major websites, including <#i_socialmedia#>.
        The <#^,p_technologies#> extension was created by the <#^,news_company#> Project and the Electronic <#p_technologies#> Foundation.""",
        u""""We were on the runway when the pilot came on the P.A. and said they had lost contact with the company
        computer system which measured the weight of the plane," <#names_last#> said.""",
        u""""We’re pretty easy going people. We travel a lot. We understand that problems happen," <#name#> told <#tv#>.
        “I just think there would be a little more information. All they say is ‘we have a computer problem.’
        By the time you get to hour three, it gets a little frustrating.”""",
        u"""<#towns_USgeneric#> Tavern will always be the benchmark <#cities_USgeneric#> restaurant for me.”""",
        u"""<#article_binder#> the <#sea#> Hotel contrasts the extreme wilderness on its back door with the extraordinary luxury of its interior.""",
    ],
    'article_p7': [
        u"""A U.N. climate change panel in <#time_lastyear#> estimated the sea level would rise more than half a meter by <#time_nextyear#>,
        but recent reports have indicated that ice sheets may be melting even more quickly, threatening places like <#island#>,
        where most of the population lives in a low-lying band around the perimeter of the island.""",
        u"""“I birdied the <#num_ord#> hole, hit a <#figs_nonzero#>-wood and a sand wedge just like, I don’t know, <#num_card#> feet past the hole (<#figs_rand_3digit#> yards).” <#name#> explained.""",
        u"""“I birdied <#amount_small#>. I hit a <#figs_nonzero#>-iron and an <#figs_nonzero#>-iron to ten feet (<#figs_rand_3digit#> yards).” <#name#> explained to the reporter.""",
        u"""“Then I birdied the <#num_ord#>, hit a driver and an <#figs_nonzero#>-iron pin high left about <#figs_nonzero#>, <#figs_rand_2digit#> feet, holed that <#figs_rand_3digit#>.” <#name#> explained.""",
        u"""“Then hit a <#figs_nonzero#>-wood and a lob wedge into the 1st to six feet (<#figs_rand_3digit#> yards).” <#name#> explained.""",
        u"""“I birdied the <#num_ord#>, hit a driver and a wedge to four feet just above the pin (<#figs_rand_3digit#> yards!).” he told reporters.""",
        u"""“Birdied <#figs_nonzero#>, I hit a driver and a 3<#figs_nonzero#>-iron just to the back fringe maybe <#figs_rand_2digit#> feet and
        two-putted that (<#figs_rand_3digit#> yards with water on the right of the green!)," he told reporters.""",
        u"""<#article_binder#> by enabling groups of individuals with the physical hardware to work around any state-imposed firewall,
        <#names_last#> plans to give freedom-seeking people the tools to “eradicate dictatorships” throughout the planet.""",
        u"""<#names_last#> and <#names_last#> are automotive photographers who had $<#figs_rand_2digit#>,000 worth of camera equipment
        with them when they were stuck so they decided to make the most of it, according to <#i_host_users#>,
        a website that covers the automotive industry and interviewed the men.""",
        u"""“<#name#> has been an amazing mentor for young chefs and restaurateurs coming up in the business over the last <#num_card_few#> decades.
        He has been influential in reviving neighborhoods through restaurants, food carts and local charity events.""",
        u"""Built in the local Mon style in the bosom of a tropical forest, the accommodation is set across <#amount_more#> floating wings, with
        <#figs_rand_2digit#> bamboo twin-rooms perched on each.""",
        u"""The “floatel,” which opened in 19<#figs_rand_2digit#>, has no electricity – so the rooms are all “romantically” lit with traditional oil
        lamps and cooled by the river flowing beneath."""
    ],
    'article_p8': [
       u"""In a lot of ways, <#island#> is something like a canary in a coal mine: It’s a tiny place with more than
       its share of troubles, most of them the kind that might have been prevented. <#island#> is battling a failed economy,
       widespread poor health and a natural environment ruined from the inside. They’re the kinds of things that aren’t altogether
       different from what’s facing many of the rest of us, but they’re magnified in a place that’s only a <#num_ord_010_019#> the size of <#state_name#>.""",
       u"""<#names_last#> revealed that <#name#> wanted to "kick his backside" after the implosion at the Masters, maybe come
       <#time_days#> the former great will be wanting to pat <#names_last#> on the back following a famous win...""",
       u"""<#article_binder#> many hard-line governments will attempt to drown out dissent by controlling the Internet with kill switches and
       firewalls. But with a phone – or a $<#figs_rand_2digit#> router the size of one – an individual can link to thousands of others,
       creating a private <#j_adjective#> network harnessing the firepower of the Internet. """,
       u"""Additionally, the report says, although <#^,company#> provides privacy, it does not give its users “full anonymity,
       since the proxy server will log all client activity.”""",
       u"""“It was definitely the most fun I’ve had in this place," <#names_last#> told the site. “I wasn’t actually going out to steal beer,”
       he said in reference to the restaurant scene. “I washed the cup and put it back in the fridge. I wanted to leave no trace.
       I didn’t want to cause any trouble. Next time we go to that airport I’ll get a beer and leave a $<#figs_rand_2digit#> tip.”""",
       u"""<#article_binder#> venture from one of its <#figs_rand_2digit#> palatial bedrooms – each with huge beds and stand-alone baths –
       out into a surrounding area bustling with <#animals#>."""
    ],
    'article_p9': [
       u"""If the Pacific <#island#>, it’d wash away one of the strangest and most troubled places on Earth. In my three days there,
       I met a cast of characters who would introduce me to the place.""",
       u"""It’s a grand slam of sorts already for <#name#> and the <#figs_rand_2digit#>th <#cities_UK#> Open has only just begun. With his imperious opening effort of
       <#figs_rand_2digit#> at <#cities_UK#> Country Club, he has now contended in all four Majors, and all in the space of the last <#figs_multiple#> months.
       Despite his notorious capitulation at this year’s Masters, here is a player moving to new level in his career.""",
       u""""I want to use technology to bring freedom to the Mideast," says <#names_last#>, one of <#figs_rand_2digit#> of <#name#>’s U.N.
       And <#names_last#>’s latest startup, <#^,company#>, would do just that.""",
       u"""It is obvious that can create a free community unbound by topographical and state barriers. <#^,num_card#> ways they got around the censors.""",
       u"""<#article_binder#> according to <#company#>, “Using HTTPS means that you are creating a more secure <#j_adjective#> channel over an unsecure <#j_adjective#> network,
       better protecting you from surveillance and eavesdropping. HTTPS encrypts the transmission, but NOT the content you are transmitting.”""",
       u"""<#names_last#> told <#tv#> less than a hour later that he and his wife were about to board a plane to <#cities_USmajor#>.""",
       u"""<#article_binder#> what he has done with putting his hand out and forging long-standing relationships with purveyors, local charities and even young
       members of the community is what I aim to do on a daily basis.""",
       u"""We have been purchasing in-season produce and much of our dairy products at the local greenmarket, which is just a block away from the restaurant.""",
    ],
    'article_p10': [
       u"""The <#cities_UK#> Open is designed to find you out, to level the playing field and offer a grueling slog, where level
       par is the desired winning number. We only have to recall <#name#>’s winning performance of <#num_card#> over par last year at
       <#cities_Spanish#> Beach and his grinding closing effort of <#figs_rand_2digit#> (three over par) to win the title, leaving <#name#>,
       <#names_first#>, <#names_first#> and <#names_first#> in his wake.""",
       u"""<#^,company#> involves the use of ad hoc wireless <#j_adjective#> network technology that mimics the survival instincts of fire ants:
       A single fire ant will drown in a pool of water. But if they link together, the ants can form a living raft and survive.""",
       u"""The crackdown on the Internet in <#continents_parts#> is hardly a new tactic to quell political dissent.""",
       u"""A recent Freedom House study found that about a third – <#figs_rand_2digit#> out of 100 – of the countries reviewed had
       “consistently or temporarily imposed total bans on <#i_socialmedia#> or equivalent services.”""",
       u"""The incident took place on <#time_months#> <#time_monthdays#> and involved those <#num_card_multiple#> men only, said <#name#>,
       manager of public affairs at <#cities_USmajor#> International.""",
       u"""<#article_binder#> it may appear they didn’t have any security around them, they were being watched, <#names_last#> said.""",
       u"""<#article_binder#> being on <#towns_USgeneric#> Center’s campus, we have had the pleasure of working alongside some of the most talented artists in the world.
       It has been our pleasure building <#j_adjective#> connections and <#j_adjective#> projects with the different constituents.”""",
       u"""<#article_question#> What are the most important lessons you have learned in the kitchen, and who taught you? Share your wisdom in the comments.""",
    ],
    'article_end':[
       u"""<#name#>, a "hacktivist" based in <#country#>, describes <#^,tonic_disorders#> as a program that enables you to
       “circumvent the central service of censorship by using a computer from someone else in the world.”
       It played a crucial role, he says, because social media pages sharing information about the protests were
       “systematically censored so you could not access them without censorship circumvention tools.”
       “So [<#^,tonic_disorders#>] was vital to get information and share it.”""",
       u"""<#article_binder#> <#^,company#> allows clients to bypass content filters. Unlike <#^,company#>, users do not have to download the program, but they need to
       be invited into the <#j_adjective#> network by another user, making the network hard for oppressive governments to infiltrate.""",
       u"""<#article_binder#> <#^,company#> Review of Censorship Circumvention Tools recommends this program for uploading and distributing
       materials when a high level of security and fast app speed are required.""",
       u"""<#article_binder#> <#names_last#> said the aircraft taxied around for nearly an hour and then returned to the gate for additional fuel.
       But passengers were not allowed to get off.""",
       u"""“It’s important to note that security agents observed the <#num_card_multiple#> filmmakers at several points during the making of the video.
       Because the filmmakers were presenting no threat to themselves, to others or to flight safety, and were causing no damage,
       there was no imperative to curtail their activities," <#names_last#> said in a statement.""",
       u"""“It’s not funny. It’s not going to happen again as far as I’m concerned. It should not have happened because it gives
       the perception the place is sitting out there unguarded and that’s why I was concerned, and am still concerned,” <#name#> told the station.""",
       u"""<#article_question#> Is there someone you’d like to see in the hot seat? Let us know in the comments below and if we agree, we’ll do our best to chase ’em down.""",
    ],
}
