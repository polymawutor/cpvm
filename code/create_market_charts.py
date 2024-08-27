import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# Define the directory where the charts will be saved
output_dir = 'charts'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to create and save a time series chart
def create_time_series_chart(csv_file, y_label, title, output_filename, y_formatter=None):
    # Read the CSV file
    df = pd.read_csv(csv_file, parse_dates=['quarter'])
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['quarter'], df[df.columns[1]], marker='o', linestyle='-', color='blue')
    
    # Set the title and labels
    plt.title(title, fontsize=16)
    plt.xlabel('Quarter', fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Format y-axis if formatter is provided
    if y_formatter:
        plt.gca().yaxis.set_major_formatter(y_formatter)
    
    # Add a grid for better readability
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save the chart as a PNG file
    plt.savefig(os.path.join(output_dir, output_filename), bbox_inches='tight')
    
    # Close the plot to avoid memory issues
    plt.close()

# Formatter to convert y-axis to trillions of USD
def trillions_formatter(x, pos):
    return f'${x*1e-12:.1f}T'

# Formatter to convert y-axis to billions of USD
def billions_formatter(x, pos):
    return f'${x*1e-9:.1f}B'

# Corrected market cap data
corrected_market_cap_data = [
    ('2020-01-01', 168100246641.44998),
    ('2020-04-01', 240244504551.83002),
    ('2020-07-01', 310198439777.73),
    ('2020-10-01', 722253660084.1799),
    ('2021-01-01', 1760323040279.1501),
    ('2021-04-01', 1298754847124.62),
    ('2021-07-01', 1736294105376.52),
    ('2021-10-01', 1931812836442.25),
    ('2022-01-01', 1820498614104.86),
    ('2022-04-01', 703137088235.65),
    ('2022-07-01', 755736747396.47),
    ('2022-10-01', 637401308298.2),
    ('2023-01-01', 1025983114283.3699),
    ('2023-04-01', 1047977553856.97),
    ('2023-07-01', 935799828606.54),
    ('2023-10-01', 1462128390624.2002),
    ('2024-01-01', 2431443150784.29),
    ('2024-04-01', 2075014345107.7397)
]

# Convert the corrected data into a DataFrame
corrected_market_cap_df = pd.DataFrame(corrected_market_cap_data, columns=['quarter', 'marketCap'])

# Save the corrected market cap data to a CSV file
corrected_market_cap_df.to_csv('aggregate_market_cap.csv', index=False)

# Create and save charts for each CSV file
create_time_series_chart('aggregate_market_cap.csv', 'Total Market Cap (Trillions USD)', 'Aggregate Market Cap Over Time', 'aggregate_market_cap.png', y_formatter=ticker.FuncFormatter(trillions_formatter))
create_time_series_chart('average_quarterly_price_momentum.csv', 'Average Price Momentum', 'Average Quarterly Price Momentum Over Time', 'average_quarterly_price_momentum.png')
create_time_series_chart('average_quarterly_price_variance.csv', 'Average Price Variance', 'Average Quarterly Price Variance Over Time', 'average_quarterly_price_variance.png')
create_time_series_chart('average_quarterly_volume.csv', 'Average Volume (Billions USD)', 'Average Quarterly Volume Over Time', 'average_quarterly_volume.png', y_formatter=ticker.FuncFormatter(billions_formatter))

print(f"Charts have been saved in the '{output_dir}' directory.")
