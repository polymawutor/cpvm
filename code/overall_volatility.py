import csv
import numpy as np # type: ignore

def read_prices_csv(file_path):
    data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        quarters = reader.fieldnames[1:]  # Exclude 'Ticker' column
        for row in reader:
            ticker = row['Ticker']
            prices = [float(row[q]) for q in quarters]
            data[ticker] = prices
    return data, quarters

def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] == 0 or prices[i] == 0:
            returns.append(0)
        else:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns

def calculate_variance(returns):
    return np.var(returns)

def main():
    file_path = 'prices.csv'
    data, quarters = read_prices_csv(file_path)

    total_variance = 0
    valid_tickers = 0

    for ticker, prices in data.items():
        returns = calculate_returns(prices)
        if len(returns) > 0:
            variance = calculate_variance(returns)
            total_variance += variance
            valid_tickers += 1

    if valid_tickers > 0:
        average_variance = total_variance / valid_tickers
        average_volatility = np.sqrt(average_variance)  # Standard deviation

        print(f"Number of tickers analyzed: {valid_tickers}")
        print(f"Average variance: {average_variance:.6f}")
        print(f"Average volatility (standard deviation): {average_volatility:.6f}")
        print(f"Average volatility as percentage: {average_volatility * 100:.2f}%")
    else:
        print("No valid data found for calculation.")

if __name__ == "__main__":
    main()