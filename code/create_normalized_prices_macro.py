import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_process_data(file_path, date_column, value_columns):
    df = pd.read_csv(file_path)
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.set_index(date_column)
    return df[value_columns]

def normalize_series(series):
    return (series - series.min()) / (series.max() - series.min())

def main():
    # Load data
    market_cap = load_and_process_data('market_cap_indices.csv', 'quarter', ['blue chip', 'mid-cap', 'small-cap'])
    hcpi = load_and_process_data('global_average_hcpi.csv', 'Quarter', ['Global Average HCPI'])
    gdp = load_and_process_data('global_average_quarterly_gdp_growth.csv', 'Quarter', ['Global Average GDP Growth (%)'])
    interest_rates = load_and_process_data('global_average_short_term_interest_rates.csv', 'Quarter', ['Global Average Short-Term Interest Rate'])

    # Combine all data
    combined_data = pd.concat([market_cap, hcpi, gdp, interest_rates], axis=1)

    # Normalize data
    normalized_data = combined_data.apply(normalize_series)

    # Create line chart
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    sns.set_palette("husl")

    for column in normalized_data.columns:
        plt.plot(normalized_data.index, normalized_data[column], label=column, linewidth=2)

    plt.title("Normalized Crypto Market Cap Indices and Macroeconomic Indicators", fontsize=16)
    plt.xlabel("Quarter", fontsize=12)
    plt.ylabel("Normalized Value", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('normalized_timeseries.png', dpi=300, bbox_inches='tight')
    print("Chart has been saved as 'normalized_timeseries.png'")

    # Save normalized data to CSV
    normalized_data.to_csv('normalized_timeseries.csv')
    print("Normalized data has been saved to 'normalized_timeseries.csv'")

if __name__ == "__main__":
    main()