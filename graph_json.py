import json
import networkx as nx

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_graph(restaurants):
    G = nx.Graph()
    for restaurant in restaurants:
        # 使用餐厅的ID作为节点，并将所有餐厅信息作为节点属性
        restaurant_id = restaurant['id']
        G.add_node(restaurant_id, **restaurant)

        # 为每个餐厅和其类别之间创建边
        for category in restaurant['categories']:
            category_alias = category['alias']
            if not G.has_node(category_alias):
                G.add_node(category_alias, type='category')
            G.add_edge(restaurant_id, category_alias)
    return G

def save_graph(graph, file_path):
    data = nx.readwrite.json_graph.node_link_data(graph)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    restaurants_data = load_data('ann_arbor_restaurants.json')
    graph = create_graph(restaurants_data)
    save_graph(graph, 'graph.json')

if __name__ == "__main__":
    main()
