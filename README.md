# Stock Data Visualization

A modern, interactive web application for visualizing and analyzing stock data from Yahoo Finance. Built with Python, Streamlit, and Plotly.

## Overview

Stock Data Visualization empowers users to explore stock market data with ease through a variety of powerful features, all wrapped in a responsive and intuitive interface.

## Features

- **Real-time Stock Data**
  - Fetch current and historical stock data from Yahoo Finance
- **Interactive Charting**
  - Visualize stock price trends with interactive, customizable charts
- **Stock Comparison**
  - Compare multiple stocks on a single chart
  - Analyze percentage change for deeper insights
- **Financial Metrics**
  - Access key financial metrics and ratios for companies
- **Performance Analysis**
  - Calculate metrics like volatility and maximum drawdown
- **Data Export**
  - Export stock data as CSV files for offline analysis
- **Responsive Design**
  - Enjoy a clean, modern UI optimized for desktop and mobile
- **Caching System**
  - Leverage efficient data caching to reduce API calls and boost performance

## Technology Stack

- **Frontend & Backend**: [Streamlit](https://streamlit.io/) - A Python library for building web apps with minimal code
- **Data Visualization**: [Plotly](https://plotly.com/) - A graphing library for interactive visualizations
- **Data Source**: [Yahoo Finance API](https://finance.yahoo.com/) via [yfinance](https://github.com/ranaroussi/yfinance) - A trusted stock data provider
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) - Core libraries for data manipulation and analysis
- **Containerization**: [Docker](https://www.docker.com/) - Ensures consistent deployment across environments

## Project Structure

The project adheres to a production-grade architecture with clear separation of concerns:

```
├── .streamlit/            # Streamlit configuration files
├── src/
│   ├── api/               # API integration logic
│   ├── cache/             # Data caching mechanisms
│   ├── components/        # Reusable UI components
│   ├── models/            # Data models and structures
│   └── utils/             # Utility functions
├── tests/                 # Unit tests for quality assurance
├── app.py                 # Main application entry point
├── Dockerfile             # Docker image configuration
└── docker-compose.yml     # Docker Compose setup
```

## Installation

### Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Docker**: Required for containerized deployment (optional)

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/chintanboghara/Stock-Data-Visualization.git
   cd Stock-Data-Visualization
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

3. Launch the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

### Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the container:
   ```bash
   docker-compose up -d
   ```

3. Access the application at `http://localhost:8501`

4. Stop the container:
   ```bash
   docker-compose down
   docker-compose down --rmi all
   ```

**Note**: Streamlit runs on port 8501 by default, not 5000 as previously stated. Ensure your firewall allows this port.

## Usage

### Single Stock Analysis

- Input a stock symbol (e.g., AAPL, MSFT, GOOGL) in the sidebar
- Choose a historical time period
- Explore the stock price chart, key metrics, and company details

### Stock Comparison

- Select "Stock Comparison" mode from the sidebar
- Enter up to 5 stock symbols
- Review a percentage change comparison chart and performance metrics

## Data Sources

All data is sourced in real-time from Yahoo Finance via the [yfinance](https://github.com/ranaroussi/yfinance) library. No financial data is stored locally, except for temporary caching to enhance performance.

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - For seamless access to Yahoo Finance data
- [Streamlit](https://streamlit.io/) - For simplifying web app development in Python
- [Plotly](https://plotly.com/) - For robust and interactive charting capabilities
