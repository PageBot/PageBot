# -*- coding: UTF-8 -*-
#
"""
        history
        Names of cities, countries, addresses.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

"""

__version__ = '4.0'



# ------------------------------------------------------
#    geography
#
content = {
    'location':    ['<#cities_hip#>', '<#city_and_state#>'],
    'cities_hip':    [
            'New York',
            'Stockholm',
            'Den Haag',
            'London',
            'Berlin',
            'Tokyo',
            'Sao Paolo'
            ],

    'state_name'    :    ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District Of Columbia','Florida','Georgia','Hawaii','Idaho',
            'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana',
            'Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico',
            'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virgin Islands','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],

    'state_abbr'    :    ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
            'NM','NY','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VI','VA','WA','WV','WI','WY'],

    'state_abbr_lc'    :    ['al','ak','az','ar','ca','co','ct','de','dc','fl','ga','hi','id','il','in','ia','ks','ky','la','me','md','ma','mi','mn','ms','mo','mt','ne','nv','nh','nj',
            'nm','ny','nd','oh','ok','or','pa','pr','ri','sc','sd','tn','tx','ut','vt','vi','va','wa','wv','wi','wy'],

    'country'        :    ['the United States','Argentina','Australia','Austria','Belgium','Brazil','Canada','Denmark','Finland','France','Germany','Hong Kong','Italy','Japan',
            'The Netherlands','New Zealand','Norway','Portugal','Singapore','Spain','Sweden','Switzerland','United Kingdom','Afghanistan','Albania','Algeria','American Samoa',
            'Andorra','Angola','Anguilla','Antarctica','Antigua and Barbuda','Armenia','Aruba','Ascension Island','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados',
            'Belarus','Belize','Benin','Bermuda','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Bouvet Island','British Virgin Islands','Brunei','Bulgaria','Burkina Faso',
            'Burundi','Cambodia','Cameroon','Cape Verde','Cayman Islands','Central African Republic','Chad','Channel Islands, Guernsey','Channel Islands, Jersey','Chile',
            'China','Christmas Island','Cocos Islands','Colombia','Comoros','Congo','Congo (Zaire)','Cook Islands','Costa Rica','Croatia','Cuba','Cyprus','Czech Republic',
            'Djibouti','Dominica','Dominican Republic','East Timor','Ecuador','Egypt','El Salvador','Equatoral Guinea','Eritrea','Estonia','Ethiopia','Falkland Islands',
            'Faroe Islands','Fiji','French Guiana','French Polynesia','French Southern Territories','Gabon','Gambia','Georgia','Ghana','Gibraltar','Greece','Greenland','Grenada',
            'Guadeloupe','Guam','Guatemala','Guinea','Guinea Bissau','Guyana','Haiti','Heard Island','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland',
            'Isle of Man','Israel','Ivory Coast','Jamaica','Jordan','Kazakhstan','Kenya','Kiribati','Kuwait','Kyrgyz Republic','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya',
            'Liechtenstein','Lithuania','Luxembourg','Macau','Macedonia','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Martinique','Mauritania',
            'Mauritius','Mayotte','McDonald Islands','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nauru',
            'Nepal','Netherlands Antilles','New Caledonia','Nicaragua','Niger','Nigeria','Niue','Norfolk Island','North Korea','Northern Mariana Islands','Pakistan','Palau','Panama',
            'Papua New Guinea','Paraguay','Peru','Philippines','Pitcairn','Poland','Puerto Rico','Qatar','Reunion Island','Romania','Russia','Rwanda','Samoa','San Marino',
            'Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Sierra Leone','Slovak Republic','Slovenia','Solomon Islands','Somalia','South Africa','South Georgia',
            'South Korea','South Sandwich Islands','Sri Lanka','St. Helena','St. Kitts-Nevis','St. Lucia','St. Pierre and Miquelon','St. Vincent and the Grenadines','Sudan',
            'Sultanate Of Oman','Suriname','Svalbard and Jan Mayen Islands','Swaziland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Togo','Tokelau','Tonga',
            'Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine','United Arab Emirates','Uruguay','Uzbekistan',
            'Vanuatu','Vatican City','Venezuela','Vietnam','Virgin Islands','Wallis and Futuna Islands','Western Sahara','Yemen','Yugoslavia','Zambia','Zimbabwe'],

    'countries_major'    :    ['United States','Argentina','Australia','Austria','Belgium','Brazil','Canada','Denmark','Finland','France','Germany','Hong Kong','Italy','Japan',
            'Netherlands','New Zealand','Norway','Portugal','Singapore','Spain','Sweden','Switzerland','United Kingdom'],
    'nationality_major':
            [
            '<#politics_euro_nationality#>',
            'Canadian',
            'Russian',
            'Chinese',
            'Japanese',
            'Arab',
            'American',
            ],
    'politics_euro_nationality':    ['French', 'Dutch', 'British','European','German', 'Croat', 'Serb', 'Turkish',
                            'Belgium','Swiss', 'Danish', 'Norwegian', 'Swedish', 'Finnish','Russian',
                            'Italian','Spanish','Austrian','Portugese','Maltesian','Polish'],
    'us_telephone': [
            '+1 (<#figs_rand_03digit#>) <#figs_rand_03digit#> <#figs_rand_04digit#>',
    ],
    'address_street'        :    [
            'Street','Street','Street',
            'Avenue','Avenue','Avenue',
            'Way','Road','Place','Boulevard','Close','Center','Plaza','Crescent','Terrace','Drive','Circle',
            ],
    'address_floor'        :    [
            '','','',
            '<#figs_ord#> Floor, ',
            'Suite <#figs_nonzero#><#figs#><#figs#>, ',
            'MS: <#figs_nonzero#><#figs#><#alphabet_caps#><#alphabet_caps#>-<#figs#><#figs#>, ',
            ],
    'address' : [
            '<#figs_nonzero#><#figs#><#figs#> <#names_last_patrician#> <#address_street#>, <#address_floor#><#town_us#>, <#state_abbr#>.',
            '<#figs_rand_5digit#> <#figs_nonzero#><#figs_ord#> Street, <#address_floor#><#town_us#>, <#state_abbr#>.',
            '<#figs_rand_5digit#> <#_scarycartel=names_last_patrician#><#_scarycartel#> <#address_street#>, <#address_floor#><#_scarycartel#>, <#state_abbr#>.',
            'P.O. Box <#figs_rand_5digit#>, <#names_last_patrician#> Station, <#town_us#>, <#state_abbr#>.'
            ],
    'city_and_state': [
            'Palo Alto, CA',
            'Menlo Park, CA',
            'Redwood City, CA',
            'Sunnyvale, CA',
            'Reston, VA',
            'Herndon, VA',
            'Atlanta, GA',
            'Boston, MA',
            'New York, NY',
            ],
    'island': [
            'Nauru', 'Caymann Island', 'Corfu', 'Tuvalu', 'Whight', 'Mircky Island', 'Mastumba', 'Bali', 'Texel', 'Terschelling',
            'Bornholm', u'Fanø', u'Rømø', 'Lolland', 'Barbados', 'Bermuda', 'Bonaire', 'British Virgin Islands', u'Curaçao',
            'Aruba', 'St.Maarten', 'St.Lucia', 'Mauritius', 'Bahrain', 'Palau', 'Belize', 'Cape Verde', 'Samoa', 'Comoros',
            'Cuba', 'Singapore', 'St.Kitts', 'Fiji', 'Grenada', 'Guinea-Bissau', 'Jamaica', 'Seychelles', 'Grenada',
            u'Timor-Lesté', 'Kiribati', 'Trinidad', 'Tobago', 'Maldives', 'Marshall Island', 'Vanuatu',
            ],
    'mountain': [
            'Ahaggar Mountains (3,003 m)', 'Auasberge (2,485 m)',u'Aïr Mountains (2,022 m)','Chappal Waddi (2,419 m)',
            'Cathkin Peak (3,377 m)','Emi Koussi (3,445 m)','Kompassberg (2,500 m)','Mount Moco (2,620 m)',
            'Mount Baker (4,844 m)','Mount Cameroon (4,040 m)','Mount Elgon (4,321 m)','Mount Emin (4,798 m)',
            'Mount Gessi (4,715 m)','Impati Mountain (1,600 m)','Mount Kadam (3,063 m)','Mount Karisimbi (4,507 m)',
            'Mount Kenya (5,199 m)','Mount Kilimanjaro (5,895 m)','Mount Kinyeti (3,187 m)','Mount Luigi di Savoia (4,627 m)',
            'Mount Meru (4,566 m)','Mount Hanang (3,417 m)','Mount Moroto (3,083 m)','Mount Morungole (2,750 m)',
            'Mount Mulanje (3,002 m)','Pico del Teide (3,717 m)',
            ],
    'ocean': [
            'Pacific Ocean', 'Atlantic Ocean', 'Arctic Ocean', 'Indian Ocean', 'Southern Ocean',
            ],
    'sea':    ['Bay of <#sea_single#>','<#sea_single#> Bay','<#sea_single#> Ocean','<#sea_single#> Passage',
            '<#sea_single#> Sea','<#sea_single#> Sea','<#sea_single#> Sea',
            '<#town_us_compass#> <#sea_single#> Sea', '<#town_us_compass#> <#sea_single#> Bay',
            'Sea of <#sea_single#>','Sea of <#sea_single#>','<#^,colors_primary#> Sea', 'Gulf of <#sea_single#>',
            'Strait of <#sea_single#>','Passage of <#sea_single#>',
            'Coastal Waters of <#country#>', 'Coastal Waters of <#sea_single#>','Coast of <#country#>',
            ],
    'sea_single': ['Adriatic','Alboran','Adriatic','Aegean','Alboran','Arafura','Arctic','Baffin','Balearic','Bali',
            'Banda','Barents', 'Bengal','Biscay','Fundy','Beaufort','Bering','Biscayne','Celebes','Chesapeake','Coral',
            'Chukchi','Siberia','<#state_name#>','<#state_name#>','<#state_name#>','<#state_name#>','<#country#>',
            ],
    'city':     [
            '<#cities_USmajor#>',
            '<#cities_UK#>',
            '<#cities_German#>',
            '<#cities_Italian#>',
            '<#cities_Spanish#>',
            '<#cities_Dutch#>',
            '<#cities_French#>'],

    'cities_USmajor': [
            'New York',
            'Boston',
            'Chicago',
            'Washington',
            'Los Angeles',
            'San Francisco',
            'Seattle',
            'Dallas',
            'Baltimore',
            'Philadelphia',
            'Pittsburgh',
            'San Jose',
            'Denver',
            'Minneapolis',
            'Houston',
            'Miami',
            'Atlanta',
            'Memphis',
            'Nashville',
            'Detroit',
            'Kansas City'
            ],           
    'abbr_cities_USmajor':[
            'New York', 'NYC',
            'Boston',
            'Chicago',
            u'Washin’',
            'LA',
            'SF',
            'Seattle',
            'Dallas',
            'Baltim',
            'Philly',
            'Pitts',
            'Denver',
            'Minny', 'Twin', 'St.Paul',
            'Houston',
            'Miami',
            'Atlanta',
            'Memphis',
            u'Nash’',
            'Detroit',
            'Kansas',
            'Tisbury',
            'Vineyard',
            # And short state names
            'Alabama','Alaska','Arizona','Arkansas','Cal','Florida','Georgia','Hawaii','Idaho',
            'Illinois','Indiana','Iowa','Kansas','Maine','Missouri','Montana',
            'Nebraska','Nevada','Ohio','Oregon','Texas','Utah','Vermont','Wyoming'
    ],
    'cities_USgeneric': [
            '<#county_US#> County',
            '<#towns_USgeneric#>',
            '<#town_us#>',
            '<#town_us#>',
            '<#town_us#>',
            '<#town_us#>',
            '<#town_us#>',
            '<#towns_USgeneric#>, <#county_US#> County',
            '<#town_us#>, <#county_US#> County',
            '<#towns_USgeneric#> (<#county_US#> County)',
            '<#town_us#> (<#county_US#> County)',
            ],

    'towns_USgeneric': [
            'Columbus',
            'Springfield',
            'Lincoln'
            ],

    'town_us':    [
            '<#town_us_px#><#town_us_sx#>',
            '<#town_us_px#><#town_us_sx#>',
            '<#town_us_px#><#town_us_sx#>',
            '<#town_us_qualifier#> <#town_us_px#><#town_us_sx#>',
            '<#names_last_patrician#>',
            '<#town_us_qualifier#> <#names_last_patrician#>',
            ],

    'town_us_qualifier':    [
            'New',
            'Mount',
            'Cape',
            '<#town_us_compass#>'
            ],

    'town_us_px': [
            'Mil',
            'Peter',
            'Adams',
            'Lawrence',
            'Taylor',
            'Bedford',
            'Jones',
            'Johns',
            'Harris',
            'George',
            'Fredericks',
            'Pine',
            'Wood',
            'Over',
            'Smiths',
            'Williams',
            'Williamson',
            'Chester',
            'Middle',
            'River',
            ],

    'town_us_sx':    [
            'ville',
            'town',
            'ton',
            'burg',
            'burgh',
            'field',
            'ford',
            'dale',
            'vale',
            'port',
            'hill'
            ],

    'town_us_compass':    [
            'North',
            'West',
            'East',
            'South'
            ],

    'county_US':    [
            'Jefferson',
            'Fairfax',
            'Orange',
            'Montgomery',
            'Washington',
            'Elwood',
            'Cook',
            'Essex',
            'Sussex',
            'Suffolk',
            'Norfolk',
            'Monroe',
            'Adams',
            'Knox',
            '<#names_last_patrician#>'
            ],
    'continents': ['Africa', 'Asia', 'Eurasia', 'Eurafrasia', 'Antarctica', 'Europe', 'Oceania',
                'Australia', 'America',
            ],
    'continents_parts': ['<#town_us_compass#> <#continents#>'],
    'cities_Russia':    [
            'Moscow',
            'St. Petersburg',
            'Kiev',
            ],

    'cities_UK': [
            'London',
            'Liverpool',
            'Leeds',
            'Manchester',
            'Sheffield',
            'Glasgow',
            'Edinburgh',
            'Oxford',
            'Cambridge'
            ],

    'cities_Spanish': [
            'Madrid',
            'Barcelona',
            'Bilbao',
            ],

    'cities_German': [
            'Berlin',
            'Frankfurt',
            'Munich',
            'Hamburg',
            'Bonn'
            ],

    'cities_Italian': [
            'Rome',
            'Milan',
            'Florence',
            'Bologna'
            ],

    'cities_Dutch': [
            'Amsterdam',
            'Rotterdam',
            'The Hague',
            'Eindhoven',
            'Haarlem',
            'Leiden',
            'Delft',
            'Maastricht',
            'Utrecht',
            'Arnhem',
            'Gouda',
            ],

    'cities_French': [
            'Paris',
            'Lyon',
            'Marseilles',
            'Liege',
            'Lille',
            'Toulouse'
            ],
    'geographicplace': ['city','county','country','island','republic','contintent'],
    }

