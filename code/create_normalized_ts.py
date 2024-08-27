import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Function to read and preprocess CSV files
def read_and_preprocess(filename):
    df = pd.read_csv(filename)
    df['Quarter'] = pd.to_datetime(df['Quarter'], format='%Y-Q%q')
    return df.set_index('Quarter')

# Read and preprocess the CSV files
market_cap = read_and_preprocess('market_cap_indices.csv')
hcpi = read_and_preprocess('global_average_hcpi.csv')
gdp_growth = read_and_preprocess('global_average_quarterly_gdp_growth.csv')
interest_rates = read_and_preprocess('global_average_short_term_interest_rates.csv')

# Combine all dataframes
combined_df = pd.concat([market_cap, hcpi['Global Average HCPI'], 
                         gdp_growth['Global Average GDP Growth (%)'],
                         interest_rates['Global Average Short-Term Interest Rate']], axis=1)

# Normalize the data
scaler = MinMaxScaler()
normalized_df = pd.DataFrame(scaler.fit_transform(combined_df), 
                             columns=combined_df.columns, 
                             index=combined_df.index)

# Function to create and save charts
def create_chart(data, title, filename):
    plt.figure(figsize=(12, 6))
    for column in data.columns:
        plt.plot(data.index, data[column], label=column)
    plt.title(title)
    plt.xlabel('Quarter')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Create charts for each market cap category
market_caps = ['blue chip', 'mid-cap', 'small-cap']
for cap in market_caps:
    chart_data = normalized_df[[cap, 'Global Average HCPI', 
                                'Global Average GDP Growth (%)',
                                'Global Average Short-Term Interest Rate']]
    create_chart(chart_data, f'Normalized Time Series - {cap.capitalize()}', f'{cap}_chart.png')
    
    # Save corresponding CSV
    chart_data.to_csv(f'{cap}_normalized_data.csv')

print("Charts and CSV files have been created successfully.")