import csv
import os
from datetime import datetime
from collections import defaultdict

def get_quarter(date):
    month = date.month
    return (month - 1) // 3 + 1

def get_quarter_key(date):
    return f"Q{get_quarter(date)} {date.year}"

def parse_timestamp(timestamp):
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",  # Format with milliseconds
        "%Y-%m-%dT%H:%M:%SZ"      # Format without milliseconds
    ]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse timestamp: {timestamp}")

def process_price_files(prices_folder):
    quarterly_prices = defaultdict(lambda: defaultdict(float))
    quarters = [f"Q{q} {y}" for y in range(2020, 2025) for q in range(1, 5)][:18]  # Up to Q2 2024

    for filename in os.listdir(prices_folder):
        if filename.endswith('.csv'):
            ticker = filename[:-4]  # Remove .csv extension
            file_path = os.path.join(prices_folder, filename)
            
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    try:
                        date = parse_timestamp(row['timestamp'])
                        quarter_key = get_quarter_key(date)
                        if quarter_key in quarters:
                            quarterly_prices[ticker][quarter_key] = float(row['close'])
                    except ValueError as e:
                        print(f"Error processing {filename}: {e}")

    return quarterly_prices, quarters

def write_prices_csv(quarterly_prices, quarters, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Ticker'] + quarters
        writer.writerow(header)

        for ticker, prices in quarterly_prices.items():
            row = [ticker] + [prices.get(quarter, 0) for quarter in quarters]
            writer.writerow(row)

def main():
    prices_folder = 'prices'
    output_file = 'prices.csv'

    quarterly_prices, quarters = process_price_files(prices_folder)
    write_prices_csv(quarterly_prices, quarters, output_file)

    print(f"Prices have been written to {output_file}")

if __name__ == "__main__":
    main()