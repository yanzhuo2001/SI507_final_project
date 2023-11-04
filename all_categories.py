import json

def extract_categories(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    categories = set()
    for restaurant in data:
        for category in restaurant.get('categories', []):
            categories.add(category['title'])

    with open('categories.txt', 'w') as f:
        for category in sorted(categories):
            f.write(category + '\n')

extract_categories('ann_arbor_restaurants.json')
