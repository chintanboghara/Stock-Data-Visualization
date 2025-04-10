"""
API integration for stock data retrieval and processing.
"""
import logging
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from src.utils.stock_data import get_stock_data, get_company_info, get_financials, StockDataError
from src.cache.cache_manager import cache_result

logger = logging.getLogger(__name__)

@cache_result(expires=3600)  # Cache for 1 hour
def fetch_stock_data(stock_symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch and cache stock historical data.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        period (str): Time period for data
        
    Returns:
        pd.DataFrame: Historical stock data
        
    Raises:
        StockDataError: If data cannot be fetched
    """
    logger.info(f"API request for stock data: {stock_symbol}, period: {period}")
    return get_stock_data(stock_symbol, period)

@cache_result(expires=7200)  # Cache for 2 hours
def fetch_company_info(stock_symbol: str) -> Dict[str, Any]:
    """
    Fetch and cache company information.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        Dict[str, Any]: Company information
        
    Raises:
        StockDataError: If data cannot be fetched
    """
    logger.info(f"API request for company info: {stock_symbol}")
    return get_company_info(stock_symbol)

@cache_result(expires=86400)  # Cache for 24 hours
def fetch_financials(stock_symbol: str) -> Dict[str, Any]:
    """
    Fetch and cache financial data.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        
    Returns:
        Dict[str, Any]: Financial data
        
    Raises:
        StockDataError: If data cannot be fetched
    """
    logger.info(f"API request for financial data: {stock_symbol}")
    return get_financials(stock_symbol)

def validate_stock_symbol(symbol: str) -> Tuple[bool, str]:
    """
    Validate stock symbol format.
    
    Args:
        symbol (str): Stock symbol to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not symbol:
        return False, "Stock symbol cannot be empty"
    
    # Strip any whitespace
    symbol = symbol.strip()
    
    # Basic validation: alphanumeric and periods only
    if not all(c.isalnum() or c == '.' for c in symbol):
        return False, "Stock symbol must contain only letters, numbers, and dots"
    
    # Length validation
    if len(symbol) > 10:
        return False, "Stock symbol too long (max 10 characters)"
        
    # Check for common invalid inputs
    if symbol.lower() in ['none', 'symbol', 'stock', 'ticker']:
        return False, "Please enter a valid stock symbol"
        
    return True, ""

def get_stock_summary(stock_symbol: str, period: str = "1y") -> Dict[str, Any]:
    """
    Get a complete summary of stock data including historical prices,
    company info, and financial data.
    
    Args:
        stock_symbol (str): Stock ticker symbol
        period (str): Time period for historical data
        
    Returns:
        Dict[str, Any]: Complete stock summary
        
    Raises:
        StockDataError: If data cannot be fetched
    """
    logger.info(f"Generating complete stock summary for {stock_symbol}")
    
    # Validate the stock symbol
    is_valid, error_message = validate_stock_symbol(stock_symbol)
    if not is_valid:
        raise StockDataError(error_message)
    
    # Fetch all data
    stock_data = fetch_stock_data(stock_symbol, period)
    company_info = fetch_company_info(stock_symbol)
    financial_data = fetch_financials(stock_symbol)
    
    # Compile summary
    summary = {
        "stock_symbol": stock_symbol,
        "company_name": company_info.get("longName", "Unknown Company"),
        "period": period,
        "stock_data": stock_data,
        "company_info": company_info,
        "financial_data": financial_data,
        "last_updated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    logger.info(f"Successfully generated stock summary for {stock_symbol}")
    return summary