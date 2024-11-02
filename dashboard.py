import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
import numpy as np

# Import your existing Monte Carlo simulation and optimization functions here
from main import monte_carlo_simulation, optimize_portfolio

# Initialize the Dash app
app = dash.Dash(__name__)

# Define custom CSS
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Custom CSS
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    ),
    
    html.Div([
        html.H1("Easy Portfolio Optimization Dashboard", className='header'),
        
        html.Div([
            html.Label("Select Stocks for Your Portfolio:", className='input-label'),
            dcc.Dropdown(
                id='stock-selector',
                options=[
                    {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                    {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                    {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
                    {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
                    {'label': 'Facebook (FB)', 'value': 'FB'}
                ],
                value=['AAPL', 'MSFT', 'AMZN'],
                multi=True,
                className='dropdown'
            ),
            html.Button('Optimize My Portfolio', id='run-button', n_clicks=0, className='button')
        ], className='input-container'),
        
        html.Div(id='explanation-text', className='explanation'),
        
        html.Div([
            dcc.Graph(id='monte-carlo-plot', className='graph'),
            dcc.Graph(id='efficient-frontier-plot', className='graph')
        ], className='graph-container'),
        
        html.Div(id='optimization-results', className='results'),
        
        html.Div(id='final-explanation', className='explanation')
    ], className='container')
])

@app.callback(
    [Output('monte-carlo-plot', 'figure'),
     Output('efficient-frontier-plot', 'figure'),
     Output('optimization-results', 'children'),
     Output('explanation-text', 'children'),
     Output('final-explanation', 'children')],
    [Input('run-button', 'n_clicks')],
    [State('stock-selector', 'value')]
)
def update_graphs(n_clicks, selected_stocks):
    if n_clicks > 0:
        # Fetch historical data
        data = yf.download(selected_stocks + ['SPY'], start="2020-01-01", end="2023-12-31")['Adj Close']
        
        # Run Monte Carlo simulation
        results = monte_carlo_simulation(data)
        
        # Optimize portfolio
        optimal_weights, optimal_return, optimal_volatility = optimize_portfolio(data)
        
        # Create Monte Carlo plot
        mc_plot = go.Figure()
        mc_plot.add_trace(go.Scatter(x=results['Volatility'], y=results['Returns'],
                                     mode='markers', name='Possible Portfolios',
                                     marker=dict(color=results['Returns'], colorscale='Viridis', size=5)))
        mc_plot.add_trace(go.Scatter(x=[optimal_volatility], y=[optimal_return],
                                     mode='markers', name='Best Portfolio',
                                     marker=dict(size=15, color='red', symbol='star')))
        
        # Calculate S&P 500 return and volatility
        spy_returns = data['SPY'].pct_change().dropna()
        spy_return = spy_returns.mean() * 252
        spy_volatility = spy_returns.std() * np.sqrt(252)
        
        mc_plot.add_trace(go.Scatter(x=[spy_volatility], y=[spy_return],
                                     mode='markers', name='S&P 500',
                                     marker=dict(size=15, color='green', symbol='diamond')))
        
        mc_plot.update_layout(
            title='Portfolio Possibilities',
            xaxis_title='Risk (Volatility)',
            yaxis_title='Potential Annual Return',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        # Create Efficient Frontier plot
        ef_plot = go.Figure()
        ef_plot.add_trace(go.Scatter(x=results['Volatility'], y=results['Returns'],
                                     mode='markers', name='Possible Portfolios',
                                     marker=dict(color=results['Returns'], colorscale='Viridis', size=5)))
        ef_plot.add_trace(go.Scatter(x=[optimal_volatility], y=[optimal_return],
                                     mode='markers', name='Best Portfolio',
                                     marker=dict(size=15, color='red', symbol='star')))
        ef_plot.update_layout(
            title='Best Performing Portfolios',
            xaxis_title='Risk (Volatility)',
            yaxis_title='Potential Annual Return',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        # Calculate Sharpe Ratio (assuming risk-free rate of 0.02)
        optimal_sharpe = (optimal_return - 0.02) / optimal_volatility
        spy_sharpe = (spy_return - 0.02) / spy_volatility
        
        # Prepare results
        results_text = [
            html.H3("Your Optimized Portfolio", className='section-header'),
            html.P("Here's how you should invest your money:"),
            html.Ul([html.Li(f"{stock}: {weight:.2%}") for stock, weight in zip(selected_stocks, optimal_weights)]),
            html.P(f"Expected Annual Return: {optimal_return:.2%}"),
            html.P(f"Expected Risk (Volatility): {optimal_volatility:.2%}"),
            html.P(f"Performance Score (Sharpe Ratio): {optimal_sharpe:.2f}"),
            html.H4("Comparison with S&P 500", className='subsection-header'),
            html.P(f"S&P 500 Expected Return: {spy_return:.2%}"),
            html.P(f"S&P 500 Risk (Volatility): {spy_volatility:.2%}"),
            html.P(f"S&P 500 Performance Score: {spy_sharpe:.2f}"),
            html.P(f"Your Portfolio Outperforms S&P 500 by: {(optimal_return - spy_return):.2%}")
        ]
        
        explanation_text = [
            html.H3("Understanding the Graphs", className='section-header'),
            html.P("Each dot in the graphs represents a possible way to invest your money across the selected stocks."),
            html.P("The horizontal axis shows the risk (volatility) of each portfolio, while the vertical axis shows the potential annual return."),
            html.P("The red star represents the best portfolio we found, balancing high returns with lower risk."),
            html.P("The green diamond shows how the S&P 500 (a common market benchmark) performs for comparison.")
        ]
        
        final_explanation = [
            html.H3("What Does This Mean for You?", className='section-header'),
            html.P("1. The 'Best Portfolio' we've found aims to give you the highest return for a given level of risk."),
            html.P("2. The percentages next to each stock show how much of your money you should consider investing in each."),
            html.P("3. The 'Expected Annual Return' is an estimate of how much your investment might grow in a year."),
            html.P("4. The 'Risk (Volatility)' indicates how much your investment value might fluctuate."),
            html.P("5. The 'Performance Score' (Sharpe Ratio) helps compare investments - a higher score is better."),
            html.P("6. We've compared your portfolio to the S&P 500, which represents the overall US stock market."),
            html.P("Remember: Past performance doesn't guarantee future results. This tool is for educational purposes only and not financial advice.", className='disclaimer')
        ]
        
        return mc_plot, ef_plot, results_text, explanation_text, final_explanation
    
    return {}, {}, [], [], []

if __name__ == '__main__':
    app.run_server(debug=True)