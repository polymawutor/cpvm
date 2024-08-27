import csv
from datetime import datetime
import pandas as pd

def read_prices_csv(file_path):
    data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        quarters = reader.fieldnames[1:]  # Exclude 'Ticker' column
        for row in reader:
            ticker = row['Ticker']
            prices = [float(row[q]) for q in quarters]
            data[ticker] = prices
    return data, quarters

def read_categories_csv(file_path):
    categories = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            categories[row['Ticker']] = row['Category']
    return categories

def calculate_index(price_data, categories, quarters):
    category_indices = {
        'blue chip': [100] * len(quarters),
        'mid-cap': [100] * len(quarters),
        'small-cap': [100] * len(quarters)
    }
    
    for ticker, prices in price_data.items():
        if ticker in categories:
            category = categories[ticker]
            for i in range(1, len(quarters)):
                if prices[i-1] != 0:
                    return_rate = (prices[i] - prices[i-1]) / prices[i-1]
                    category_indices[category][i] *= (1 + return_rate)

    return category_indices

def main():
    prices_file = 'prices.csv'
    categories_file = 'categories.csv'

    price_data, quarters = read_prices_csv(prices_file)
    categories = read_categories_csv(categories_file)

    indices = calculate_index(price_data, categories, quarters)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(indices, index=quarters)
    df.to_csv('market_cap_indices.csv')
    print("Historical indices have been saved to 'market_cap_indices.csv'")

if __name__ == "__main__":
    main()