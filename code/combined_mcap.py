import csv
import os
from datetime import datetime

def parse_timestamp(timestamp):
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse timestamp: {timestamp}")

def get_q2_2024_end_date():
    return datetime(2024, 6, 30)

def process_price_files(prices_folder):
    q2_2024_end = get_q2_2024_end_date()
    total_market_cap = 0

    for filename in os.listdir(prices_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(prices_folder, filename)
            
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                latest_date = datetime.min
                latest_market_cap = 0

                for row in reader:
                    try:
                        date = parse_timestamp(row['timestamp'])
                        if date <= q2_2024_end and date > latest_date:
                            latest_date = date
                            latest_market_cap = float(row['marketCap'])
                    except ValueError as e:
                        print(f"Error processing {filename}: {e}")

                if latest_date > datetime.min:
                    total_market_cap += latest_market_cap

    return total_market_cap

def main():
    prices_folder = 'prices'
    total_market_cap = process_price_files(prices_folder)

    print(f"Total Market Cap at the end of Q2 2024: ${total_market_cap:,.2f}")

if __name__ == "__main__":
    main()