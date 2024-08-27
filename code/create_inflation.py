import csv
from datetime import datetime
import statistics

def parse_quarter(quarter_str):
    year = int(quarter_str[:4])
    quarter = int(quarter_str[4])
    return datetime(year, ((quarter - 1) * 3) + 1, 1)

def is_valid_value(value):
    try:
        float_value = float(value)
        return float_value > 0
    except ValueError:
        return False

def main():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 7, 1)  # Q2 2024 ends on June 30, 2024

    data = {}
    country_count = {}

    with open('inflation_data_hcpi_q.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country = row['Country']
            for key, value in row.items():
                if key.isdigit() and len(key) == 5:
                    quarter_date = parse_quarter(key)
                    if start_date <= quarter_date < end_date and is_valid_value(value):
                        if quarter_date not in data:
                            data[quarter_date] = []
                            country_count[quarter_date] = set()
                        data[quarter_date].append(float(value))
                        country_count[quarter_date].add(country)

    results = []
    for quarter in sorted(data.keys()):
        avg_hcpi = statistics.mean(data[quarter])
        country_coverage = len(country_count[quarter])
        results.append((quarter, avg_hcpi, country_coverage))

    # Write results to CSV
    with open('global_average_hcpi.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Quarter', 'Global Average HCPI', 'Country Coverage'])
        for quarter, avg_hcpi, coverage in results:
            writer.writerow([quarter.strftime('%Y-Q%q'), f'{avg_hcpi:.2f}', coverage])

    print("Global average HCPI data has been written to 'global_average_hcpi.csv'")

if __name__ == "__main__":
    main()