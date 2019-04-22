# -*- coding: UTF-8 -*-
#
"""
        history
        Scientific names, words and things
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'





# ------------------------------------------------------
#    scientific
#
content = {
    'sci_transition_metals':        [
            'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum',
            'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver','Cadmium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum',
            'Gold', 'Mercury', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Ununnilium', 'Unununium', 'Ununbium','<#names_last_patrician#>ium',],
    'sci_noble_gasses':    ['Helium', 'Neon', 'Argon', 'Krypton', 'Xenon', 'Radon'],
    'sci_other_metals':    ['Aluminum', 'Gallium', 'Indium', 'Tin', 'Thallium', 'Lead', 'Bismuth' ],
    'sci_elements'    :    ['<#sci_transition_metals#>','<#sci_noble_gasses#>','<#sci_other_metals#>',],
    'sci_astro_planets':    ['mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto',],
    'sci_astro_moons':        ['deimos','phobos','io'],
    'sci_astro_stars'    :    ['ceres','andromeda','ursa','cassiopeia','aldebaran','antares','arcturus',
            'argo','betelgeuse','callisto','castor','corvus','cygnus','deneb','draco','fornax','hercules','hydra','lyra','mensa','orion',
            'pegasus','perseid','phoenix','pleiades','pollux','regulus','rigel','sirius','vega',],
    'sci_astro_constellations':    ['aquarius','aries','capricorn','cancer','gemini','leo','libra','pisces','sagittarius', 'scorpio','taurus','virgo',],
    'sci_astro_misc':    ['galaxy',],
    'sci_astro':        [
            '<#sci_astro_planets#>',
            '<#sci_astro_moons#>',
            '<#sci_astro_stars#>',
            '<#sci_astro_constellations#>',
            ],
    'sci_popularelements':    ['Hydrogen', 'Carbon', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Titanium',
                    '<#sci_transition_metals#>',
                    '<#sci_noble_gasses#>', '<#sci_other_metals#>',
                    ],

    'sci_blood_type':        ['A', 'B', 'O', 'AB'],
    'sci_blood_rhesus':        ['positive', 'negative', 'pos', 'neg', '+', '-'],
    'sci_blood':        ['<#sci_blood_type#> <#sci_blood_rhesus#>'],
    'sci_anatomy_human':    [
            '<#sci_anatomy_one#>',
            '<#left_or_right#> <#sci_anatomy_two#>',
            '<#sci_anatomy_human_transplant#>',
            '<#left_or_right#> <#sci_anatomy_two#>',
            '<#sci_anatomy_human_transplant#>',
            ],
    'sci_anatomy_one':    ['head', 'nose', 'mouth', 'skull'],
    'sci_anatomy_two':    [
            'ear', 'eye',
            'lung',
            'foot', 'toe', 'ankle', 'leg', 'kneecap', 'thigh',
            'hand', '<#sci_anatomy_finger#> finger',
            'thumb', 'pinky', 'little finger',
            ],
    'sci_anatomy_finger':    ['index', 'middle', 'ring'],

    'sci_anatomy_human_transplant':    [
            'digit',
            'tendon', 'artery', 'gut',
            'liver', 'kidney', 'heart',
            ],

    'sci_disciplines':    [
            'liberal arts', 'mathematics',
            'physics', 'philosphy', 'classics', 'literature',
            'medicin', 'art', 'economics',
            ],

    'sci_titles_sx':    [
            'MRCVS',
            'MD', 'MA', 'MP', 'MO',
            'RS<#alphabet_caps#><#alphabet_caps#>'
            ],
    'sci_titles_px':    [
            'Professor',
            'Doctor',
            'Fellow',
            ],
    'sci_pseudo':[
            '<#sci_isms#>','<#sci_isms#>','<#sci_isms#>','<#sci_isms#>',
            '<#sci_isms_px#><#sci_isms#>',
            '<#sci_isms_px#>-<#sci_isms#>',
            ],
    'sci_pseudomisc':    [
            'vernacular',
            'stupidity',
            'ratio',
            ],
    'sci_isms_px':[
            'post',
            'neo',
            'pan',
            'socio',
            'ethno',
            'techno',
            'proto',
            'multi',
            'theo',
            'macro',
            'micro',
            ],
    'sci_isms':[
            'industrialism',
            'communism',
            'socialism',
            'cubism',
            'optimism',
            'pessimism',
            'capitalism',
            'modernism',
            'eclecticism',
            'globalism',
            'futurism',
            'dadaism',
            'criticism',
            'pluralism',
            'satanism',
            'protestantism',
            'agnosticism',
            'catholocism',
            'judaism',
            'journalism',
            'eroticism',
            'creationism',
            'cynicism',
            'positivism',
            'negativism',
            ],


    'university':     [
            'University of <#city#>',
            'University of <#state_name#>',
            '<#state_name#> University',
            '<#state_name#> State University',
            '<#city#> Business School',
            ],
    'university_dept':     [
            'Department of <#!^,sci_disciplines#> of the <#university#>',
            'Dpt. of <#!^,sci_disciplines#> of the <#university#>',
            ],

}

