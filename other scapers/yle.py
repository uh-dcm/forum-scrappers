import json
from datetime import datetime

import requests
import pandas as pd

def collect( id ):
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

if __name__ == '__main__':
    print( len( collect( '74-20063567' ) ) )
    df = pd.DataFrame(collect( '20-10007002' )).to_csv('check')