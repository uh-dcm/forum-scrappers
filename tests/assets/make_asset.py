import requests
import os
path = os.getcwd()

url = "https://yle-fi-search.api.yle.fi/v1/search?app_id=hakuylefi_v2_prod&app_key=4c1422b466ee676e03c4ba9866c0921f&language=fi&limit=10&offset=0&query=peruna&type=article"
path = "tests/assets/yle_mock_threads.html"
print(f"mock_response_from_file('{path}', '{url}')")
response = requests.get(url)
if response.status_code == 200:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(response.text)
else:
    print(f"Failed to retrieve the URL. Status code: {response.status_code}")
