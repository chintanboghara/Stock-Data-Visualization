# Stock Data Visualization Application

A modern, interactive web application for visualizing stock data from Yahoo Finance. Built with Python, Streamlit, and Plotly.

## Features

- **Real-time Stock Data**: Fetch current and historical stock data from Yahoo Finance
- **Interactive Charting**: Visualize stock price trends with interactive charts
- **Stock Comparison**: Compare multiple stocks on the same chart with percentage change analysis
- **Financial Metrics**: View key financial metrics and ratios for companies
- **Performance Analysis**: Calculate and display metrics like volatility and maximum drawdown
- **Data Export**: Download stock data as CSV files for further analysis
- **Responsive Design**: Clean, modern UI that works on desktop and mobile devices
- **Caching System**: Efficient data caching to minimize API calls and improve performance

## Technology Stack

- **Frontend & Backend**: Streamlit
- **Data Visualization**: Plotly
- **Data Source**: Yahoo Finance API via yfinance
- **Data Processing**: Pandas, NumPy
- **Containerization**: Docker for easy deployment

## Project Structure

The application follows a production-grade architecture with proper separation of concerns:

```
├── .streamlit/            # Streamlit configuration
├── src/
│   ├── api/               # API integration
│   ├── cache/             # Caching mechanisms
│   ├── components/        # UI components
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── tests/                 # Unit tests
├── app.py                 # Main application
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Docker Compose configuration
```

## Usage

### Running Locally

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

### Using Docker

1. Build the Docker image: `docker-compose build`
2. Run the container: `docker-compose up`
3. Access the application at http://localhost:5000

## Features Usage

### Single Stock Analysis
- Enter a stock symbol (e.g., AAPL, MSFT, GOOGL) in the sidebar
- Select a time period for historical data
- View stock price chart, key metrics, and company information

### Stock Comparison
- Switch to "Stock Comparison" mode in the sidebar
- Enter multiple stock symbols (up to 5)
- View percentage change comparison chart
- Analyze performance metrics for each stock

## Future Enhancements

- Technical indicators (Moving Averages, RSI, MACD)
- Portfolio tracking and analysis
- News integration for relevant stock events
- User accounts to save favorite stocks and custom views
- Advanced filtering and screening options

## Data Sources

This application fetches all data from Yahoo Finance via the yfinance library. The application does not store any financial data locally other than for temporary caching purposes.

## License

MIT License