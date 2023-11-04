import json

def extract_transactions(file_path, output_file):
    with open(file_path, 'r') as f:
        restaurants = json.load(f)

    with open(output_file, 'w') as f:
        for restaurant in restaurants:
            review_count = restaurant.get('review_count', 0)  # 默认值设置为0，以防没有'review_count'字段
            f.write(str(review_count) + '\n')

extract_transactions('ann_arbor_restaurants.json', 'review_count.txt')
