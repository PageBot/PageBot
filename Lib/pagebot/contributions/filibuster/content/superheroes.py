# FILIBUSTER.ORG!

"""
        history
        Superheroes, to spice up the news a bit
        3.0.0   started it
        3.0.1   added hero_comic_title with support
--------------------------------------------------------------------
"""

__version__ = '4.0.0'
__author__ = "evb"

content = {
        'HEADLINE_superhero':   [
                '<#hero_protagonist#> saves <#hero_city#>!',
                '<#hero_city#> indebted tso <#hero_protagonist#>!',
                '<#hero_city#> saved by <#hero_protagonist#>!',
                '<#hero_city#> under threat by <#hero_antagonist#>!',
                '<#robot#> slain by <#hero_protagonist#>!',
                '<#hero_protagonist#> defeats <#hero_antagonist#>'
                ],
                
                
        'hero_outfit':      ['<#hero_brand#>suit', '<#hero_brand#>outfit', '<#hero_brand#>armor', '<#hero_brand#>leotard'],
        'hero_moan':            ['Aaargh', 'Argh', 'Humph!', 'Glaglgalga!'],
        'hero_onomatopaea': ['BLAST', 'KAPOW', 'WHAM', 'ZAP', 'ZOT', 'KRAZOOM', 'ZZZZZOOM'],
        
        'hero_comic_title': [
                '#<-randint(1,320)-> "<#!^,hero_antagonist#> vs. <#!^,hero_protagonist#>" (<#hero_comic_publisher#>)',
                '<#!^,hero_antagonist#> SERIES <-randint(1,320)->',
                '<#!^,hero_protagonist#>, <#hero_comic_issue#>: #<-randint(1,320)->',
                '<#!^,hero_protagonist#>, <#hero_comic_issue#> #<-randint(1,320)->',
                '<#!^,hero_protagonist#>, <#hero_comic_publisher#> #<-randint(1,320)->',
                ],
        'hero_comic_publisher': ['<#p_oldbiz_px#> Comics', '<#p_oldbiz_px#> Mills', '<#p_oldbiz_px#> Toons', ],
        'hero_comic_issue': ['Phantom Zone', 'The Dark Period', 'The 3D Episode',
                'Negativeland <#num_roman#>', 'with <#robot#>',
                'on <#sci_astro_planets#>', 'the "<#sci_astro_stars#>" issue',
                '<#hero_comic_publisher#> <#hero_comic_year#>',
                '<#hero_comic_publisher#> series'],
        'hero_comic_year':  ['<-randint(1930,2200)->'],
        'hero_antagonist':  [
                '<#hero_adj_evil#> <#hero_name#>', 
                '<#hero_adj_evil#> <#heroin_name#>',
                '<#hero_name#>', 
                '<#heroin_name#>'
                ],
        'hero_protagonist': [
                '<#hero_adj_good#> <#hero_name#>',
                '<#hero_adj_good#> <#heroin_name#>',
                '<#hero_name#>',
                '<#heroin_name#>'
                ],
        'hero': ['<#hero_name#>', '<#heroin_name#>', '<#robot#>'],
        'hero_altcarreer':  [
                'journalist for the <#paper_US#>',
                'bar tender at the <#pub_name#>',
                'fisherman', 'surgeon', 
                'teacher at the <#university_dept#>',
                'scientist at the <#university_dept#>',
                'a <#sci_disciplines#> teacher',
                'civil servant',
                ],
        'hero_name':        [
                '<#hero_brand#>Man',
                '<#hero_brand#>man',
                '<#hero_brand#>-boy',
                '<#hero_brand#>kid',
                '<#war_military#> <#hero_brand#>'
                ],
        'heroin_name':      [
                '<#hero_brand#>woman',
                '<#hero_brand#>-woman',
                '<#hero_brand#>-girl',
                ],
        'supersized':   ['Super', 'Hyper', 'Ultra', 'Mini', 'Maxi', 'Macro', 'Micro',],
        'hero_brand':   [
                '<#supersized#>','<#supersized#>','<#supersized#>',
                'Omni', 'God', 
                'Vacuum',
                'Particle', 'Universe', 'Cosmos',
                'Rocket', 'Hydro',
                'Atom', 
                '<#robot_px#><#robot_sx_robotic#>',
                '<#hero_pets#>',
                '<#sci_transition_metals#>',
                ],
        'hero_pets':    [
                'Cat', 'Bat', 
                'Hawk',
                'Wolf', 'Lion',
                'Aardvark',
                ],
        'hero_intro_bad':   [
                'the <#hero_adj_evil#> <#hero_name#>, <#hero_superlative_evil#>',
                'the <#hero_adj_evil#> <#hero_name#>, <#hero_superlative_evil#>, <#hero_superlative_evil#>',
                'the <#hero_adj_evil#> <#hero_name#> with his <#hero_superpowers#>',
                'the <#hero_adj_evil#> <#hero_name#> with his <#hero_superpowers#> and <#hero_superpowers#>',
                'the <#hero_adj_evil#> <#heroin_name#>, <#hero_superlative_evil#>',
                'the <#hero_adj_evil#> <#heroin_name#>, <#hero_superlative_evil#>, <#hero_superlative_evil#>',
                'the <#hero_adj_evil#> <#heroin_name#> with her <#hero_superpowers#>',
                'the <#hero_adj_evil#> <#heroin_name#> with her <#hero_superpowers#> and <#hero_superpowers#>',
                ],
        'hero_intro_good':  [
                'the <#hero_adj_good#> <#hero_name#>, <#hero_superlative_good#>',
                'the <#hero_adj_good#> <#hero_name#>, <#hero_superlative_good#>, <#hero_superlative_good#>',
                'the <#hero_adj_good#> <#hero_name#> with <#hero_superpowers#>',
                'the <#hero_adj_good#> <#hero_name#> with <#hero_superpowers#> and <#hero_superpowers#>',
                'the <#hero_adj_good#> <#heroin_name#>, <#hero_superlative_good#>',
                'the <#hero_adj_good#> <#heroin_name#>, <#hero_superlative_good#>, <#hero_superlative_good#>',
                'the <#hero_adj_good#> <#heroin_name#> with <#hero_superpowers#>',
                'the <#hero_adj_good#> <#heroin_name#> with <#hero_superpowers#> and <#hero_superpowers#>',
                ],
        'hero_superlative_evil':    [
                '<#hero_qualification_evil#> than <#hero_comparison_evil#>',
                ],
        'hero_qualification_evil':  [
                'more destructive',
                'stronger',
                'faster',
                'more important',
                'more expensive',
                ],
        'hero_comparison_evil': [
                'a falling meteor',
                'a crashing train',
                'an atomic explosion'
                ],
        'hero_superlative_good':    [
                '<#hero_qualification_good#> than <#hero_comparison_good#>',
                ],
        'hero_qualification_good':  [
                'faster',
                'stronger',
                'speedier',
                'healthier',
                ],
        'hero_comparison_good': [
                'a speeding bullet',
                'the speed of light',
                'the speed of sound',
                'a train',
                'a jet aeroplane',
                'a jet fighter',
                'gravity',
                'the <#num_ord#> law of thermodynamics'
                ],
        'hero_superpowers': [
                'his <#hero_superpowers#>',
                'his <#hero_superpowers#> and <#hero_superpowers#>'
                ],
        'hero_superpowers': [
                '<#hero_superpower_adj#> vision',
                '<#hero_superpower_adj#> power',
                '<#hero_superpower_adj#> grip',
                '<#hero_superpower_adj#> speed',
                '<#hero_superpower_adj#> breath',
                '<#hero_superpower_adj#> hearing',
                '<#hero_superpower_adj#> digestive system',
                '<#hero_superpower_adj#> analytical mind',
                '<#hero_superpower_adj#> mind power',
                '<#hero_superpower_adj#> ESP',
                '<#hero_superpower_adj#> powers of deduction',
                '<#hero_superpower_adj#> force',
                ],
        'hero_superpower_adj':  [
                '<#hero_pets#>like',
                '<#hero_pets#>',
                'X-ray', '<#sci_popularelements#>',
                'freezing', 'unearthly', 'paranormal',
                'mysterious', '<#hero_brand#>',
                '<#robot_px#><#robot_sx_robotic#>',
                'nuclear', 'atomic', 'static',
                'mathematical', 'physical', 'democratic', 
                ],
        'hero_material':    ['<#hero_material_adj#><#robot_px#>tronium', '<#hero_material_adj#><#sci_noble_gasses#>ite', ],
        'hero_material_adj':    [
                '','','','','','','','','',
                'deadly ', 'valuable ', 'priceless ', 'poisenous ', 'illegal ', 'addictive ',  
                ],
        'hero_material_description':    [
                'one <#hero_quantity#> of the material is enough to <#hero_damage#>',
                'one <#hero_quantity#> is sufficient to <#hero_damage#>',
                ],

        'hero_adj': [ 
                '','','',
                '<#hero_adj_good#>',
                '<#hero_adj_evil#>',
                '<#hero_adj_neutral#>',
                ],
        'hero_adj_neutral': ['atomic', 'nuclear'],
        'hero_adj_good':    [
                'last',
                'excellent',
                'powerful',
                'righteous',
                'mighty ',
                'formidable ',
                'unsurpassed ',
                ],
        'hero_adj_evil':    [
                'thundering',
                'dasterdly',
                'heinous',
                'evil ',
                'horrible ',
                'terrible '
                ],
        'hero_city':
            [
            '<#city#>', '<#hero_city_px#>polis', '<#hero_city_px#> City'
            ],
        'hero_city_px': ['Metro','Radio', 'Electro', 'Cosmo', 'Psycho', 'Hydro',],

        #------------------------------------------------------------------------------
        #
        #       stuff for robot names
        #   
        'robot':    [
                '<#robot_px#><#robot_sx_robotic#><#robot_number#>',
                '<#robot_px#><#robot_sx_robotic#><#robot_number#>',
                '<#robot_px#><#robot_sx_computer#><#robot_number#>',
                ],
        'robot_px': [
                'Experimen', 'Galac', 'Destru', 'Infec', 'Demen', 'Demon', 
                'Domina', 'Digi', 'Compu', 'Killa','Radia', 'Atom',
                'Nucleo', 'Urania', 'Proto', 'Neutro', 'Geno', 'Photo', 'Magneto',
                'Quanto', 'Manix', 'Crypto', 'Analy', 'Trans',
                'Op', 'Pho', 'Spec', 'Zy',
                'Robo',
                '<#supersized#>', '<#supersized#>','<#supersized#>', 
                '<#hero_city_px#>',  '<#hero_city_px#>',
                ],
        'robot_sx_robotic': [
                'tor',
                'tron',
                'trix',
                'tator',
                'tra',
                ],
        'robot_sx_computer':    [
                'com',
                'con',
                ],
        'robot_number': [
                '','','','2000', '3000',
                '-<-randint(1,100)->', '-<#num_roman#>',
                '-<-randint(1,10)->', '-<-randint(1,10)->', '-<-randint(1,10)->',
                ],

        
        
        #------------------------------------------------------------------------------
        #
        #       and now putting it all in action:
        #
        'hero_story': [
                '''<#time_day_recentpast#> in <#dumpytown=hero_city#><#dumpytown#>.
                <#guy1=name_male#><#guy1#> and <#guy2=name_male#><#guy2#> overheard <#villain=hero#><#villain#>.
                "Citizens of <#dumpytown#>! <#hero_demands_evil#>" yelled <#villain#>.
                "Oh No!" said <#guy1#>, "We must do something - he will <#hero_damage#>".
                <#guy1#>, a quiet <#hero_altcarreer#> by day, quickly changed into his <#hero_outfit#> and became <#hero1=hero#><#hero1#>: "I will stop him with my <#hero_superpowers#>!" he yelled.
                <#guy2#> did the same and became <#hero2=hero#><#hero2#>, a secret not even his friend <#names_first_absurdlyBritish#> knows about.
                <#hero1#>, <#hero_superlative_good#> and <#hero_superlative_good#>, rushed over to <#villain#>.
                Using the chaos as cover, <#villain#> has broken into <#usbank#>, and was emptying out the safes.
                "You must stop now, <#villain#>!" said <#hero1#>.
                "Never", answered <#villain#>, "I will destroy with my <#poison=hero_material#><#poison#>!, Hahaha!".
                "<#hero_moan#>! -- <#poison#>! I can.. feel.. my powers... weakening...".
                <#hero_onomatopaea#>
                <#hero_onomatopaea#>
                <#hero_voxpopuli_desperate#>
                <#hero_voxpopuli_desperate#>
                "Oh No! <#villain#> is getting the better of <#hero1#>! We are doomed!"
                Desperate, the <#feebleresistance=war_groups#><#feebleresistance#> attacked <#villain#> but their <#war_explosive#>s and <#war_explosive#> did not harm <#villain#>.
                "<#hero_moan#>! Do you think your <#war_explosive#>s can hurt me!?" he yelled. The <#feebleresistance#> fled.
                "Not so fast, <#villain#>" said <#hero2#>, "Get a taste of my <#hero_superpowers#>!"
                <#hero_onomatopaea#>
                <#hero_onomatopaea#>
                <#hero_onomatopaea#>
                <#hero_onomatopaea#>
                <#hero_onomatopaea#>
                "<#hero_moan#>! <#hero2#>, I.. don't.. understand..." said <#villain#>. 
                "Haha! You wonder why your <#poison#> does not harm me?-
                I am in fact <#r2d2=robot#><#r2d2#>! Your powers cannot touch me! and your <#hero_superpowers#> is no match for my <#hero_superpowers#>!"
                The citizens of <#dumpytown#> were overjoyed and made <#r2d2#> alias <#hero2#> <#jobs_jr_directors#> for life.
                <#hero1#> is on the mend and got a medal from Mayor <#name_somewhiteguy#>.
                '''
                ],
        'hero_voxpopuli_desperate': [
                'The citizens of <#dumpytown#> watched the spectacle in terror.',
                'The citizens of <#dumpytown#> watched their beautiful town burn down.',
                'Rioting in <#dumpytown#>, citizens in panic.',
                '''<#hero_moan#>! We're doomed!" yelled the citizens of <#dumpytown#>.''',
                'No one can save us now!',
                "We're done for!",
                ],
        'hero_plans_evil':  [
                '<#hero_damage#> with one <#hero_quantity#> of <#hero_material#>',
                ],
        'hero_demands_evil':    [
                'Give me the <#hero_rewards_evil#> or I will <#hero_plans_evil#>!',
                ],
        'hero_rewards_evil':    [
                'all the <#hero_material#> in the <#hero_locale#>',
                'all your <#hero_material#>',
                'all the <#hero_material#>',
                ],
        'hero_quantity':    ['drop', 'sniff', 'whiff', 'spoonful', 'truckload', 'gram', 'kilo', 'pound', 'suitcase', 'look at'],
        'hero_damage':  [
                'set fire to the <#hero_locale#>',
                'destroy the entire <#hero_locale#>',
                'kill everybody in the <#hero_locale#>',
                ],
        'hero_locale':  ['building', 'block', 'street', 'city', 'country', 'world', 'planet', 'universe'],



}
