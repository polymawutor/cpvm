import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and preprocess CSV files
def read_csv(filename, date_column='quarter'):
    df = pd.read_csv(filename)
    df[date_column] = pd.to_datetime(df[date_column])
    df.set_index(date_column, inplace=True)
    return df

# Read all CSV files
price_variance = read_csv('average_quarterly_price_variance.csv')
volume = read_csv('average_quarterly_volume.csv')
momentum = read_csv('average_quarterly_price_momentum.csv')
hcpi = read_csv('global_average_hcpi.csv', date_column='Quarter')
gdp_growth = read_csv('global_average_quarterly_gdp_growth.csv', date_column='Quarter')
interest_rates = read_csv('global_average_short_term_interest_rates.csv', date_column='Quarter')
fear_greed = read_csv('fear_greed_index.csv', date_column='Quarter')

# Combine all dataframes
combined_df = pd.concat([
    price_variance['return'],
    volume['volume'],
    momentum['momentum'],
    hcpi['Global Average HCPI'],
    gdp_growth['Global Average GDP Growth (%)'],
    interest_rates['Global Average Short-Term Interest Rate'],
    fear_greed['FGI']
], axis=1)

# Rename columns for clarity
combined_df.columns = ['Price Variance', 'Volume', 'Price Momentum', 'HCPI', 'GDP Growth', 'Interest Rate', 'Fear & Greed Index']

# Calculate correlation matrix
correlation_matrix = combined_df.corr()

# Save correlation matrix to CSV
correlation_matrix.to_csv('correlation_matrix.csv')

# Create heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Matrix of Economic Factors vs Price Variance')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

# Find top 3 correlated factors with Price Variance
correlations_with_price_variance = correlation_matrix['Price Variance'].abs().sort_values(ascending=False)
top_3_factors = correlations_with_price_variance[1:4]  # Exclude Price Variance itself

print("Top 3 highly correlated factors with Price Variance:")
print(top_3_factors)

print("\nCorrelation matrix saved to 'correlation_matrix.csv'")
print("Correlation heatmap saved to 'correlation_heatmap.png'")