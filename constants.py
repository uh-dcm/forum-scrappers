# A list of constant variables used for scraping
# Storing them separately is intended to improve readability

#UI_constants
ALLOWED_DOMAINS = ['vauva.fi', 'yle.fi', 'hs.fi']

#HS constants


##HS search parameters

HS_TIMES = {'whenever': 'whenever', 'today' : 'today', 'week':'week', 'month':'month'}

HS_CATEGORIES = {'kaikki':'kaikki','autot':'autot','espoo':'espoo','helsinki':'helsinki',
                           'visio':'visio','hsytimessa':'hstimess%C3%A4', 'hsio':'hsio','kirjaarviot':'kirjaarviot',
                           'kolumnit':'kolumnit','koti':'koti', 'kultturi':'kultturi','kuukausiliite':'kuukauisiliite',
                           'lastenuutiset':'lastenuutiset','lifestyle':'lifestyle','maailma':'maailma','mielipide':'mielipide'}

HS_SORTING = {'old-to-new':'old','new-to-old':'new','relevant':'rel'}

HS_PARAMETERS = {'Publishing time' : HS_TIMES, 'Category' : HS_CATEGORIES, 'Sorting' : HS_SORTING}

#Yle constants
#Yle search parameters
YLE_TIMES = {'tanaan' : 'time=today', 'viikko': 'time=week', 'kuukausi' : 'time=month', 'anytime': '' } 

YLE_CATEGORIES = {'uutiset' : 'service=uutiset', 'urheilu' : 'service=urheilu', 'oppiminen' : 'service=oppiminen',
               'elävä-arkisto': 'service=elava-arkisto', 'ylex' : 'service=ylex', 'kaikki' : ''}
YLE_LANGUAGE = {'suomi': '', 'svenska': 'language=sv', 'english': 'language=en', 'russian': 'language=ru',
             'samegiella': 'language=se', 'karjala': 'language=krl', 'kaikki': 'language=all'}

YLE_PARAMETERS = {'Publishing time' : YLE_TIMES, 'Category' : YLE_CATEGORIES, 'Language' : YLE_LANGUAGE}

#Kaksplus search parameters


