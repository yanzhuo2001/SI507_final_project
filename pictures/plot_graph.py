import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def annotate_bars(ax, is_horizontal=False):
    for p in ax.patches:
        value = int(p.get_height()) if not is_horizontal else int(p.get_width())
        x = p.get_x() + p.get_width() / 2
        y = p.get_y() + p.get_height() / 2
        if is_horizontal:
            ax.annotate(f'{value}', (value, y), ha='left', va='center', fontsize=10, color='black', xytext=(5, 0), textcoords='offset points')
        else:
            ax.annotate(f'{value}', (x, value), ha='center', va='bottom', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

def visualize_data(df):
    sns.set(style="whitegrid")

    # 1. 餐厅评分分布图
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='rating', data=df, palette='viridis')
    plt.title('Distribution of Restaurant Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Number of Restaurants')
    annotate_bars(ax)
    plt.show()

    # 2. 餐厅价格范围分布图
    df['price_label'] = df['price'].str.replace('$', 'S')
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='price_label', data=df, palette='viridis', order=['S', 'SS', 'SSS', 'SSSS'])
    plt.title('Distribution of Restaurant Price Ranges')
    plt.xlabel('Price Range')
    plt.ylabel('Number of Restaurants')
    annotate_bars(ax)
    plt.show()

    # 3. 餐厅类别分布图
    categories = df['categories'].explode().apply(lambda x: x['title'])
    top_categories = categories.value_counts().head(50)  # 只显示前20个最常见的类别
    plt.figure(figsize=(10, 10))  # 增加图表的高度
    barplot = sns.barplot(y=top_categories.index, x=top_categories.values, palette='viridis')
    plt.title('Top 20 Restaurant Categories')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Category')

    # 在每个长方形上添加文本
    for index, value in enumerate(top_categories):
        plt.text(value, index, str(value))

    plt.show()

    # 4. 餐厅交易类型分布图
    transactions = df['transactions'].explode()
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x=transactions, palette='viridis')
    plt.title('Distribution of Restaurant Transaction Types')
    plt.xlabel('Transaction Type')
    plt.ylabel('Number of Restaurants')
    annotate_bars(ax)
    plt.show()

def main():
    file_path = 'ann_arbor_restaurants.json'
    df = load_data(file_path)
    visualize_data(df)

main()

