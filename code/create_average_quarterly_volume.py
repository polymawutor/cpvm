import os
import pandas as pd
from datetime import datetime
import pytz

# Define the directory where the CSV files are stored
prices_folder = 'prices'

# Define the date range for filtering and make them timezone-aware (UTC)
start_date = datetime(2020, 1, 1, tzinfo=pytz.UTC)
end_date = datetime(2024, 6, 30, tzinfo=pytz.UTC)

# Initialize an empty list to store individual DataFrames
all_data = []

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
        # Add the DataFrame to the list
        all_data.append(df)

# Concatenate all the DataFrames in the list
all_data = pd.concat(all_data, ignore_index=True)

# Convert the timestamp to a quarterly period
all_data['quarter'] = all_data['timestamp'].dt.to_period('Q')

# Group by quarter and calculate the average volume
quarterly_avg_volume = all_data.groupby('quarter')['volume'].mean().reset_index()

# Convert the period back to a datetime for output
quarterly_avg_volume['quarter'] = quarterly_avg_volume['quarter'].dt.to_timestamp()

# Save the result to a CSV file
output_file = 'average_quarterly_volume.csv'
quarterly_avg_volume.to_csv(output_file, index=False)

print(f"Average quarterly volume data has been saved to {output_file}")
