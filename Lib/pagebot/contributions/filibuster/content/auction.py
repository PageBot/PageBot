# -*- coding: UTF-8 -*-
#
#    Contributed by Erik van Blokland and Jonathan Hoefler
#    Original from filibuster.

"""
        auction
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""

__version__ = '4.0'


content = {
    'auction_section': ['<#commercial_section#>'],
    'auction_shortheadline':[
        '<#^,politics_euro_nationality#> <#^,auction_antiques_objects#>',
        '<#^,auction_antiques_period#> <#^,auction_antiques_objects#>',
        '<#^,auction_antiques_adj#> <#^,auction_antiques_objects#>',
    ],
    'auction_antiques': [
        '<#politics_euro_nationality#> <#auction_antiques_adj#> <#auction_antiques_period#> <#auction_antiques_objects#> (<#auction_object_state#>)',
        '<#auction_antiques_adj#> <#politics_euro_nationality#> <#auction_antiques_period#> <#auction_antiques_objects#> (<#auction_object_state#>)',
        '<#auction_antiques_adj#> <#auction_antiques_material#> <#auction_antiques_period#> <#auction_antiques_objects#>',
    ],
    'auction_antiques_adj': [
        'Antique',
        'old',
        'antique',
        'embossed',
        'signed',
        'embroidered',
        'vintage',
    ],
    'auction_antiques_bid': [
        '<-randint(1, 100)->,000',
    ],
    'auction_antiques_material': [
        'cloth',
        'cotton',
        'glass',
        'silver',
        'gold-plated',
        'wood',
        'pine',
        'oak',
        'leather',
    ],
    'auction_antiques_objects': [
        'clock',
        'tea tin',
        'book',
        'embroidery',
        'pocket knife',
        'coverlet',
        'hunting pouch',
        'mirror',
        'tapestry sampler',
        'wall phone',
        'hat pin',
        'trunk',
        'dental tools',
        'tryptich',
        'piano roll',
        'master',
        'painting',
        'tool',
        'chronometer',
    ],
    'auction_antiques_period': [
        '<-randint(17, 19)->th century',
        'edwardian',
        'victorian',
        'art nouveau',
        'impressionist',
        '"arts and crafts"',
        'Jeffersonian',
    ],
    'auction_autos': [
        '<-randint(1960, 1970)-> <#car_brand#><#car_mod#>',
        'Drive a <#car_brand#><#car_mod#> for FREE! Exclusive Secrets!',
        'COBRA RADAR/LASER DETECTORS',
        'Turbocharged MR2 REAR ENGINE SPORT CAR..WOW!',
    ],
    'auction_autos_bid': [
        '<-randint(10, 50)->,000',
    ],
    'auction_beanbags': [
        '<#hero_pets#> beanie baby',
        '<#hero_pets#> Beaniebaby',
    ],
    'auction_beanbags_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_books': [
        '<#hero_comic_title#>',
    ],
    'auction_books_bid': [
        '<-randint(10, 100)->.00',
    ],
    'auction_category': [
        'autos',
        'antiques',
        'books',
        'music',
        'movies',
        'coins',
        'stamps',
        'collectibles',
        'computers',
        'dolls',
        'jewelry',
        'photo',
        'electronics',
        'pottery',
        'glass',
        'sports',
        'memorabilia',
        'toys',
        'beanbags',
        'miscellaneous',
    ],
    'auction_coins': [
        '<#politics_euro_nationality#> coins  (<#auction_object_state#>)',
        'coins from <#country#>  (<#auction_object_state#>)',
        'Complete collection from <#country#>  (<#auction_object_state#>)',
        'Historic currency from <#country#>',
    ],
    'auction_coins_bid': [
        '<-randint(5, 10)->,000',
    ],
    'auction_collectibles': [
        '<#hero_comic_title#>  (<#auction_object_state#>)',
    ],
    'auction_collectibles_bid': [
        '<-randint(5, 20)*20->',
    ],
    'auction_computers': [
        '<#CE_product#>',
    ],
    'auction_computers_bid': [
        '<-randint(10, 40)*75->.00',
    ],
    'auction_dolls': [
        'The <#names_first_female#> Collection',
        '<-randint(1960, 2000)-> <#names_first_female#>',
        '<#names_first_female#>, <-randint(1960, 2000)-> issue.',
        'Hummel ceramic figurine',
    ],
    'auction_dolls_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_electronics': [
        '<#CE_product#>',
    ],
    'auction_electronics_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_glass': [
        'Some old Glass',
    ],
    'auction_glass_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_item': [
        '<#auction_<#auction_category#>#><#auction_qualification#>',
    ],
    'auction_item_bid': [
        '$<#auction_<#auction_category#>_bid#>.00',
    ],
    'auction_jewelry': [
        '<#auction_antiques_adj#> <#auction_jewelry_object#>',
        '<#auction_antiques_period#> <#auction_jewelry_object#>',
        '<#auction_jewelry_object#>',
        '<#auction_jewelry_adj#> <#auction_jewelry_object#>',
        '<#auction_jewelry_object#> (<#auction_object_state#>)',
        '<#auction_jewelry_adj#> <#auction_jewelry_object#> (<#auction_object_state#>)',
    ],
    'auction_jewelry_adj': [
        'diamond',
        'glass',
        'gold',
        'silver',
        'platinum',
        'gold plated',
        'brass',
        'rhinestone',
    ],
    'auction_jewelry_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_jewelry_object': [
        'necklace',
        'ring',
        'earring',
        'armband',
        'tiara',
        'leaf pin',
        'pin',
        'chain',
    ],
    'auction_memorabilia': [
        'Memories, hardly used.',
    ],
    'auction_memorabilia_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_miscellaneous': [
        '<#!^,sci_anatomy_human#>, <#sci_blood#>',
        'property on <#sci_astro_planets#>',
    ],
    'auction_miscellaneous_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_movies': [
        '<#!uppercase, movie_medium#>: <#movie_superheroes#> (<-randint(1960, 2000)->)',
        '<#!uppercase, movie_medium#>: <#movie_superheroes#> (by <#name_japanese#>)',
        '<#!uppercase, movie_medium#>: <#!uppercase, fbt#> (by <#name_japanese#>, <-randint(1960, 2000)->)',
        '<#!uppercase, movie_medium#>: <#fbt#> (<-randint(1960, 2000)->)',
    ],
    'auction_movies_bid': [
        '<-randint(5, 100)*20->,00',
    ],
    'auction_music': [
        '<#classic_composer#> by <#classic_orchestra#> (<#auction_object_state#>)',
        'CD: <#classic_recording_highbrow#>',
        u'old 78’s! <#classic_composer#> <#classic_classification#> (<#auction_object_state#>)',
        'Piano rolls: <#classic_composer#> (<#auction_object_state#>)',
    ],
    'auction_music_bid': [
        '<-randint(5, 20)*5->.00',
    ],
    'auction_object_detail': [
        'corner',
        'back',
        'front',
        'top',
        'bottom',
        'inside',
    ],
    'auction_object_state': [
        'slightly scratched',
        'mint',
        'near mint',
        'excellent condition',
        'reasonable',
        '<#auction_object_state_deteriorate#> at <#auction_object_detail#>',
        'in original box',
        'w/original box',
    ],
    'auction_object_state_deteriorate': [
        'slight foxing',
        'scratches',
        'worn',
        'discolored',
        'frayed',
    ],
    'auction_photo': [
        '<#corporation_japanese#> Camera',
    ],
    'auction_photo_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_pottery': [
        'Piece of therapeutic pottery',
    ],
    'auction_pottery_bid': [
        '<-randint(5, 10)->',
    ],
    'auction_qualification': [
        ' - in excellent condition',
        ' L@@K!!',
        ' (needs some work)',
        ' GREAT PRICE',
        ' Limited Time Only',
        ' - Mint Condition',
        '~BLOWOUT SALE~',
        'WOW',
        '',
        '',
        '',
        '',
        '',
        '',
    ],
    'auction_sports': [
        '<#sportsteam_us#> cap',
        'Signed <#sportsteam_us#> Ball',
        'Signed <#sportsteam_us#> Shirts',
        '<#sportsteam_us#> season tickets',
        '<#sportsteam_us#> tickets - Great Seats!',
    ],
    'auction_sports_bid': [
        '<-randint(10, 100)*50->',
    ],
    'auction_stamps': [
        '<#colors_primary#> Mauritius <-randint(5, 50)-> cents. Rare!stamps from <#country#>',
        'Complete collections from <#country#>',
        'Historic stamps from <#country#>',
    ],
    'auction_stamps_bid': [
        '<-randint(5, 10)->,000.00',
    ],
    'auction_toys': [
        '<#fbt#>, <-randint(1960, 2000)->, needs batteries',
    ],
    'auction_toys_bid': [
        '<-randint(10, 200)*50->',
    ],
    'car_brand': [
        'GM',
        'Mustang',
        'Chevvy',
        'Ferrari',
        'Volkswagen',
        'Mercedes-Benz',
    ],
    'car_mod': [
        ' Convertible',
        ' Roadster',
        ' High Top',
        ' Van',
        '',
        '',
        '',
        '',
        '',
        '',
    ],    }

