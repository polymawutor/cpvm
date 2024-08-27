import csv
import os
import numpy as np
import matplotlib.pyplot as plt

def read_volume_data(folder_path, ticker):
    file_path = os.path.join(folder_path, f"{ticker}.csv")
    volumes = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                volumes.append(float(row['volume']))
    return volumes

def read_categories_csv(file_path):
    categories = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            categories[row['Ticker']] = row['Category']
    return categories

def calculate_average_quarterly_volume(volumes):
    return np.mean(volumes) if volumes else 0

def main():
    prices_folder = 'prices'
    categories_file = 'categories.csv'

    categories = read_categories_csv(categories_file)

    category_volumes = {
        'blue chip': 0,
        'mid-cap': 0,
        'small-cap': 0
    }

    category_counts = {cat: 0 for cat in category_volumes}

    for ticker, category in categories.items():
        volumes = read_volume_data(prices_folder, ticker)
        if volumes:
            avg_volume = calculate_average_quarterly_volume(volumes)
            category_volumes[category] += avg_volume
            category_counts[category] += 1

    # Calculate average volume per category
    for category in category_volumes:
        if category_counts[category] > 0:
            category_volumes[category] /= category_counts[category]

    # Remove categories with zero volume
    category_volumes = {k: v for k, v in category_volumes.items() if v > 0}

    # Plotting
    plt.figure(figsize=(10, 8))
    plt.pie(category_volumes.values(), labels=category_volumes.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1(np.arange(len(category_volumes))))
    plt.title('Average Quarterly Volume Distribution by Market Cap Category', fontsize=16, fontweight='bold')

    # Add a legend
    plt.legend(title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Add a brief explanation
    plt.figtext(0.5, -0.05, 
                "Average quarterly volume calculated from available data in price files",
                ha="center", fontsize=10, style='italic')

    plt.tight_layout()
    plt.savefig('volume_distribution_by_category.png', dpi=300, bbox_inches='tight')
    print("Chart has been saved as 'volume_distribution_by_category.png'")

    # Print out the average volumes
    print("\nAverage Quarterly Volumes:")
    for category, volume in category_volumes.items():
        print(f"{category}: {volume:.2e}")

if __name__ == "__main__":
    main()