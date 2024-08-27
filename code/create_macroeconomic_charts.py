import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# Define the directory where the charts will be saved
output_dir = 'charts_macroeconomic'
os.makedirs(output_dir, exist_ok=True)

# Function to convert quarter to the first day of the quarter
def quarter_to_timestamp(quarter_str):
    year, quarter = quarter_str.split('-Q')
    year = int(year)
    quarter = int(quarter)
    month = (quarter - 1) * 3 + 1  # Q1 -> January, Q2 -> April, Q3 -> July, Q4 -> October
    return pd.Timestamp(year=year, month=month, day=1)

# Function to create and save a time series chart with dual y-axes
def create_dual_axis_chart(market_cap_csv, macro_csv, macro_col, y_label_macro, title, output_filename):
    # Read the CSV files
    market_cap_df = pd.read_csv(market_cap_csv, parse_dates=['quarter'])
    macro_df = pd.read_csv(macro_csv)
    
    # Convert macro quarterly periods to timestamps
    macro_df['Quarter'] = macro_df['Quarter'].apply(quarter_to_timestamp)

    # Merge the data on the quarter
    merged_df = pd.merge(market_cap_df, macro_df, left_on='quarter', right_on='Quarter')

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot market cap data
    ax1.plot(merged_df['quarter'], merged_df['marketCap'], marker='o', linestyle='-', color='blue', label='Market Cap')
    ax1.set_xlabel('Quarter', fontsize=14)
    ax1.set_ylabel('Market Cap (Billions USD)', fontsize=14, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x*1e-9:.0f}B'))
    
    # Create a second y-axis for the macroeconomic factor
    ax2 = ax1.twinx()
    ax2.plot(merged_df['quarter'], merged_df[macro_col], marker='o', linestyle='-', color='red', label=y_label_macro)
    ax2.set_ylabel(y_label_macro, fontsize=14, color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add titles and legends
    plt.title(title, fontsize=16)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Save the chart as a PNG file
    plt.savefig(os.path.join(output_dir, output_filename), bbox_inches='tight')
    
    # Close the plot to avoid memory issues
    plt.close()

# Create and save charts comparing market cap with each macroeconomic factor
create_dual_axis_chart(
    'aggregate_market_cap.csv',
    'global_average_hcpi.csv',
    'Global Average HCPI',
    'Global Average HCPI',
    'Aggregate Market Cap vs. Global Average HCPI',
    'market_cap_vs_hcpi.png'
)

create_dual_axis_chart(
    'aggregate_market_cap.csv',
    'global_average_quarterly_gdp_growth.csv',
    'Global Average GDP Growth (%)',
    'Global Average GDP Growth (%)',
    'Aggregate Market Cap vs. Global Average GDP Growth',
    'market_cap_vs_gdp_growth.png'
)

create_dual_axis_chart(
    'aggregate_market_cap.csv',
    'global_average_short_term_interest_rates.csv',
    'Global Average Short-Term Interest Rate',
    'Global Average Short-Term Interest Rate (%)',
    'Aggregate Market Cap vs. Global Average Short-Term Interest Rate',
    'market_cap_vs_short_term_interest_rate.png'
)

create_dual_axis_chart(
    'aggregate_market_cap.csv',
    'fear_greed_index.csv',
    'FGI',
    'Fear & Greed Index',
    'Aggregate Market Cap vs. Fear & Greed Index',
    'market_cap_vs_fear_greed_index.png'
)

print(f"Charts have been saved in the '{output_dir}' directory.")
