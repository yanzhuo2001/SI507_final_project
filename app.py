from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from convert_json_map import load_data, search_restaurants, filter_restaurants, show_restaurant_details, create_map

def format_restaurants(data):
    # Check if data is a list and convert to DataFrame if necessary
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # Format the results for the template
    formatted_results = []
    for _, row in data.iterrows():
        # Format categories as a comma-separated string
        formatted_categories = '; '.join([category['title'] for category in row['categories']])
        # Format transactions as a comma-separated string, if they exist
        formatted_transactions = '; '.join(row['transactions']) if 'transactions' in row and row['transactions'] else 'None'
        # Add a dictionary for each restaurant with the desired information
        formatted_results.append({
            'name': row['name'],
            'categories': formatted_categories,
            'rating': row['rating'],
            'price': row['price'],
            'review_count': row['review_count'],
            'transactions': formatted_transactions,
            'url': row['url']  # 添加 Yelp 网址
        })
    return formatted_results

app = Flask(__name__)

# 加载数据和初始化地图
G, df = load_data('ann_arbor_restaurants.json')
create_map(df, 'static/map.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['search_query']
        results = search_restaurants(df, query)
        # Format the results for the template
        formatted_results = format_restaurants(results)
        create_map(results, 'static/map.html')
        return render_template('index.html', restaurants=formatted_results)
    else:
        # Format the results for the template
        formatted_results = format_restaurants(df)
        create_map(df, 'static/map.html')
        return render_template('index.html', restaurants=formatted_results)

@app.route('/filter', methods=['POST'])
def filter_restaurants_route():
    # Process the filtering request
    categories = request.form.get('categories', '').split(',')
    price = request.form.get('price', None)
    rating = request.form.get('rating', None)
    rating = float(rating) if rating else None
    review_count = request.form.get('review_count', None)
    review_count = int(review_count) if review_count else None
    transactions = request.form.get('transactions', '').split(',')
    sort_by = request.form.get('sort_by', None)
    categories = [c.strip() for c in categories if c.strip()]
    transactions = [t.strip() for t in transactions if t.strip()]

    # Call the filter_restaurants function with the processed input
    results = filter_restaurants(df, categories, price, rating, review_count, transactions, sort_by)
    # Format the results for the template
    formatted_results= format_restaurants(results)
    # Save the map with the filtered results
    create_map(results, 'static/map.html')
    # Pass the formatted results to the template
    return render_template('index.html', restaurants=formatted_results)


@app.route('/details/<int:index>', methods=['GET'])
def restaurant_details(index):
    # 显示餐厅详细信息
    restaurant = show_restaurant_details(df, index)
    return jsonify(restaurant.to_dict())

app.run(debug=True)
