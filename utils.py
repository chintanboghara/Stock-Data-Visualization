import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import StringIO

def get_stock_data(stock_symbol, period="1y"):
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        period (str): Time period for data (e.g., '1mo', '3mo', '1y', '5y', 'max')
        
    Returns:
        pandas.DataFrame: Historical stock data
    """
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period=period)
    
    # Check if data is empty
    if data.empty:
        raise ValueError(f"No data found for {stock_symbol}")
    
    # Format the dataframe
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.index = pd.to_datetime(data.index)
    data = data.round(2)
    
    return data

def get_company_info(stock_symbol):
    """
    Get company information and key statistics from Yahoo Finance.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        dict: Company information and key statistics
    """
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    return info

def get_financials(stock_symbol):
    """
    Get financial data for a stock.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        dict: Financial data including income statement, balance sheet, and cash flow
    """
    stock = yf.Ticker(stock_symbol)
    
    # Get financial data
    financials = {
        "income_statement": stock.income_stmt,
        "balance_sheet": stock.balance_sheet,
        "cash_flow": stock.cashflow
    }
    
    return financials

def create_stock_chart(stock_data, stock_symbol):
    """
    Create an interactive stock price chart using Plotly.
    
    Args:
        stock_data (pandas.DataFrame): Historical stock data
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        plotly.graph_objects.Figure: Interactive stock chart
    """
    # Create subplot with 2 rows
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, 
                        row_heights=[0.7, 0.3])
    
    # Add candlestick chart for OHLC
    fig.add_trace(
        go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name="OHLC"
        ),
        row=1, col=1
    )
    
    # Add volume bar chart
    fig.add_trace(
        go.Bar(
            x=stock_data.index,
            y=stock_data['Volume'],
            name="Volume",
            marker=dict(color='rgba(0, 128, 255, 0.5)')
        ),
        row=2, col=1
    )
    
    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'].rolling(window=20).mean(),
            line=dict(color='rgba(255, 165, 0, 0.8)', width=2),
            name="20-day MA"
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'].rolling(window=50).mean(),
            line=dict(color='rgba(255, 0, 0, 0.8)', width=2),
            name="50-day MA"
        ),
        row=1, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"{stock_symbol} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def format_financial_metrics(info):
    """
    Format company financial metrics as a dataframe.
    
    Args:
        info (dict): Company information dictionary
        
    Returns:
        pandas.DataFrame: Formatted financial metrics
    """
    metrics = {
        'Metric': [
            'Previous Close',
            'Open',
            'Day Low/High',
            'Volume',
            'Avg. Volume',
            'Market Cap',
            'Beta',
            'P/E Ratio',
            'EPS (TTM)',
            'Forward P/E',
            'Dividend Rate',
            'Dividend Yield',
        ],
        'Value': [
            f"${info.get('previousClose', 'N/A')}" if isinstance(info.get('previousClose'), (int, float)) else 'N/A',
            f"${info.get('open', 'N/A')}" if isinstance(info.get('open'), (int, float)) else 'N/A',
            f"${info.get('dayLow', 'N/A')} - ${info.get('dayHigh', 'N/A')}" if isinstance(info.get('dayLow'), (int, float)) and isinstance(info.get('dayHigh'), (int, float)) else 'N/A',
            f"{info.get('volume', 'N/A'):,}" if isinstance(info.get('volume'), (int, float)) else 'N/A',
            f"{info.get('averageVolume', 'N/A'):,}" if isinstance(info.get('averageVolume'), (int, float)) else 'N/A',
            f"${info.get('marketCap', 'N/A') / 1e9:.2f}B" if isinstance(info.get('marketCap'), (int, float)) else 'N/A',
            f"{info.get('beta', 'N/A'):.2f}" if isinstance(info.get('beta'), (int, float)) else 'N/A',
            f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), (int, float)) else 'N/A',
            f"${info.get('trailingEps', 'N/A'):.2f}" if isinstance(info.get('trailingEps'), (int, float)) else 'N/A',
            f"{info.get('forwardPE', 'N/A'):.2f}" if isinstance(info.get('forwardPE'), (int, float)) else 'N/A',
            f"${info.get('dividendRate', 'N/A'):.2f}" if isinstance(info.get('dividendRate'), (int, float)) else 'N/A',
            f"{info.get('dividendYield', 'N/A') * 100:.2f}%" if isinstance(info.get('dividendYield'), (int, float)) else 'N/A',
        ]
    }
    
    return pd.DataFrame(metrics)

def format_financial_ratios(info):
    """
    Format company financial ratios as a dataframe.
    
    Args:
        info (dict): Company information dictionary
        
    Returns:
        pandas.DataFrame: Formatted financial ratios
    """
    ratios = {
        'Ratio': [
            'Return on Equity',
            'Return on Assets',
            'Profit Margin',
            'Operating Margin',
            'Quick Ratio',
            'Current Ratio',
            'Debt to Equity',
            'Price to Book',
            'Price to Sales',
            'Book Value',
            'Earnings Growth',
            'Revenue Growth',
        ],
        'Value': [
            f"{info.get('returnOnEquity', 'N/A') * 100:.2f}%" if isinstance(info.get('returnOnEquity'), (int, float)) else 'N/A',
            f"{info.get('returnOnAssets', 'N/A') * 100:.2f}%" if isinstance(info.get('returnOnAssets'), (int, float)) else 'N/A',
            f"{info.get('profitMargins', 'N/A') * 100:.2f}%" if isinstance(info.get('profitMargins'), (int, float)) else 'N/A',
            f"{info.get('operatingMargins', 'N/A') * 100:.2f}%" if isinstance(info.get('operatingMargins'), (int, float)) else 'N/A',
            f"{info.get('quickRatio', 'N/A'):.2f}" if isinstance(info.get('quickRatio'), (int, float)) else 'N/A',
            f"{info.get('currentRatio', 'N/A'):.2f}" if isinstance(info.get('currentRatio'), (int, float)) else 'N/A',
            f"{info.get('debtToEquity', 'N/A'):.2f}" if isinstance(info.get('debtToEquity'), (int, float)) else 'N/A',
            f"{info.get('priceToBook', 'N/A'):.2f}" if isinstance(info.get('priceToBook'), (int, float)) else 'N/A',
            f"{info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if isinstance(info.get('priceToSalesTrailing12Months'), (int, float)) else 'N/A',
            f"${info.get('bookValue', 'N/A'):.2f}" if isinstance(info.get('bookValue'), (int, float)) else 'N/A',
            f"{info.get('earningsGrowth', 'N/A') * 100:.2f}%" if isinstance(info.get('earningsGrowth'), (int, float)) else 'N/A',
            f"{info.get('revenueGrowth', 'N/A') * 100:.2f}%" if isinstance(info.get('revenueGrowth'), (int, float)) else 'N/A',
        ]
    }
    
    return pd.DataFrame(ratios)

def convert_df_to_csv(df):
    """
    Convert DataFrame to CSV for download.
    
    Args:
        df (pandas.DataFrame): DataFrame to convert
        
    Returns:
        str: CSV string
    """
    return df.to_csv().encode('utf-8')
