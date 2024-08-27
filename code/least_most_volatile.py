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

    ticker_volatilities = {}

    for ticker, prices in data.items():
        returns = calculate_returns(prices)
        if len(returns) > 0:
            variance = calculate_variance(returns)
            volatility = np.sqrt(variance)  # Standard deviation
            ticker_volatilities[ticker] = volatility

    if ticker_volatilities:
        least_volatile_ticker = min(ticker_volatilities, key=ticker_volatilities.get)
        most_volatile_ticker = max(ticker_volatilities, key=ticker_volatilities.get)

        print(f"Number of tickers analyzed: {len(ticker_volatilities)}")
        print(f"\nLeast volatile ticker: {least_volatile_ticker}")
        print(f"Volatility: {ticker_volatilities[least_volatile_ticker]:.6f}")
        print(f"Volatility as percentage: {ticker_volatilities[least_volatile_ticker] * 100:.2f}%")

        print(f"\nMost volatile ticker: {most_volatile_ticker}")
        print(f"Volatility: {ticker_volatilities[most_volatile_ticker]:.6f}")
        print(f"Volatility as percentage: {ticker_volatilities[most_volatile_ticker] * 100:.2f}%")

        # Calculate and print overall market volatility
        average_volatility = np.mean(list(ticker_volatilities.values()))
        print(f"\nOverall market volatility: {average_volatility:.6f}")
        print(f"Overall market volatility as percentage: {average_volatility * 100:.2f}%")
    else:
        print("No valid data found for calculation.")

if __name__ == "__main__":
    main()