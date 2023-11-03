import json
import folium
from folium import IFrame
import networkx as nx
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

all_categories = [
        "African", "American (New)", "American (Traditional)", "Art Galleries", "Asian Fusion", "Bagels", "Bakeries",
        "Barbeque", "Bars", "Beer Bar", "Beer Gardens", "Beer, Wine & Spirits", "Beverage Store", "Boating", "Bowling",
        "Brazilian", "Breakfast & Brunch", "Breweries", "Brewpubs", "Bubble Tea", "Buffets", "Burgers", "Cafes",
        "Cafeteria", "Cajun/Creole", "Car Wash", "Caribbean", "Caterers", "Cheese Shops", "Cheesesteaks", "Chicken Shop",
        "Chicken Wings", "Chinese", "Cocktail Bars", "Coffee & Tea", "Coffee Roasteries", "Comfort Food", "Convenience Stores",
        "Cooking Schools", "Creperies", "Cuban", "Cupcakes", "Dance Clubs", "Delis", "Desserts", "Dim Sum", "Diners",
        "Dive Bars", "Donuts", "Empanadas", "Ethiopian", "Falafel", "Fast Food", "Fish & Chips", "Food Court", "Food Delivery Services",
        "Food Stands", "Food Trucks", "French", "Gastropubs", "Gelato", "German", "Gluten-Free", "Greek", "Grocery", "Halal",
        "Hawaiian", "Himalayan/Nepalese", "Hookah Bars", "Hot Dogs", "Hot Pot", "Hungarian", "Ice Cream & Frozen Yogurt", "Indian",
        "International Grocery", "Irish", "Italian", "Japanese", "Jazz & Blues", "Juice Bars & Smoothies", "Korean", "Kosher",
        "Latin American", "Lebanese", "Lounges", "Meat Shops", "Mediterranean", "Mexican", "Middle Eastern", "Moroccan", "Music Venues",
        "Musical Instruments & Teachers", "New Mexican Cuisine", "Noodles", "Pancakes", "Pasta Shops", "Persian/Iranian", "Pizza", "Poke",
        "Polish", "Pool Halls", "Pop-Up Restaurants", "Pubs", "Ramen", "Restaurants", "Russian", "Salad", "Sandwiches", "Seafood",
        "Seafood Markets", "Singaporean", "Soul Food", "Soup", "Southern", "Spanish", "Specialty Food", "Sports Bars", "Steakhouses",
        "Street Vendors", "Supper Clubs", "Sushi Bars", "Szechuan", "Tacos", "Taiwanese", "Tapas Bars", "Tapas/Small Plates", "Tex-Mex",
        "Thai", "Tobacco Shops", "Turkish", "Vegan", "Vegetarian", "Venues & Event Spaces", "Vietnamese", "Waffles", "Wine Bars", "Wraps"
    ]

def get_input(query1, query2):
    result = None
    while True:
        judge = input(query2)
        if judge.lower() == 'y':
            if query2 == "Filter by categories? (y/n): ":
                show_categories(all_categories)
            result = input(query1)
            if query1 == "Enter price ($, $$, $$$, or $$$$): " and result !='$' and result != '$$' and result != '$$$' and result != '$$$$':
                print("Invalid choice. Please enter $, $$, $$$, or $$$$")
            elif query1 == "Enter minimum rating (0-5): " and (float(result) < 0 or float(result) > 5):
                print("Invalid choice. Please enter a number between 0 and 5.")
            elif query1 == "Enter minimum review count: ":
                try:
                    user_input_as_int = int(result)
                    if user_input_as_int > 0:
                        break
                    else:
                        print("Invalid choice. Please enter a positive integer.")
                except ValueError:
                    print("Invalid choice. Please enter a positive integer.")
            elif query1 == "Filter by transactions? (y/n): " and result != 'pickup' and result != 'delivery' and result != 'restaurant_reservation':
                print("Invalid choice. Please enter pickup, delivery, or restaurant_reservation.")
            elif query1 == "Enter sort by (name, rating, review_count, price): " and result != 'name' and result != 'rating' and result != 'review_count' and result != 'price':
                print("Invalid choice. Please enter name, rating, review_count, or price.")
            else:
                break
        elif judge.lower() == 'n':
            break
        else:
            print("Invalid choice. Please enter y or n.")

    return result

def create_map(df, filename='map.html'):
    # Create a map object
    m = folium.Map(location=[42.2808, -83.7430], zoom_start=13)

    # Add markers to the map
    for index, row in df.iterrows():
        iframe = IFrame(f"<a href='{row['url']}' target='_blank'>{row['name']}</a>", width=200, height=100)
        popup = folium.Popup(iframe, parse_html=True)
        folium.Marker(
            location=[row['coordinates']['latitude'], row['coordinates']['longitude']],
            popup=popup
        ).add_to(m)

    # Save to an HTML file
    m.save(filename)

def show_categories(categories):
    categories = sorted(categories)
    for i, category in enumerate(categories, start=1):
        print(category, end=", " if i % 8 != 0 else "\n")
    if len(categories) % 8 != 0:
        print("\n")

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = nx.Graph()
    for restaurant in data:
        G.add_node(restaurant['id'], **restaurant)
    df = pd.DataFrame.from_records([G.nodes[n] for n in G.nodes])
    return G, df

def search_restaurants(df, query, top_k=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['name'])
    query_vec = vectorizer.transform([query])
    cosine_sim = linear_kernel(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_k:][::-1]
    top_restaurants = df.iloc[top_indices]
    return top_restaurants

def filter_restaurants(df, categories=None, price=None, rating=None, review_count=None, transactions=None, sort_by=None):
    filtered_df = df.copy()
    if categories:
        categories = [c.lower() for c in categories]
        filtered_df = filtered_df[filtered_df['categories'].apply(lambda x: any(c['title'].lower() in categories for c in x))]
    if price:
        filtered_df = filtered_df[filtered_df['price'] == price]
    if rating:
        filtered_df = filtered_df[filtered_df['rating'] >= rating]
    if review_count:
        filtered_df = filtered_df[filtered_df['review_count'] >= review_count]
    if transactions:
        filtered_df = filtered_df[filtered_df['transactions'].apply(lambda x: any(t in transactions for t in x))]
    if sort_by:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)
    return filtered_df

def show_restaurant_details(df, index):
    restaurant = df.iloc[index]
    for key, value in restaurant.items():
        print(f'{key}: {value}')
    # Create a map for the single restaurant
    create_map(df.iloc[[index]])  # Pass a DataFrame containing only the selected restaurant

def main():
    pd.set_option('display.max_rows', None)  # 设置为None表示显示所有行
    pd.set_option('display.max_columns', None)  # 设置为None表示显示所有列
    pd.set_option('display.width', 5000)  # 设置显示的宽度，可以根据需要调整
    G, df = load_data('ann_arbor_restaurants.json')
    create_map(df)  # This will create a map with all restaurants
    
    while True:
        print("1: Search Restaurants")
        print("2: Filter Restaurants")
        print("3: Show Restaurant Details")
        print("4: Exit")
        choice = input("Choose an option: ")


        if choice == '1':
            query = input("Enter search query: ")
            results = search_restaurants(df, query)
            print(results[['name', 'categories', 'rating', 'price']])
            create_map(results)

        elif choice == '2':
            categories = (get_input("Enter categories (comma separated): ", "Filter by categories? (y/n): "))
            if categories != None:
                categories = categories.split(',')
            price = get_input("Enter price ($, $$, $$$, or $$$$): ", "Filter by price? (y/n): ")
            rating = get_input("Enter minimum rating (0-5): ", "Filter by rating? (y/n): ")
            if rating != None:
                rating= float(rating)
            review_count = get_input("Enter minimum review count: ", "Filter by review count? (y/n): ")
            if review_count != None:
                review_count = int(review_count)
            transactions = get_input("Enter transactions (pickup, delivery, restaurant_reservation): ","Filter by transactions? (y/n): ")
            if transactions != None:
                transactions=transactions.split(',')
            sort_by = get_input("Enter sort by (name, rating, review_count, price): ", "Sort results? (y/n): ")

            results = filter_restaurants(df, categories, price, rating, review_count, transactions, sort_by)
            print(results[['name', 'categories', 'rating', 'price']])
            create_map(results)

        elif choice == '3':
            while True:
                print("This function only accepts the index of a restaurant as input.")
                print("You can get the index of a restaurant by searching or filtering.")
                input1 = input("Do you want to continue? (y/n): ").lower()
                if input1 == 'y':
                    index = int(input("Enter restaurant index: "))
                    show_restaurant_details(df, index)
                    break
                elif input1 == 'n':
                    break
                else:
                    print("Invalid choice. Please enter y or n.")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

        print()

main()
