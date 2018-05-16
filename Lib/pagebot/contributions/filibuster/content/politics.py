# -*- coding: UTF-8 -*-
#
"""
        history
        World news headlines, wars, disaster, politics
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

4.0    - changed location to city in weather
        - added war_military for ranks
evb        

"""

__version__ = '4.0'



# ------------------------------------------------------
#    worldnews
#
content = {

    # ------------------------------------------------------
    #    politics
    #
    'politics_headline'                :    ['<#^,politics_us#>', '<#^,politics_euro_headline#>'],
    'politics_section': ['Politics','Politics','Politics','Politics','Politics','Politics','Politics','Politics','Election','The White House',],
    
    'politics_us'                :    ['<#politics_us_election#>', '<#politics_us_event_single#> <#politics_action_sing#>', '<#politics_us_event_pl#> <#politics_action_pl#>'],
    'politics_us_events'            :    ['<#politics_us_event_single#>', '<#politics_us_event_pl#>'],
    
    'politics_us_congressman'    :    ['Senator','Representative'],
    'politics_us_congressman_abbr':    ['Sen.','Rep.'],
    'politics_us_guy'            :    ['<#politics_us_congressman_abbr#> <#name_somewhiteguy#> (<#politics_us_partyabbr#>, <#state_abbr#>)'],
            
    'politics_us_event_single':    ['Senator', 'Congressman', 'Congress', 'Senate', 'House', 
            'the <#politics_us_party#> party', 'the <#politics_us_party#> Convention',
            'President', u'President’s <#politics_us_confidant#>', 'White House', 'White House <#politics_us_confidant#>',
            'Capitol Hill', 'Supreme Court', 'Supreme Court Justice', 'Lawyer', 'House Speaker',     '<#politics_us_agency#> spokesman'
            ],
    'politics_us_event_pl':        ['Senators', 'Supreme Court Justices', 'Lawyers', '<#politics_us_partyadj#>s'
            ],
    'politics_us_party':            ['Democratic', 'Republican'],
    'politics_us_partyadj':        ['Democrat', 'Republican'],
    'politics_us_partyabbr':        ['D','R'],
    'politics_us_confidant':        ['advisor', 'astrologer'],
    'politics_us_agency':        ['Federal Bureau of <#politics_us_department#>', 'Treasury', 'Secret Service', 'NSA', 'DEA', 'CIA', 'FBI'],
    'politics_us_department':    ['Engraving and Printing', 'Investigation', 
            '<#politics_us_contraband#>, <#politics_us_contraband#> and <#politics_us_contraband#>'],
    'politics_us_contraband':    ['Marijuana', 'Drugs', 'Cocaine', 'Firearms', 'Knives', 'Scissors', 'Rocks', 'Heroin', 'Plutonium'],
    
    # euro politics
    'politics_euro_headline':['<#politics_euro_nationality#> <#politics_euro_leader#> <#politics_action_sing#>',
                    '<#politics_euro_nationality#> <#politics_euro_officials#> <#politics_action_pl#>',
            ],
    'politics_euro_officials':    ['civil servants', 'union members', 'officials', 'representatives'],
    'politics_euro_leader':        ['Parliament', 'Prime Minister', 'Head of State', 'President', 'delegation', 'official', 'spokesperson'],
    'politics_action_pl':        ['<#politics_action#>',
            'questioned in <#war_target#> <#politics_scandalnoun#>',
            'OK <#politics_scandaladj#> <#politics_law#>', 
             'criticise <#politics_scandaladj#> <#politics_law#>',
            'ratify <#politics_scandaladj#> <#politics_law#>',
            'welcome <#politics_scandaladj#> <#politics_law#>',
            'oppose <#politics_scandaladj#> <#politics_law#>',
            'visit <#news_disastertype#> area'],
    'politics_action_sing':        [
            '<#politics_action#>',
            'passes <#politics_scandaladj#> <#politics_law#>',
            'opposes <#politics_scandaladj#> <#politics_law#>',
            'visits <#news_disastertype#> area',
            'visits <#news_disastertype#> victims'
            ],
    'politics_law':                ['law', 'laws', 'legislation', 'bill', 'plan', 'proposal'],
    'politics_action':            ['named in <#politics_scandal#>', 'involved in <#politics_scandal#>', 'cleared of <#politics_scandal#>'],
    
    'politics_us_election':        [
            '<#politics_us_candidate#> <#politics_us_event_single#>-elect',
            '<#politics_us_candidate#> ahead in polls for <#politics_us_event_single#>',
            '<#politics_us_candidate#> not to run for <#politics_us_event_single#>',
            '<#politics_us_candidate#> mentioned as candidate for <#politics_us_event_single#>',
            '<#politics_us_candidate#> running for <#politics_us_event_single#>',
            '<#politics_us_candidate#> announced candidacy for <#politics_us_event_single#>',
            ],
    'politics_us_candidate':    [
            '<#name_somewhiteguy#>',
            '<#name_somewhiteguy#>',
            '<#name_somewhiteguy#>',
            '<#name_somewhiteguy#>',
            'Larry Flynt',
            'Howard Hughes',
            'Donald Trump',
            'Bill F. Gates',
            'Franklin D. Roosevelt',
            
            ],
    'politics_scandal':                ['<#politics_scandaladj#> <#politics_scandalnoun#>'],
    'politics_scandalnoun':            ['investigation', 'coverup', 'trial', 'charges', 'tapes'],
    'politics_scandaladj':            ['bribes', 'corruption', 'drug', 'tax', 'gun control', 'arms export',
            'sex', 'murder', 'adoption', 'secret payments','donations', '<#politics_subsidyflavor#> subsidies', '<#bank#>',
            'phone tap', 'encryption', '<#war_explosive#>', 'payoff',
            
            ],
    'war_explosive':            ['<#war_explosivemedium#>', '<#war_explosiveadj#> <#war_explosivemedium#>'],
    'war_explosiveadj':            ['plastic', 'chemical', 'nuclear', 'primitive', 'laserguided','anti-personnel', 'tactical', 'personnel',
            'cruise', 'smart', 'laserguided', 'biological', 'miniature', 'micro','conventional', 'old', 'new'],
            
    'war_explosivemedium':        ['landmine', 'bomb', 'rocket', 'missile', 'ICMS', 'ICBM', 'booby-trap'],

    'politics_subsidyflavor':        ['agriculture', 'arts', 'farm', 'wine', 'banana', 'trade', 'export'],
    'politics_treaty':                ['<#politics_treatydescription#> <#politics_agreement#>'],
    'politics_treatydescription':        ['Dayton', 'Oslo', 'Stockholm', 'Camp David', 'Dublin', 'Belfast',],
    'politics_agreement':            ['agreement>', 'accord', 'accords', 'treaty', 'treaties', 'peace process', 'talks', 'cease-news_disaster_fire', 'battle'],
}
