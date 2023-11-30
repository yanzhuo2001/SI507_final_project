from flask import Flask, render_template, request, jsonify
import pandas as pd
from convert_json_map import load_data, search_restaurants, filter_restaurants, show_restaurant_details, create_map

app = Flask(__name__)

def format_restaurants(data):
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # 将 NaN 值替换为 'N/A'
    data.fillna("N/A", inplace=True)

    formatted_results = []
    for _, row in data.iterrows():
        formatted_categories = '; '.join([category['title'] for category in row['categories']])
        formatted_transactions = '; '.join(row['transactions']) if 'transactions' in row and row['transactions'] else 'None'
        formatted_results.append({
            'name': row['name'],
            'categories': formatted_categories,
            'rating': row['rating'],
            'price': row['price'],
            'review_count': row['review_count'],
            'transactions': formatted_transactions,
            'url': row['url'],
            'coordinates': row['coordinates']
        })
    return formatted_results

# 加载数据和初始化地图
G, df = load_data('ann_arbor_restaurants.json')
create_map(df, 'static/map.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = df.iloc[start:end]
    formatted_results = format_restaurants(paginated_data)
    total_pages = (len(df) + per_page - 1) // per_page

    if request.method == 'POST':
        query = request.form['search_query']
        results = search_restaurants(df, query)
        formatted_results = format_restaurants(results)
        create_map(results, 'static/map.html')

    return render_template('index.html', restaurants=formatted_results, total_pages=total_pages, current_page=page)

@app.route('/api/restaurants', methods=['GET'])
def api_restaurants():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '')
    categories = request.args.get('categories', '')
    price = request.args.get('price', '')
    rating = request.args.get('rating', None)
    rating = float(rating) if rating else None
    review_count = request.args.get('review_count', None)
    review_count = int(review_count) if review_count else None
    transactions = request.args.get('transactions', '')
    sort_by = request.args.get('sort_by', '')

    # 初始筛选为全部数据
    filtered_df = df.copy()

    # 根据查询字符串过滤
    if query:
        filtered_df = filtered_df[filtered_df['name'].str.contains(query, case=False)]

    # 根据分类过滤
    if categories:
        category_list = [category.strip() for category in categories.split(';')]
        filtered_df = filtered_df[filtered_df['categories'].apply(lambda cats: any(cat['title'] in category_list for cat in cats))]

    # 根据价格过滤
    if price:
        filtered_df = filtered_df[filtered_df['price'] == price]

    # 根据评级过滤
    if rating:
        filtered_df = filtered_df[filtered_df['rating'] >= rating]

    # 根据评论数量过滤
    if review_count:
        filtered_df = filtered_df[filtered_df['review_count'] >= review_count]

    # 根据交易类型过滤
    if transactions:
        transaction_list = [transaction.strip() for transaction in transactions.split(';')]
        filtered_df = filtered_df[filtered_df['transactions'].apply(lambda trans: any(t in transaction_list for t in trans))]

    # 实现排序
    if sort_by:
        filtered_df = filtered_df.sort_values(by=sort_by)

    create_map(filtered_df, filename='static/map.html')

    # 实现分页
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = filtered_df.iloc[start:end]
    formatted_results = format_restaurants(paginated_data)
    total_pages = (len(filtered_df) + per_page - 1) // per_page

    return jsonify({
        'restaurants': formatted_results,
        'total_pages': total_pages,
        'current_page': page,
        'map_url': 'static/map.html'  # 添加地图 URL
    })

@app.route('/details/<int:index>', methods=['GET'])
def restaurant_details(index):
    restaurant = show_restaurant_details(df, index)
    return jsonify(restaurant.to_dict())

app.run(debug=True)
