"""
Visualization utilities for creating charts and formatting data for display.
"""
import logging
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def create_stock_chart(stock_data: pd.DataFrame, stock_symbol: str) -> go.Figure:
    """
    Create an interactive stock price chart using Plotly.
    
    Args:
        stock_data (pandas.DataFrame): Historical stock data
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        plotly.graph_objects.Figure: Interactive stock chart
    """
    # Create a subplot with 2 rows for price and volume
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03, 
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{stock_symbol} Stock Price", "Volume")
    )
    
    # Add price data
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='rgb(38, 166, 154)'),
            hovertemplate='%{x}<br>$%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add volume bar chart
    fig.add_trace(
        go.Bar(
            x=stock_data.index,
            y=stock_data['Volume'],
            name='Volume',
            marker=dict(color='rgba(58, 71, 80, 0.6)'),
            hovertemplate='%{x}<br>%{y:,.0f} shares<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout for better visualization
    fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode='x unified',
        xaxis2_rangeslider_visible=False,
        template='plotly_white'
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig


def create_comparison_chart(stock_data_dict: Dict[str, pd.DataFrame], title: str = "Stock Price Comparison") -> go.Figure:
    """
    Create an interactive comparison chart for multiple stocks.
    
    Args:
        stock_data_dict (Dict[str, pd.DataFrame]): Dictionary mapping stock symbols to their data
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Interactive comparison chart
    """
    # Define a color palette for different stocks
    colors = [
        'rgb(38, 166, 154)',   # Teal
        'rgb(239, 85, 59)',    # Red
        'rgb(49, 130, 189)',   # Blue
        'rgb(204, 204, 0)',    # Yellow
        'rgb(153, 51, 255)',   # Purple
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add each stock's data
    for i, (symbol, data) in enumerate(stock_data_dict.items()):
        # Normalize data to show percentage change relative to first data point
        if not data.empty:
            first_close = data['Close'].iloc[0]
            normalized_data = (data['Close'] / first_close - 1) * 100
            
            # Add line for this stock
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=normalized_data,
                    mode='lines',
                    name=symbol,
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate='%{x}<br>' + symbol + ': %{y:.2f}%<extra></extra>'
                )
            )
    
    # Update layout
    fig.update_layout(
        title=title,
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        hovermode='x unified',
        template='plotly_white',
        yaxis=dict(
            title="Percentage Change (%)",
            tickformat=".2f"
        ),
        xaxis=dict(
            title="Date",
            rangeslider=dict(visible=False)
        )
    )
    
    return fig

def format_financial_metrics(info: Dict[str, Any]) -> pd.DataFrame:
    """
    Format company financial metrics as a dataframe.
    
    Args:
        info (dict): Company information dictionary
        
    Returns:
        pandas.DataFrame: Formatted financial metrics
    """
    # Extract relevant financial metrics
    metrics = {
        'EPS (TTM)': info.get('trailingEPS'),
        'P/E Ratio': info.get('trailingPE'),
        'Forward P/E': info.get('forwardPE'),
        'Market Cap': info.get('marketCap'),
        'Revenue (TTM)': info.get('totalRevenue'),
        'Revenue Per Share': info.get('revenuePerShare'),
        'Profit Margin': info.get('profitMargins'),
        'Operating Margin': info.get('operatingMargins'),
        'Return on Assets': info.get('returnOnAssets'),
        'Return on Equity': info.get('returnOnEquity'),
        'Free Cash Flow': info.get('freeCashflow')
    }
    
    # Format values for display
    formatted_metrics = {}
    for key, value in metrics.items():
        if key in ['Market Cap', 'Revenue (TTM)', 'Free Cash Flow']:
            # Format large currency values
            if value and isinstance(value, (int, float)):
                if value >= 1e9:
                    formatted_metrics[key] = f"${value / 1e9:.2f}B"
                elif value >= 1e6:
                    formatted_metrics[key] = f"${value / 1e6:.2f}M"
                else:
                    formatted_metrics[key] = f"${value:.2f}"
            else:
                formatted_metrics[key] = "N/A"
                
        elif key in ['Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity']:
            # Format percentages
            if value and isinstance(value, (int, float)):
                formatted_metrics[key] = f"{value * 100:.2f}%"
            else:
                formatted_metrics[key] = "N/A"
                
        else:
            # Default formatting
            if value and isinstance(value, (int, float)):
                formatted_metrics[key] = f"{value:.2f}"
            else:
                formatted_metrics[key] = "N/A"
    
    # Convert to DataFrame
    df = pd.DataFrame(
        {'Metric': list(formatted_metrics.keys()), 'Value': list(formatted_metrics.values())}
    )
    
    return df

def format_financial_ratios(info: Dict[str, Any]) -> pd.DataFrame:
    """
    Format company financial ratios as a dataframe.
    
    Args:
        info (dict): Company information dictionary
        
    Returns:
        pandas.DataFrame: Formatted financial ratios
    """
    # Extract relevant financial ratios
    ratios = {
        'Price to Book': info.get('priceToBook'),
        'Price to Sales': info.get('priceToSalesTrailing12Months'),
        'Beta': info.get('beta'),
        'Dividend Yield': info.get('dividendYield'),
        'Payout Ratio': info.get('payoutRatio'),
        'Earnings Growth': info.get('earningsGrowth'),
        'Revenue Growth': info.get('revenueGrowth'),
        'Debt to Equity': info.get('debtToEquity'),
        'Current Ratio': info.get('currentRatio'),
        'Quick Ratio': info.get('quickRatio'),
        'Dividend Rate': info.get('dividendRate')
    }
    
    # Format values for display
    formatted_ratios = {}
    for key, value in ratios.items():
        if key in ['Dividend Yield', 'Payout Ratio', 'Earnings Growth', 'Revenue Growth']:
            # Format percentages
            if value and isinstance(value, (int, float)):
                formatted_ratios[key] = f"{value * 100:.2f}%"
            else:
                formatted_ratios[key] = "N/A"
                
        else:
            # Default formatting
            if value and isinstance(value, (int, float)):
                formatted_ratios[key] = f"{value:.2f}"
            else:
                formatted_ratios[key] = "N/A"
    
    # Convert to DataFrame
    df = pd.DataFrame(
        {'Ratio': list(formatted_ratios.keys()), 'Value': list(formatted_ratios.values())}
    )
    
    return df

def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to CSV for download.
    
    Args:
        df (pandas.DataFrame): DataFrame to convert
        
    Returns:
        bytes: CSV data as bytes
    """
    try:
        return df.to_csv(index=True).encode('utf-8')
    except Exception as e:
        logger.error(f"Error converting DataFrame to CSV: {str(e)}")
        # Return empty CSV in case of error
        return "Error converting data".encode('utf-8')