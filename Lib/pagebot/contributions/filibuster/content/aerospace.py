# -*- coding: UTF-8 -*-

"""
        history
        Airplanes n things
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
        'aerospace_headline': ['<#air_news_neutral#>'],
        'aerospace_ankeiler': [
                '<#air_news_bad#>',
                '<#air_news_medium#>',
                '<#air_news_medium#>',
                '<#air_news_neutral#>',
                '<#air_news_neutral#>',
                '<#air_news_neutral#>',
                '<#air_news_slanted#>',
                ],
        'aerospace_section':['Flights','Travel','Travel','Travel','Travel','Aerospace','Holiday'],

        'air_jetmodel_wide':[
                'Boeing 7<-randint(0,9)->7 <#air_jetmodel_flavor#>',
                'B 7<-randint(0,9)->7-<-randint(1,5)->00 <#air_jetmodel_flavor#>',
                'Airbus <-randint(1, 6)->00<#alphabet_caps#> <#air_jetmodel_flavor#>',
                'McDonnell Douglas MD<-randint(4, 20)-> <#air_jetmodel_flavor#>',
                'MD<-randint(4, 20)-> <#air_jetmodel_flavor#>',
                'DC<-randint(8, 15)-> <#air_jetmodel_flavor#>',
                ],
        'air_jetmodel_medium':[
                'Short Sunderland <-randint(8, 15)->00',
                'Saab <#alphabet_caps#><-randint(8, 15)->0',
                'Fokker F<-randint(20, 30)->0',
                ],
        'air_jetmodel_small':[
                'Cessna Citation<#num_roman#>',
                '<#num_roman#>',
                ],
        'air_jetmodel_flavor': ['','','','','',
                'Luxury Liner','HighTop','<#air_class_adj#>Top','<#alphabet_caps#>',
                'WideBody',
                'WideWing',
                'LuxuryWing',
                ],
        'air_carrier': [
                '<#air_carrier_generic#>','<#air_carrier_generic#>','<#air_carrier_generic#>',
                '<#air_carrier_generic#>','<#air_carrier_generic#>','<#air_carrier_generic#>',
                'KLM', 'Continental', 'SwissAir', 'SAS', 'Air France', 'Virgin Atlantic',
                'Sky Team', 'Delta', 'KLM', 'Sky Team', 'Delta', 'KLM', 'Sky Team', 'Delta', 'KLM',
                'Lufthansa', 'SAS',
                ],
        'air_carrier_px': [
                'Trans','National',
                'Royal','Euro',
                'Air','Pan',
                'Grand','Inter',
                ],
        'air_carrier_name': [
                'US', 'Canada', 'Japan','France', 'Alaska','Scandinavian','American','Asian',
                'Cargo','Carrier','Globe','World','Global',
                ],
        'air_carrier_sx1': ['Wings', 'Cargo',
                'Pacific','Atlantic','Bulk','Charters','Travel','Air', 'Airways','Air', 'Airways',
                ],
        'air_carrier_generic': [
                '<#air_carrier_px#><#air_carrier_sx1#>',
                '<#air_carrier_px#><#air_carrier_name#><#air_carrier_sx1#>',
                '<#air_carrier_px#><#air_carrier_name#>',
                '<#air_carrier_name#><#air_carrier_px#>',
                '<#air_carrier_name#><#air_carrier_sx1#>',
                ],
        'air_flightnumber': ['flight <-randint(200, 400)->'],
        'air_loyalty': ['<#air_loyalty_px#><#air_loyalty_sx#>'],
        'air_loyalty_px':[
                'Loyalty',
                'World',
                'SilverWing',
                'Ambassador',
                'Customer',
                'Friendship',
                'Air',
                ],
        'air_loyalty_sx':[
                'Points','Account',
                'Miles',
                'Perks',
                ],
        'air_class': [
                '<#air_class_adj#><#air_class_adj#> Class',
                '<#air_class_adj#> Class',
                '<#air_class_adj#>class',
                ],
        'air_class_adj': [
                'Business','Royal','First','Excellence','Excel','Premier','Comfort','Care','World',
                'Gold','Silver','Platinum','Lux','Ambassador','Envoy', 'Comfy', 'Froufrou',
                ],
        'air_description': [
                '<#air_carrier#> <#air_jetmodel_wide#>'
                ],
        'air_crashsites': ['Newfoundland','Alaska','Pacific','Canada','Atlantic','Greenland','Nova Scotia'],
        'air_crashcause': ['no accident','accident','weather','bomb','terrorists','human error','fighter attack'],
        'air_crashinvestigator': ['FCC', 'NTSB', 'FBI', '<#politics_euro_nationality#> police', '<#politics_euro_nationality#> investigators'],
        'air_accident': [
                'Heavy turbulence','Peanuts','Problems', 'cell-phone usage',
                'Fire','Emergency landing','Landing gear problem','Birds','Snow',
                'hooligans', 'a drunk passenger', 'radioactive cargo'
                '<#air_accident_causes#> in the <#air_accident_objects#>'
                ],
        'air_accident_causes': ['faulty wiring', 'software problems', 'software conflicts'],
        'air_accident_objects': ['onboard entertainment systems', 'in-seat games', 'GPS equipment',
                ''
                ],
        'air_crash_casualties': [
                '<-randint(2, 10)-> wounded',
                '<-randint(2, 10)-> injured',
                '<-randint(200, 400)-> dead and <-randint(2, 10)-> wounded',
                '<-randint(200, 400)-> dead',
                '<-randint(200, 400)-> feared dead',
                '<-randint(200, 400)-> missing',
                ],
        'air_people': ['pilots', 'airtraffic controllers', 'luggage handlers',
                'customs', 'stewardesses','flight attendants', 'caterers','maintenance','crew',
                'cabin crews',],
        'air_news_bad':[
                '<#air_carrier#> plane lost over <#air_crashsites#>.',
                'Tragedy: <#air_carrier#> down over <#air_crashsites#>, <#air_crash_casualties#>.',
                'Midair collision: <#air_carrier#> and <#air_carrier#> at <#city#> Airport, <#air_crash_casualties#>.',
                '<#air_jetmodel_medium#> accident at <#city#> Airport, <#air_crash_casualties#>.',
                ],
        'air_news_medium':[
                '<#air_accident#>: <-randint(2, 50)-> <#air_carrier#> passengers wounded.',
                "<#air_crashinvestigator#>: <#air_flightnumber#> should not have left <#city#> Airport.",
                "<#air_crashinvestigator#>: <#air_flightnumber#>-case reopened.",
                "<#air_crashinvestigator#> reopen <#air_flightnumber#>-case: suspected <#air_accident#>.",
                '<#!capitalize,war_forces#> hijack <#air_carrier#> <#air_flightnumber#>.',
                "<#air_crashinvestigator#>: cause <#air_flightnumber#> crash: <#air_crashcause#>.",
                '<#air_carrier#> <#air_people#> strike <#num_ord#> day, <-randint(2, 50)*100-> people stuck.',
                ],
        'air_news_neutral':[ # Keep these short messages
                u'<#air_carrier#>: “ticket prices up”',
                '<#air_carrier#> reports a <-randint(2,10)->M profit last quarter',
                '<#air_carrier#> reports a <-randint(2,10)->M loss last quarter',
                '<#air_carrier#> reports a <-randint(2,10)->M gross last quarter',
                u'<#air_carrier#> last quarter “not so good”',
                '<#air_carrier#> bust: <-randint(200, 2000)-> jobs lost',
                '<#air_carrier#> strike: <-randint(2, 50)*100-> stranded',
                ],
        'air_news_slanted':[
                '<#air_carrier#> and <#air_carrier#> announce strategic allience',
                '<#air_carrier#> to buy <-randint(5,15)-> <#air_jetmodel_wide#>: <-randint(2,10)->M deal',
                '<#air_carrier#> presents <#air_jetmodel_wide#>, <#air_class#>',
                '<#air_carrier#> rolls out <#air_jetmodel_wide#>, new <#air_class#> seats',
                '<#air_carrier#> joins <#air_carrier#> in <#air_loyalty#> program',
                ],
        'air_commercial':[
                u'<#air_commercial_offer#> <#carrier#>: <#air_commercial_motto#>™'
                ],
        'air_commercial_offer':[
                'Introducing <#air_class#> on all <#carrier=air_carrier#><#carrier#> <#air_jetmodel_wide#> planes',
                '<#air_class#> now available on all <#carrier=air_carrier#><#carrier#> flights to <#city#>'
                ],
        'air_commercial_motto':[
                'a fine way to fly', 'we know how to fly', 'flying comes natural to us', 'we fly planes the way they were intended', 'we read the manual',
                'taking you there'
                ],
        }

