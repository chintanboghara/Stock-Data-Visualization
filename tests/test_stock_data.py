"""
Unit tests for stock data utilities.
"""
import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.utils.stock_data import get_stock_data, get_company_info, get_financials, StockDataError, safe_format

class TestStockData(unittest.TestCase):
    """Test cases for stock data utilities."""
    
    @patch('yfinance.Ticker')
    def test_get_stock_data_success(self, mock_ticker):
        """Test successful retrieval of stock data."""
        # Create mock data
        mock_history = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0],
            'High': [155.0, 156.0, 157.0],
            'Low': [148.0, 149.0, 150.0],
            'Close': [153.0, 154.0, 155.0],
            'Volume': [1000000, 1100000, 1200000],
            'Dividends': [0, 0, 0],
            'Stock Splits': [0, 0, 0]
        })
        
        # Configure mock
        mock_instance = mock_ticker.return_value
        mock_instance.history.return_value = mock_history
        
        # Call function
        result = get_stock_data('AAPL', '1mo')
        
        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(list(result.columns), ['Open', 'High', 'Low', 'Close', 'Volume'])
        mock_instance.history.assert_called_once_with(period='1mo')
    
    @patch('yfinance.Ticker')
    def test_get_stock_data_empty(self, mock_ticker):
        """Test error handling for empty stock data."""
        # Configure mock to return empty DataFrame
        mock_instance = mock_ticker.return_value
        mock_instance.history.return_value = pd.DataFrame()
        
        # Assert that the function raises an exception
        with self.assertRaises(StockDataError):
            get_stock_data('INVALID', '1mo')
    
    @patch('yfinance.Ticker')
    def test_get_company_info_success(self, mock_ticker):
        """Test successful retrieval of company info."""
        # Create mock data
        mock_info = {
            'longName': 'Apple Inc.',
            'symbol': 'AAPL',
            'marketCap': 2500000000000,
            'currentPrice': 150.0
        }
        
        # Configure mock
        mock_instance = mock_ticker.return_value
        mock_instance.info = mock_info
        
        # Call function
        result = get_company_info('AAPL')
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertEqual(result['longName'], 'Apple Inc.')
        self.assertEqual(result['symbol'], 'AAPL')
    
    def test_safe_format_functions(self):
        """Test safe formatting of different types of values."""
        # Test currency formatting
        self.assertEqual(safe_format(150.5, "currency"), "$150.50")
        
        # Test percentage formatting
        self.assertEqual(safe_format(0.15, "percentage"), "15.00%")
        
        # Test large currency formatting
        self.assertEqual(safe_format(1500000000, "large_currency"), "$1.50B")
        self.assertEqual(safe_format(1500000, "large_currency"), "$1.50M")
        
        # Test handling of invalid values
        self.assertEqual(safe_format(None), "N/A")
        self.assertEqual(safe_format(np.nan), "N/A")
        self.assertEqual(safe_format("not a number"), "N/A")

if __name__ == '__main__':
    unittest.main()