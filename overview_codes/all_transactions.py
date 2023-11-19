import json

def extract_transactions(file_path, output_file):
    with open(file_path, 'r') as f:
        restaurants = json.load(f)

    with open(output_file, 'w') as f:
        for restaurant in restaurants:
            transactions = restaurant.get('transactions', [])
            for transaction in transactions:
                f.write(transaction + '\n')

extract_transactions('ann_arbor_restaurants.json', 'transactions.txt')
