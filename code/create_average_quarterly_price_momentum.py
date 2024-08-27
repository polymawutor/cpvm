import os
import pandas as pd
from datetime import datetime
import pytz

# Define the directory where the CSV files are stored
prices_folder = 'prices'

# Define the date range for filtering and make them timezone-aware (UTC)
start_date = datetime(2020, 1, 1, tzinfo=pytz.UTC)
end_date = datetime(2024, 6, 30, tzinfo=pytz.UTC)

# Initialize a list to store momentum data
momentum_data = []

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
        
        # Ensure there are enough data points to calculate momentum
        if len(df) > 1:
            # Convert the timestamp to a quarterly period
            df['quarter'] = df['timestamp'].dt.to_period('Q')
            # Calculate quarterly returns as the percentage change in close prices
            df['quarterly_return'] = df.groupby('quarter')['close'].pct_change()
            # Calculate momentum for each quarter (using the previous quarter's return)
            df['momentum'] = df['quarterly_return'].shift(1)
            # Remove rows where momentum could not be calculated
            df = df.dropna(subset=['momentum'])
            # Add the momentum data to the list
            momentum_data.append(df[['quarter', 'momentum']])

# Combine all momentum data into a single DataFrame
all_momentum = pd.concat(momentum_data, ignore_index=True)

# Calculate the average momentum across all tickers per quarter
avg_quarterly_momentum = all_momentum.groupby('quarter')['momentum'].mean().reset_index()

# Convert the period back to a datetime for output
avg_quarterly_momentum['quarter'] = avg_quarterly_momentum['quarter'].dt.to_timestamp()

# Save the result to a CSV file
output_file = 'average_quarterly_price_momentum.csv'
avg_quarterly_momentum.to_csv(output_file, index=False)

print(f"Average quarterly price momentum data has been saved to {output_file}")
