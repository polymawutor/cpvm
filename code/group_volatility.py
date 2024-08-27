import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] == 0 or prices[i] == 0:
            returns.append(0)
        else:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns

def calculate_volatility(returns):
    return np.std(returns)

def main():
    prices_file = 'prices.csv'
    categories_file = 'categories.csv'

    price_data, _ = read_prices_csv(prices_file)
    categories = read_categories_csv(categories_file)

    category_volatilities = {
        'blue chip': [],
        'mid-cap': [],
        'small-cap': []
    }

    for ticker, prices in price_data.items():
        if ticker in categories:
            returns = calculate_returns(prices)
            volatility = calculate_volatility(returns)
            category = categories[ticker]
            category_volatilities[category].append(volatility)

    avg_volatilities = {cat: np.mean(vols) for cat, vols in category_volatilities.items() if vols}

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.set_palette("deep")

    bars = plt.bar(avg_volatilities.keys(), avg_volatilities.values())

    plt.title('Average Volatility by Market Cap Category', fontsize=16, fontweight='bold')
    plt.xlabel('Market Cap Category', fontsize=12)
    plt.ylabel('Average Volatility', fontsize=12)

    # Adding value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.4f}',
                 ha='center', va='bottom')

    # Customizing the plot
    plt.ylim(0, max(avg_volatilities.values()) * 1.1)  # Add some space above the bars
    plt.xticks(rotation=0)

    # Add a brief explanation
    plt.figtext(0.5, -0.05, 
                "Volatility measured as standard deviation of quarterly returns (Q1 2020 - Q2 2024)",
                ha="center", fontsize=10, style='italic')

    plt.tight_layout()
    plt.savefig('volatility_by_category.png', dpi=300, bbox_inches='tight')
    print("Chart has been saved as 'volatility_by_category.png'")

if __name__ == "__main__":
    main()