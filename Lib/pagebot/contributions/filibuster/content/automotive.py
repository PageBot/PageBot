# -*- coding: UTF-8 -*-

"""
        history
        Automotive, everything to do with cars
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'
__author__ = "rich"


# this module contains 1 single dictionary named content.
# you define your stuff inside this dictionary.
content = {
        'cars_headline': ['<#automotive_shortheadline#>'],
        'automotive_section':    ['Cars', 'Cars', 'Cars', 'New cars', 'Hot cars'],
        'automotive_shortheadline': ['<#^,car_name#>'],
        'car_engine_type':        [
                '440 Wedge',
                'Boss 302',
                '429 Super Cobra Jet',
                '426 Hemi',
                '327 Turbo-Fire',
                'LT-1 350',
                '340 Six Pack',
                '409',
                'Flathead V8',
                'Rat motor'
                ],
        'car_brand_loyalty':    [
                'Mopar Machine',
                'Freaky Ford',
                'Heavy Chevy',
                'Studly Stude',
                'Purrin Pontiac',
                ],
        'car_brand_us': [
                'Cadillac',
                'Ford',
                'Pontiac',
                ],
        'car_brand_europ': [
                'Nissan',
                'Mercedes',
                'Volkswagen',
                'Volvo',
                'Saab',
                'Renault',
                u'Citroën',
                'Audi',
                ],
        'car_brand_japan': [
                'Nissan',
                'Toyota',
                ],
        'car_brand': [
                '<#car_brand_us#>','<#car_brand_us#>','<#car_brand_europ#>','<#car_brand_europ#>',
                '<#car_brand_japan#>',
                ],
        'car_busts':    [
                'junker',
                'jalopy',
                'scrap heap',
                ],
        'car_engine_boltons':    [
                'Holley double pumper',
                'Hooker headers',
                'GM 6-71 blower',
                'roller rockers',
                'four-bolt mains',
                'Edelbrock high rise manifold',
                'cast aluminum valve covers',
                'forged rods',
                'solid lifters',
                'Mildon fuel injection',
                'cowl induction',
                'domed pistons',
                'dry sump oiler',
                ],
        'car_engine_boltonscap':    [
                'Holley double pumper',
                'Hooker headers',
                'GM 6-71 blower',
                'Roller rockers',
                'Four-bolt mains',
                'Edelbrock high rise manifold',
                'Cast aluminum valve covers',
                'Forged rods',
                'Solid lifters',
                'Mildon fuel injection',
                'Cowl induction',
                'Domed pistons',
                ],
        'car_compression_ratio':    [
                '10.1:1',
                '11:1',
                '9.4:1',
                '8.3:1',
                '12.2:1',
                ],
        'car_heads_carsets':    [
                'Main Street monster',
                'ground pounder',
                'street machine',
                'hiway hauler',
                'dragstrip demon',
                'pavement pounder',
                ],
        'car_body_work':    [
                'chopped n channeled',
                'candy apple red',
                'scalloped',
                'louvered',
                'tubbed out',
                'flamed'
                ],
        'car_engine_modifiers':    [
                'ported & polished',
                'balanced and blueprinted',
                'worked',
                'blown',
                'injected'
                ],
#erik...how do I put an apostrophe before a text string? example: '57 Chevy'
#    by putting the entire string in double quotes
#    better yet: use html entities, but I'll have more on that later.
        'car_hot_rods':    [
                u"’57 Chevy",
                'Willys coupe',
                'duece',
                'hi boy roadster',
                'vette',
                'stang',
                'Shelby Cobra',
                'Cuda',
                u"’67 Chevelle",
                'Galaxie 500',
                'Fairlane',
                u"’55 Merc",
                't-bucket',
                u"’32 Ford",
                'GT 350',
                'Chevy II',
                'Challenger',
                'Charger',
                'Impala',
                'Goat',
                ],

        'car_hotrod_modifier':    [
                'hopped up',
                'radical',
                ],
        'car_blow_doors':    [
                'eatin dust',
                'eatin rubber',
                'suckin smoke',
                'belchin bleach',
                'suckin CO',
                ],
        'car_power_delivery':    [
                'TH 350',
                '9 inch rear',
                'set of fat Mickey Thompson slicks',
                'Detroit locker',
                ],
        'car_power_designators':    [
                'horses',
                'ponies',
                ],
        'car_name': [
                u'<#car_hot_rods#>',
                u'<#car_hot_rods#>, <#car_engine_type#>',
                u'<#car_brand#>',
                u'<#car_brand#>',
                u'<#car_brand#>',
                u'<#car_brand#> <#car_engine_type#>',
                ],
        'car_shop_talk':    [
                u'This <#car_body_work#> <#car_heads_carsets#> has a <#car_engine_modifiers#> <#car_engine_type#> with a <#car_power_delivery#> to get all that power on the street.',
                u'You cant run with this <#car_hotrod_modifier#> <#car_hot_rods#>, she’s got a <#car_engine_modifiers#> <#car_engine_type#> with a <#car_compression_ratio#> compression ratio and <#car_engine_boltons#>.',
                u'Need more <#car_power_designators#>? Try a <#car_engine_modifiers#> <#car_engine_type#> with a <#car_compression_ratio#> compression ratio and <#car_engine_boltons#>.',
                u'<#car_engine_boltonscap#> and a <#car_engine_modifiers#> <#car_engine_type#> will give your <#car_hot_rods#> a lotta <#car_power_designators#>.',
                u'Forget your <#car_busts#>, my <#car_hotrod_modifier#> <#car_hot_rods#> has a <#car_engine_modifiers#> <#car_engine_type#> thatll leave you <#car_blow_doors#>.',
                ],
        }



