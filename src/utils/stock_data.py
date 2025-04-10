"""
Stock data utilities for fetching and processing financial data from Yahoo Finance.
"""
import logging
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)

class StockDataError(Exception):
    """Custom exception for stock data fetching errors."""
    pass

def get_stock_data(stock_symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        period (str): Time period for data (e.g., '1mo', '3mo', '1y', '5y', 'max')
        
    Returns:
        pandas.DataFrame: Historical stock data
        
    Raises:
        StockDataError: If data cannot be fetched or is invalid
    """
    try:
        # Log the API request
        logger.info(f"Fetching stock data for {stock_symbol} with period {period}")
        
        # Create a Ticker object
        ticker = yf.Ticker(stock_symbol)
        
        # Get historical data
        df = ticker.history(period=period)
        
        # Check if data is empty
        if df.empty:
            raise StockDataError(f"No data found for ticker {stock_symbol}")
        
        # Keep only relevant columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Round values for better display
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].round(2)
        
        logger.info(f"Successfully fetched {len(df)} data points for {stock_symbol}")
        return df
    
    except Exception as e:
        # Log the error
        logger.error(f"Error fetching stock data for {stock_symbol}: {str(e)}")
        raise StockDataError(f"Failed to fetch stock data: {str(e)}")

def get_company_info(stock_symbol: str) -> Dict[str, Any]:
    """
    Get company information and key statistics from Yahoo Finance.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        dict: Company information and key statistics
        
    Raises:
        StockDataError: If company information cannot be fetched
    """
    try:
        # Log the API request
        logger.info(f"Fetching company info for {stock_symbol}")
        
        # Create a Ticker object
        ticker = yf.Ticker(stock_symbol)
        
        # Get company info
        info = ticker.info
        
        # Check if info is empty
        if not info or len(info) < 5:  # Basic check for minimally valid data
            raise StockDataError(f"Insufficient company information for {stock_symbol}")
        
        logger.info(f"Successfully fetched company info for {stock_symbol}")
        return info
    
    except Exception as e:
        # Log the error
        logger.error(f"Error fetching company info for {stock_symbol}: {str(e)}")
        raise StockDataError(f"Failed to fetch company information: {str(e)}")

def get_financials(stock_symbol: str) -> Dict[str, Any]:
    """
    Get financial data for a stock.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        dict: Financial data including income statement, balance sheet, and cash flow
        
    Raises:
        StockDataError: If financial data cannot be fetched
    """
    try:
        # Log the API request
        logger.info(f"Fetching financial data for {stock_symbol}")
        
        # Create a Ticker object
        ticker = yf.Ticker(stock_symbol)
        
        # Get financial data
        financials = {
            "income_statement": ticker.income_stmt,
            "balance_sheet": ticker.balance_sheet,
            "cash_flow": ticker.cashflow
        }
        
        # Check if any financial data is available
        if all(v.empty for v in financials.values()):
            logger.warning(f"No financial data available for {stock_symbol}")
            return {}
        
        logger.info(f"Successfully fetched financial data for {stock_symbol}")
        return financials
    
    except Exception as e:
        # Log the error
        logger.error(f"Error fetching financial data for {stock_symbol}: {str(e)}")
        raise StockDataError(f"Failed to fetch financial data: {str(e)}")

def safe_format(value: Any, format_type: str = "default") -> str:
    """
    Safely format financial values with proper error handling.
    
    Args:
        value: The value to format
        format_type: Type of formatting to apply (default, currency, percentage, etc.)
        
    Returns:
        str: Formatted value as a string or 'N/A' if formatting fails
    """
    try:
        # Handle None or NaN
        if value is None or (isinstance(value, (int, float)) and np.isnan(value)):
            return "N/A"
        
        # Handle different format types
        if format_type == "currency":
            return f"${float(value):.2f}"
        
        elif format_type == "percentage":
            return f"{float(value) * 100:.2f}%"
        
        elif format_type == "large_currency":
            # Format in billions or millions
            value = float(value)
            if value >= 1e9:
                return f"${value / 1e9:.2f}B"
            elif value >= 1e6:
                return f"${value / 1e6:.2f}M"
            else:
                return f"${value:.2f}"
        
        # Default formatting
        return str(value)
    
    except (ValueError, TypeError):
        return "N/A"