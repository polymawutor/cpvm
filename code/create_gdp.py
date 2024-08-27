import csv
from datetime import datetime
import statistics

def parse_quarter(quarter_str):
    year, quarter = quarter_str.split('-Q')
    return datetime(int(year), ((int(quarter) - 1) * 3) + 1, 1)

def is_valid_value(value):
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False

def main():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 7, 1)  # Q2 2024 ends on June 30, 2024

    data = {}
    country_count = {}

    with open('gdp_raw.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country = row['REF_AREA']
            quarter_str = row['TIME_PERIOD']
            value = row['OBS_VALUE']

            if quarter_str and is_valid_value(value):
                quarter_date = parse_quarter(quarter_str)
                if start_date <= quarter_date < end_date:
                    if quarter_date not in data:
                        data[quarter_date] = []
                        country_count[quarter_date] = set()
                    data[quarter_date].append(float(value))
                    country_count[quarter_date].add(country)

    results = []
    for quarter in sorted(data.keys()):
        avg_gdp_growth = statistics.mean(data[quarter])
        country_coverage = len(country_count[quarter])
        results.append((quarter, avg_gdp_growth, country_coverage))

    # Write results to CSV
    with open('global_average_quarterly_gdp_growth.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Quarter', 'Global Average GDP Growth (%)', 'Country Coverage'])
        for quarter, avg_growth, coverage in results:
            writer.writerow([quarter.strftime('%Y-Q%m'), f'{avg_growth:.4f}', coverage])

    print("Global average quarterly GDP growth has been written to 'global_average_quarterly_gdp_growth.csv'")

if __name__ == "__main__":
    main()