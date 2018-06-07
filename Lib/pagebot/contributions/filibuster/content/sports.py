# -*- coding: UTF-8 -*-
#
"""
        history
        The World Of Sports
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading
4.0    -fixed names_japanese
evb
"""

__version__ = '4.0'


# ------------------------------------------------------
#    sports
#
content = {
        # TODO: Needs restore so club match is never against itself.
        'sports_section':    ['Sports', 'Sports', 'Sports', 'Sports', 'Sports', 'Sports',
                'Cup', 'Superbowl', 'The World of Sports', 'Guy Stuff', 'New sports',
                'Sports this week', 'Today', 'Finals <#time_thisyear#>', 'Local sports',
                'World Championship', 'Olympics', 'Olympics','Runner up', 'Champions',
                'Regatta', 'Winners', 'The Course', 'Semi-finals', 'Champs', 'Athletics',
                'Rowing', 'NBA', 'Baseball', 'Marathon', 'Sailing',
                ],
        'sports_headline':    [
                u'<#sportsheadline_us#>',
                u'<#sportsheadline_us#>',
                u'<#sportsheadline_us#>',
                u'<#sportsheadline_us#>',
                u'<#sportsheadline_us#>',
                u'<#sportsheadline_generic#>',
                u'<#sportsheadline_soccer#>'
                u"""<#sportsheadline_football#>""",
                u"""<#sportsheadline_football#>""",
                u"""<#sportsheadline_football#>""",
                ],
        'sports_blurb':    ['<#sportsheadline_us#>', '<#sportsheadline_us#>', '<#sportsheadline_us#>', '<#sportsheadline_us#>',
                '<#sportsheadline_generic#>', '<#sportsblurb_soccer#>'],
        'sports_ankeiler': [
                u"""<#^,sports_soccer_highlight#>""",
                u"""<#^,sportsheadline_us#>""",
                ],
        'sports_summary': [
                u'<#sports_soccer_highlight#>',
                u'<#sports_soccer_highlight#>',
                u'<#sports_soccer_highlight#>',
                u'<#sports_soccer_highlight#>',
                u'<#sports_soccer_roundoff#>',
                u'<#sports_soccer_roundoff#>',
                u'<#sports_soccer_roundoff#>',
                u'<#sports_soccer_roundoff#>',
                u"""<#name_male#> addressed a wide range of topics in a <#figs_rand_2digit#>-minute session with the news media on <#time_days#> morning.""",
                u"""<#amount_more#> of players and agents have taken to <#i_socialmedia#>, giving fans an unvarnished view of their thoughts.""",
                ],
        # football
        'sportsheadline_football':    [
                'The <#sportsteam_us#> vs. the <#sportsteam_us#>, the  won <#sports_victoryflavor#> with <-randint(40, 100)-> to <-randint(0, 39)->.',
                "<#sportsteam_us#>'s <#time_days#> victory over the <#sportsteam_us#>: <#sports_footballopportunity#>.",
                '<#sportsteam_us#> victory over the <#sportsteam_us#>:  <#sports_footballopportunity#>.',
                '<#sportsteam_us#> and <#sportsteam_us#>: not over yet.',
                '<#!bold, sportsteam_us#> <#sports_footballopportunity#>.',
                '<#!bold, sportsteam_us#> vs. the <#sportsteam_us#> cancelled.',
                '<#!bold, sportsteam_us#> coach named in <#politics_scandalnoun#>',
                '<#sportsteam_us#> coach <#!bold, names_last_patrician#> named in <#politics_scandalnoun#>',
                'Coach <#names_last_patrician#> quits after <#sportsteam_us#> loss.',
                '<#!bold, sports_league#>: <#sports_footballevent#> this <#time_days#>!',
                '<#sportsteam_us#> preparing for their upcoming <#!bold, sports_league#> <#sports_footballevent#> debut.',
                "<#sportsteam_us#>'s <#names_last#> injured.",
                ],
        'sports_football_match':    ['The <#sportsteam_us#> vs. the <#sportsteam_us#>'],
        'sports_league':        ['<#alphabet_caps#>FL', 'Pro<#alphabet_caps#>FL'],
        'sports_footballevent':        ['playoffs', 'selection', 'Superbowl', '<#fb_weed#>bowl'],
        'fb_weed':        ['Cotton', 'Ragweed', 'Grass', 'Pollen', 'Dust'],
        'sports_footballopportunity':    [
                'qualify for the <#sports_league#> <#sports_footballevent#>',
                'get new lease on <#sports_league#>',
                'reinforce their hold on <#sports_league#>',
                'start thinking about <#sports_footballevent#>'
                ],
        'sports_victoryflavor':    ['surprisingly', 'as expected', 'barely', 'easily', '- get this -'],
        'sportsteam_us':    ['<#sportsteam_us_px#> <#sportsteam_us_sx#>'],
        'sportsteam_us_px':        ['<#state_name#>', '<#cities_USgeneric#>', '<#cities_USmajor#>', '<#cities_USmajor#>', '<#cities_USmajor#>'],
        'sportsteam_us_sx':        [
                'Indians', 'Raiders', 'Ducks', 'Buffalo', 'Dogs',
                'Dolphins', 'Bears', 'Wildcats', 'Hornets', 'Beavers', 'Tigers',
                'Doctors', 'Jets', 'Soldiers', 'Slaves', 'Magicians',
                'Cowboys', 'Sharks', 'Geese',
                ],

        'sportsteam_us_location'    :    ['NY','Philly','Dallas','Detroit','Atlanta','SF','Denver','Chicago','Tampa','Houston','LA',],
        'sportsteam_us_generic'    :    ['Astros','Sixers','Canucks','Liberty','Raiders','Rockets','Devils','Angels','Pistons','Braves','Oilers',],

        'sportsverb_wins_pl'        :    ['beats','trounces','over','takes','demolishes','blitzes','blanks','shuts out',],
        'sportsverb_wins_sing'        :    ['beat','trounce','over','take','demolish','blitz','blank','shut out',],

        'sportsverb_achieves_pl'    :    ['aces','takes','advances to'],
        'sportsverb_achieves_sing'    :    ['ace','take','advance to'],

        'sports_scores_small'        :    ['6-2','6-4','8-4','8-6','10-8','10-6','7-5','7-3','5-0','8-0','11-0','3-1','5-1',],
        'sports_scores_big'        :    ['3<#figs#>-2<#figs#>','2<#figs#>-1<#figs#>','1<#figs#>-<#figs#>'],
        'sports_scores'            :    ['<#sports_scores_small#>','<#sports_scores_small#>','<#sports_scores_big#>'],

        'sports_qualifiers'            :    ['in O/T',],
        'sports_goal'                :    ['draft pick','draft selection',],
        'sports_trophy'            :    ['Pennant','Playoffs','Semifinals','Series','Championship','Open'],

        'sports_position'            :    ['Coach','Quarterback','Pitcher'],
        'sports_action'            :    ['slamdunk','field goal','homerun','no-hitter'],

        'sportsbasic_us'        :    [
                '<#sportsteam_us_location#> <#sportsverb_wins_pl#> <#sportsteam_us_generic#>',
                '<#sportsteam_us_location#> <#sportsverb_wins_pl#> <#sportsteam_us_location#>',
                '<#sportsteam_us_generic#> <#sportsverb_wins_sing#> <#sportsteam_us_location#>',
                ],

        'sports_achievement_us':    [
                '<#sportsteam_us_location#> <#sportsverb_achieves_pl#> <#sports_trophy#>',
                '<#sportsteam_us_generic#> <#sportsverb_achieves_sing#> <#sports_trophy#>',
                '<#town_us#> <#sportsverb_achieves_pl#> <#sports_goal#>',
                ],
        'sports_organizations_us':    ['NBA','NFL','NCAA','WNBA',],

        'sports_machination_us':    [
                '<#names_last#> <#sportsverb_achieves_pl#> <#sports_trophy#>',
                '<#names_last#> named to <#sports_organizations_us#> <#sports_goal#>',
                '<#names_last#> dropped from <#sports_organizations_us#> <#sports_goal#>',
                '<#sports_position#> <#names_last#> to retire from <#sportsteam_us_generic#>',
                '<#sports_position#> <#names_last#> injured, out for season',
                '<#names_last#> signed to <#sportsteam_us_generic#>',
                '<#sportsteam_us_generic#> sign <#names_last#> in $1<#figs_nonzero#>M deal',
                '<#sportsteam_us_generic#> investigated for drug use',
                '<#names_last#> sets <#sports_action#> record',
                "<#company_consolidated#>'s <#names_last_patrician#> buys <#sportsteam_us_generic#> for $<#figs_nonzero#><#figs_nonzero#>M",
                '<#names_last#> leads <#sportsteam_us_generic#> to <#sports_scores#> victory',
                ],

        'sportsheadline_us'    :    [
                '<#sportsbasic_us#>, <#sports_scores#>',
                '<#sportsbasic_us#>, <#sports_scores#>',
                '<#sportsbasic_us#>, <#sports_scores#> <#sports_qualifiers#>',
                '<#sports_achievement_us#>',
                '<#sports_achievement_us#>',
                '<#sports_machination_us#>',
                '<#sports_machination_us#>',
                '<#sports_machination_us#>',
                ],

        'sportsheadline_soccer':    [
                '<#sports_soccer_teams#> - <#sports_soccer_teams#>, <#sports_soccer_score#>.',
                '<#sports_soccer_teams#> vs. <#sports_soccer_teams#>, <#sports_soccer_score#>.',
                '<#sports_soccer_teams#> played <#sports_soccer_teams#>, <#sports_soccer_score#>, <#sports_soccer_location#>.',
                'Review: <#sports_soccer_teams#> and <#sports_soccer_teams#> for the <#sports_soccer_tournament#>.',
                '<#!bold, sports_soccer_tournament#>: <#sports_soccer_teams#> and <#sports_soccer_teams#>.',
                ],
        'sportsblurb_soccer':    [
                '<#sportsheadline_soccer#><br><#sports_soccer_highlight#>',
                '<#sportsheadline_soccer#><br><#sports_soccer_highlight#> <#sports_soccer_roundoff#>',
                ],

        'sports_soccer_location':    ['<#cities_Italian#>', '<#cities_German#>', '<#cities_Dutch#>', '<#cities_Russia#>'],
        'sports_soccer_teams':        [
                'Ajax', 'PSV', 'Feyenoord', 'ADO',
                'Luik', 'Antwerpen',
                'Borussia', 'Dynamo',
                'Juventus', 'Barcelona', 'Real Madrid', 'Parma',
                'Manchester United', 'Leeds',
                'Brazil', 'Argentina', 'Holland', 'Germany', '<#country#>',
                ],
        'sports_soccer_tournament':    [
                '<#sports_soccer_tournamentpx#><#sports_soccer_tournamentsx#>',
                '<#sports_soccer_authority#> <#sports_soccer_tournamentpx#><#sports_soccer_tournamentsx#>',
                ],

        # only to be used after running <#sportsheadline_soccer#>
        'sports_soccer_highlight':    [
                '<#names_last#> scored his <#figs_ord#> goal this season after a great assist by <#otherguy=names_last#><#otherguy#>. <#otherguy#> recently joined the team after a transfer from <#sports_soccer_teams#>.',
                'The <#figs_ord#> minute into the second half <#names_last#> was given yellow by referee <#names_last#>, his second one this season.',
                ' announced it acquired <#names_last#> from  for <-randint(2, 30)-> million.',
                '<#names_last#> left the match after <-randint(1, 44)-> minutes after injuring his knee.',
                ],
        'sports_soccer_roundoff':    [
                ' is doing very well in the <#sports_soccer_tournament#>.',
                " didn't too well in the <#sports_soccer_tournament#> but the new players <#names_last#> and <#names_last#> are working miracles.",
                ],
        'sports_soccer_tournamentpx':    ['Premier', '<#sports_sponsor#>', 'Honor', 'Gold', 'Euro', 'Champions', 'World', 'Western'],
        'sports_soccer_tournamentsx':    ['League', 'Competition', 'Cup', 'Championship'],
        'sports_soccer_authority':    ['<#alphabet_caps#>FA', 'I<#alphabet_caps#>FA'],
        'sports_soccer_score':        [
                '<-randint(0, 3)->-<-randint(0, 3)->',
                '<-randint(3, 5)->-<-randint(0, 3)->'
                ],

        # generic sports
        'sportsheadline_generic': [
                '<#names_last#> <#sports_record#> on <#sports_distance#>.',
                '<#names_last#> <#sports_record#> at <#sports_genericevent#>.',
                ],
        'sports_record':    ['Gold', 'Silver', 'Bronze',
                'WR',
                '1st', '2nd', '3rd',
                'first', 'second', 'third',
                ],
        'sports_distance':    ['10K', '1000m', '400m', '5000m', '5K',],
        'sports_generic_match':    [
                '<#names_last#> vs <#names_last#>',
                '<#name_male#> vs <#name_male#>',
                '<#name_female#> vs <#name_female#>',
                ],
        'sports_genericevent':    [
                '<#sports_venue#> <#sports_eventflavor#>',
                '<#sports_sponsor#> <#sports_eventflavor#>',
                '<#sports_sponsor#> <#sports_eventflavor#>, <#sports_venue#>',
                ],
        'sports_sponsor':        ['<#company_consolidated#>', '<#name_japanese#>', '<#names_last_patrician#>'],
        'sports_eventflavor':    ['Open', 'Cup', 'Derby', 'Championship',],
        'sports_venue':        ['<#cities_USmajor#>', '<#city#>', '<#country#>', '<#sports_sponsor#>Stadium', '<#sports_sponsor#>Dome', '<#sports_sponsor#>Arena', ],

        # horses ? gambling?
        }

