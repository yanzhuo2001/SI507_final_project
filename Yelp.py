import requests
import json
import time

api_key = 'xjBZe7_IvwLXcaUPxWrfcvMT-Xw1rUxNlx4PSdvHx6jSzUp-YYZyHLo3SzXGIlWR8261_pGwuoTo8hhAZEeioWQIhB9k1freKyv8v-lMMSihaQZyakMhlPHXO_c_ZXYx'
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': f'Bearer {api_key}'}
params = {'location': 'Ann Arbor', 'categories': 'restaurants', 'limit': 50}

restaurants = []

for offset in range(0, 1000, 50):  # Yelp API allows up to 1000 results, 50 results per request
    params['offset'] = offset
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    restaurants.extend(data.get('businesses', []))
    time.sleep(0.1)  # To avoid hitting Yelp's rate limit

with open('ann_arbor_restaurants.json', 'w') as f:
    json.dump(restaurants, f)

print('Finished saving restaurant information.')
