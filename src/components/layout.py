"""
Layout components for the Streamlit app.
"""
import logging
import streamlit as st
import pandas as pd
from typing import Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def set_page_config() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Stock Data Visualization",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def set_page_style() -> None:
    """Set custom CSS styles for the page."""
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .metric-container {
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin-bottom: 1rem;
        }
        .subheader {
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #0e1117;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 0.5rem;
        }
        .stDataFrame {
            margin-top: 1rem;
        }
        footer {
            opacity: 0.7;
            font-size: 0.8rem;
        }
        .stButton>button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header() -> None:
    """Render the application header and description."""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://img.icons8.com/color/150/000000/stocks.png", width=120)
    
    with col2:
        st.title("📈 Stock Data Visualization")
        st.markdown(
            """
            Explore stock data from Yahoo Finance with interactive charts and metrics.
            Enter a stock symbol like AAPL, MSFT, or GOOGL and select a time period to visualize.
            """
        )

def render_input_section() -> Tuple[list, str, bool]:
    """
    Render the input section with stock symbol and period selection.
    
    Returns:
        Tuple[list, str, bool]: Selected stock symbols, period, and comparison mode flag
    """
    st.sidebar.header("Input Parameters")
    
    # Mode selection - Single stock or Comparison
    mode = st.sidebar.radio(
        "Mode",
        ["Single Stock Analysis", "Stock Comparison"],
        help="Select between analyzing a single stock or comparing multiple stocks"
    )
    
    # Initialize comparison mode flag
    comparison_mode = mode == "Stock Comparison"
    
    # Stock symbol input based on mode
    if comparison_mode:
        st.sidebar.subheader("Stock Symbols")
        # Default symbols for comparison
        default_symbols = ["AAPL", "MSFT", "GOOGL"]
        
        # Create inputs for multiple stocks (up to 5)
        stock_symbols = []
        
        # First symbol is required
        symbol1 = st.sidebar.text_input(
            "Primary Stock Symbol",
            value=default_symbols[0],
            help="Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
        stock_symbols.append(symbol1)
        
        # Add options for comparison stocks
        symbol2 = st.sidebar.text_input(
            "Comparison Stock 1",
            value=default_symbols[1],
            help="Enter a stock to compare (leave empty to ignore)"
        ).upper()
        if symbol2:
            stock_symbols.append(symbol2)
            
        symbol3 = st.sidebar.text_input(
            "Comparison Stock 2",
            value=default_symbols[2],
            help="Enter a stock to compare (leave empty to ignore)"
        ).upper()
        if symbol3:
            stock_symbols.append(symbol3)
            
        symbol4 = st.sidebar.text_input(
            "Comparison Stock 3 (Optional)",
            value="",
            help="Enter a stock to compare (leave empty to ignore)"
        ).upper()
        if symbol4:
            stock_symbols.append(symbol4)
            
        symbol5 = st.sidebar.text_input(
            "Comparison Stock 4 (Optional)",
            value="",
            help="Enter a stock to compare (leave empty to ignore)"
        ).upper()
        if symbol5:
            stock_symbols.append(symbol5)
            
        # Remove duplicates while preserving order
        stock_symbols = list(dict.fromkeys(stock_symbols))
    else:
        # Single stock mode
        stock_symbol = st.sidebar.text_input(
            "Stock Symbol",
            value="AAPL",
            help="Enter a valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
        stock_symbols = [stock_symbol]
    
    # Time period selection
    periods = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y",
        "Max": "max"
    }
    
    selected_period_name = st.sidebar.selectbox(
        "Time Period",
        list(periods.keys()),
        index=3,  # Default to 1 Year
        help="Select the time period for historical data"
    )
    
    period = periods[selected_period_name]
    
    # Add a fetch button
    if st.sidebar.button("Fetch Stock Data"):
        st.session_state.trigger_fetch = True
    
    # Add cache clear option in an expander
    with st.sidebar.expander("Advanced Options"):
        if st.button("Clear Cache"):
            from src.cache.cache_manager import clear_cache
            clear_cache()
            st.success("Cache cleared successfully!")
    
    # Add info about the app in a sidebar expander
    with st.sidebar.expander("About"):
        st.markdown("""
        This application fetches real-time stock data from Yahoo Finance.
        
        **Features:**
        - Interactive stock price charts
        - Stock comparison capabilities
        - Key financial metrics and ratios
        - Company information
        - Data export to CSV
        
        **Data Source:** [Yahoo Finance](https://finance.yahoo.com/)
        """)
    
    return stock_symbols, period, comparison_mode

def render_company_header(company_name: str, stock_symbol: str) -> None:
    """
    Render the company header.
    
    Args:
        company_name (str): Name of the company
        stock_symbol (str): Stock symbol
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### {company_name} ({stock_symbol})")
    
    with col3:
        st.markdown(f"<p style='text-align: right;'>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
    
    st.markdown("---")

def render_footer() -> None:
    """Render the page footer with data source information."""
    st.markdown("---")
    st.markdown(
        """
        <footer>
            Data Source: Yahoo Finance | Updated: %s | 
            Disclaimer: This app is for informational purposes only. Not financial advice.
        </footer>
        """ % datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        unsafe_allow_html=True
    )

def render_error(message: str, suggestion: Optional[str] = None) -> None:
    """
    Render an error message.
    
    Args:
        message (str): The error message to display
        suggestion (str, optional): Suggestion for resolving the error
    """
    st.error(message)
    if suggestion:
        st.info(suggestion)
    
    # Log the error
    logger.error(f"Application error: {message}")

def render_info(message: str) -> None:
    """
    Render an information message.
    
    Args:
        message (str): The information message to display
    """
    st.info(message)

def render_warning(message: str) -> None:
    """
    Render a warning message.
    
    Args:
        message (str): The warning message to display
    """
    st.warning(message)