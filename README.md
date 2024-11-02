# Market Analysis Portfolio Optimization

## Description

This project provides an interactive web-based dashboard for portfolio optimization. It allows users to select stocks, run Monte Carlo simulations, and view optimized portfolio allocations. The dashboard is designed to be user-friendly, visually appealing, and informative, even for those without extensive financial knowledge.

## Features

- Interactive stock selection
- Monte Carlo simulation visualization
- Efficient Frontier plot
- Optimized portfolio allocation
- Comparison with S&P 500 index
- User-friendly explanations of financial concepts

## Technologies Used

- Python 3.7+
- Dash (for web application framework)
- Plotly (for interactive visualizations)
- Pandas (for data manipulation)
- NumPy (for numerical computations)
- yfinance (for fetching stock data)
- SciPy (for portfolio optimization)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/portfolio-optimization-dashboard.git
cd portfolio-optimization-dashboard
```

2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the dashboard:
```
python dashboard.py
```

2. Open a web browser and go to `http://127.0.0.1:8050/`

3. Use the dropdown menu to select stocks for your portfolio.

4. Click the "Optimize My Portfolio" button to run the simulation and optimization.

5. Explore the interactive graphs and read the explanations provided.

## Project Structure

- `dashboard.py`: Main application file containing the Dash app and callbacks
- `main.py`: Contains core functions for Monte Carlo simulation and portfolio optimization
- `assets/styles.css`: CSS file for styling the dashboard
- `requirements.txt`: List of Python dependencies
## Results
<img width="1469" alt="Screenshot 2024-11-01 at 9 57 13 PM" src="https://github.com/user-attachments/assets/4f447392-c0fa-4c68-89fc-42f8a031d3cf">
<img width="1422" alt="Screenshot 2024-11-01 at 9 57 24 PM" src="https://github.com/user-attachments/assets/fc60ae99-d97a-455f-a54f-7c8460d6998a">
<img width="1451" alt="Screenshot 2024-11-01 at 9 57 36 PM" src="https://github.com/user-attachments/assets/cb832702-95f4-464f-9c99-34679dcde8d5">
<img width="1326" alt="Screenshot 2024-11-01 at 9 57 46 PM" src="https://github.com/user-attachments/assets/ba07499b-9c63-4f73-b3c6-9929fda4b6ca">


## Customization

- To add more stocks, modify the `options` list in the `stock-selector` Dropdown component in `dashboard.py`.
- Adjust the date range for historical data by modifying the `start` and `end` parameters in the `yf.download()` function call.

## Limitations

- This tool is for educational purposes only and should not be considered as financial advice.
- Past performance does not guarantee future results.
- The optimization is based on historical data and assumes that past trends will continue.

## Future Improvements

- Add more asset classes (e.g., bonds, commodities)
- Implement advanced optimization techniques
- Include risk-adjusted performance metrics
- Add user authentication for personalized portfolios

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

