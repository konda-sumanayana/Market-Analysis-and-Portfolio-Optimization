import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

def calculate_portfolio_performance(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_return, portfolio_volatility

def monte_carlo_simulation(data, num_portfolios=10000):
    returns = data.pct_change().dropna()
    
    results = []
    for _ in range(num_portfolios):
        weights = np.random.random(len(returns.columns))
        weights /= np.sum(weights)
        portfolio_return, portfolio_volatility = calculate_portfolio_performance(weights, returns)
        results.append([portfolio_return, portfolio_volatility] + list(weights))
    
    columns = ['Returns', 'Volatility'] + list(returns.columns)
    return pd.DataFrame(results, columns=columns)

def negative_sharpe_ratio(weights, returns, risk_free_rate=0.02):
    portfolio_return, portfolio_volatility = calculate_portfolio_performance(weights, returns)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe_ratio

def optimize_portfolio(data):
    returns = data.pct_change().dropna()
    
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    initial_weights = np.array([1/num_assets] * num_assets)
    
    result = minimize(negative_sharpe_ratio, 
                      initial_weights, 
                      args=args,
                      method='SLSQP', 
                      bounds=bounds, 
                      constraints=constraints)
    
    optimal_weights = result.x
    optimal_return, optimal_volatility = calculate_portfolio_performance(optimal_weights, returns)
    
    return optimal_weights, optimal_return, optimal_volatility

if __name__ == "__main__":
    # Example usage
    tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    data = yf.download(tickers, start="2020-01-01", end="2023-12-31")['Adj Close']
    
    mc_results = monte_carlo_simulation(data)
    print("Monte Carlo Simulation Results:")
    print(mc_results.head())
    
    optimal_weights, optimal_return, optimal_volatility = optimize_portfolio(data)
    print("\nOptimal Portfolio:")
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.4f}")
    print(f"Expected Annual Return: {optimal_return:.4f}")
    print(f"Expected Annual Volatility: {optimal_volatility:.4f}")