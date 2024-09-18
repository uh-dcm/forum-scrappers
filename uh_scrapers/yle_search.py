import json
from datetime import datetime

import requests
import pandas as pd





def get_input(allowed_list):
    while True:
        searchconstruct = input("->")
        if searchconstruct in allowed_list:
            return allowed_list[searchconstruct], searchconstruct
        else:
             print("Not applicable input, try again:")

def yle_search_by_query():
    url = []
    
    fields = {'uutiset' : 'service=uutiset', 'urheilu' : 'service=urheilu', 'oppiminen' : 'service=oppiminen',
               'elävä-arkisto': 'service=elava-arkisto', 'ylex' : 'service=ylex', 'kaikki' : ''}
    print('Search category: \n' + "\n".join(fields) + "\n")
    url.append(get_input(fields))



    times = {'tanaan' : 'time=today', 'viikko': 'time=week', 'kuukausi' : 'time=month', 'anytime': '' }         
    print('Choose time period:\n' + "\n".join(times) + "\n")
    url.append(get_input(times))
    
    
    
    lang = {'suomi': '', 'svenska': 'language=sv', 'english': 'language=en', 'russian': 'language=ru',
             'samegiella': 'language=se', 'karjala': 'language=krl', 'kaikki': 'language=all'}
    print('Choose language of the articles:\n' + '\n'.join(lang) + "\n")
    url.append(get_input(lang))
    
    print('Input search query:')
    queryurl="query="
    query=input("->")
    url.append((queryurl + query.replace(" ", "%20"), query))
    filename = [entry[1] for entry in url]
    filename = f'category={filename[0]}&time={filename[1]}&lang={filename[2]}&searchquery={filename[3]}'
    url = [valid[0] for valid in url if valid[0] != '']
    url = "&".join(url)
    collect_threads(url, filename)

#Collect threads for comment scraping from search construct
def collect_threads(searchstr, filename):
    app_id = 'hakuylefi_v2_prod'
    app_key = '4c1422b466ee676e03c4ba9866c0921f'
    nresults= 10
    offset = 0
    url = f'https://yle-fi-search.api.yle.fi/v1/search?app_id={app_id}&app_key={app_key}&limit={nresults}&offset={offset}&type=article&{searchstr}'
    data = requests.get(url)
    data = data.json()
    print(data)
    count = data['meta']['count']
    comment_data = []
    for entry in data['data']:
        comments = collect_comments(entry['id'])
        if 'notifications' not in comments:
            comment_data.extend(comments)

    while offset+nresults < count:
        offset = offset + nresults
        print("offset: ")
        print(offset)
        print("count: ")
        print(count)
        url = f'https://yle-fi-search.api.yle.fi/v1/search?app_id={app_id}&app_key={app_key}&limit={nresults}&offset={offset}&type=article&{searchstr}'
        data = requests.get(url)
        data = data.json()
        for entry in data['data']:
            comments = collect_comments(entry['id'])
            if 'notifications' not in comments:
                comment_data.extend(comments)


    dt = datetime.now()
    filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")

    to_4cat_csv(comment_data, f'scrapedcontent/yle_scraped_{filename_date_string}_{filename}.csv')



#Collect individual comments from a thread
def collect_comments( id ):
    app_key = 'sfYZJtStqjcANSKMpSN5VIaIUwwcBB6D'
    app_id = 'yle-comments-plugin'
    url = f"https://comments.api.yle.fi/v1/topics/{id}/comments/accepted?app_id={app_id}&app_key={app_key}&parent_limit=100"

    data = requests.get( url )
    data = data.json()

    return data


def to_4cat_csv( comments , output_file_name ):
    df = pd.DataFrame( comments )

    newdf = pd.DataFrame()
    newdf['body'] = df['content']
    newdf['author'] = df['author']
    newdf['timestamp'] = df['createdAt'].apply(  lambda date: datetime.strptime(  date , "%Y-%m-%dT%H:%M:%S%z" ).strftime("%Y-%m-%d %H:%M:%S") )
    newdf['id'] = df['id']
    newdf['thread'] = df['topicExternalId']

    newdf.to_csv( output_file_name )
