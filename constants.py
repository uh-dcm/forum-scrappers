# A list of constant variables used for scraping
# Storing them separately is intended to improve readability

#UI_constants
ALLOWED_DOMAINS = ['vauva.fi', 'yle.fi', 'hs.fi', 'kaksplus.fi', 'kauppalehti.fi']

#Vauva constants
#Vauva parameters

VAUVA_PARAMETERS = {}

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

#Kaksplus constants
#Kaksplus search parameters
KAKSPLUS_FORUM_SECTIONS = {'Aihe vapaa':'2',
                           'Lapsen saaminen':'10054',
                           'Vauvat ja taaperot':'10055',
                           'Lapset ja teinit':'10056',
                           'Perhe-elämä':'10057',
                           'ANNA-Naistentaudit':'10058',
                           'Seksi':'35',
                           'Seksinovellit ja ero-tarinat':'48',
                           'ANNA-Vauvahaavet':'10059',
                           'ANNA-Odotusaika':'10060',
                           'ANNA-Vauvan hoito':'10061',
                           'ANNA-Parisuuhteessa':'10062',
                           'ANNA-Seksi':'10063'
                           }

#Kauppalehti contants
#Kauppalehti forum sections
KAUPPALEHTI_FORUM_SECTIONS = {
    "Kaikki foorumit": "",
    "Sijoittaminen": "1",
    "Kotimaiset osakkeet": "5",
    "Ulkomaiset osakkeet": "2",
    "Asunnot ja kiinteistöt": "13",
    "Kryptot": "38",
    "Aloittelijan palsta": "6",
    "Rahastot ja ETF:t": "15",
    "Unelmasalkku": "39",
    "Yleinen sijoituskeskustelu": "18",
    "Talous": "3",
    "Talous ja talouspolitiikka": "8",
    "Työelämä": "17",
    "Yrittäminen": "14",
    "Yhteiskuntapolitiikka": "28",
    "Lifestyle": "4",
    "Kahvihuone": "12",
    "Autot": "20",
    "Viini ja ruoka": "16",
    "Tiede ja tekniikka": "19",
    "Tiedotteet ja palaute": "37",
    "Tiedotteet": "36",
    "Kehitysehdotukset ja palaute": "7",
    "Testipalsta": "10"
}

#Hevostalli constants
HEVOSTALLI_FORUMS = {
    'Yleinen keskustelu': 1,
    'Ratsastus': 2,
    'Raviurheilu': 3,
    'Hoitajat kohtaavat': 4,
    'Tallielämää': 5,
    'Etsintäkuulutukset': 6,
    'Nuorten nurkka': 7,
    'Seniorit': 9,
    'Leirielämää': 10,
    'Tarinatuokio': 11,
    'Virtuaalitallit': 12,
    'Kyselyt & gallupit': 13,
    'Palautteet & tiedotus': 14,
    'Hevoskasvatus': 15,
    'Ponialue': 16,
    'Mummola': 18
}




