import os
import pandas as pd
from datetime import datetime
import pytz

# Define the directory where the CSV files are stored
prices_folder = 'prices'

# Define the date range for filtering and make them timezone-aware (UTC)
start_date = datetime(2020, 1, 1, tzinfo=pytz.UTC)
end_date = datetime(2024, 6, 30, tzinfo=pytz.UTC)

# Initialize a list to store variance data
variance_data = []

# Loop through all the files in the prices folder
for filename in os.listdir(prices_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(prices_folder, filename)
        # Read the CSV file
        df = pd.read_csv(file_path, sep=';', parse_dates=['timestamp'])
        # Convert the timestamp column to datetime using format='mixed'
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        # Filter data within the date range
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        
        # Ensure there are enough data points to calculate variance
        if len(df) > 1:
            # Calculate daily returns as the percentage change in close prices
            df['return'] = df['close'].pct_change()
            # Calculate variance for each quarter
            df['quarter'] = df['timestamp'].dt.to_period('Q')
            quarterly_variance = df.groupby('quarter')['return'].var().reset_index()
            # Add the variance data to the list
            variance_data.append(quarterly_variance)

# Combine all variance data into a single DataFrame
all_variances = pd.concat(variance_data, ignore_index=True)

# Calculate the average variance across all tickers per quarter
avg_quarterly_variance = all_variances.groupby('quarter')['return'].mean().reset_index()

# Convert the period back to a datetime for output
avg_quarterly_variance['quarter'] = avg_quarterly_variance['quarter'].dt.to_timestamp()

# Save the result to a CSV file
output_file = 'average_quarterly_price_variance.csv'
avg_quarterly_variance.to_csv(output_file, index=False)

print(f"Average quarterly price variance data has been saved to {output_file}")
