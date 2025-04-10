"""
Stock Data Visualization Application

This application fetches and visualizes stock data from Yahoo Finance.
It provides interactive charts, key financial metrics, and company information.
"""
import logging
import traceback
from typing import Dict, List, Tuple, Any
import streamlit as st
import pandas as pd
from src.utils.config import setup_logging, get_config
from src.api.stock_api import get_stock_summary, StockDataError, validate_stock_symbol
from src.components.layout import (
    set_page_config, 
    set_page_style, 
    render_header, 
    render_input_section,
    render_company_header, 
    render_footer, 
    render_error,
    render_info
)
from src.components.metrics import (
    render_key_metrics,
    render_stock_chart,
    render_stock_comparison,
    render_financial_data_tables,
    render_recent_data_table,
    render_company_information
)

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize configuration
config = get_config()

# Initialize session state for data persistence
if 'stock_summaries' not in st.session_state:
    st.session_state.stock_summaries = {}
if 'trigger_fetch' not in st.session_state:
    st.session_state.trigger_fetch = False
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

def fetch_stock_data(symbol: str, period: str) -> Dict[str, Any]:
    """
    Fetch stock data for a given symbol.
    
    Args:
        symbol (str): Stock symbol to fetch
        period (str): Time period for the data
        
    Returns:
        Dict[str, Any]: Stock summary data
        
    Raises:
        StockDataError: If data cannot be fetched
    """
    logger.info(f"Fetching stock summary for {symbol} with period {period}")
    
    # Validate the stock symbol
    is_valid, error_message = validate_stock_symbol(symbol)
    if not is_valid:
        raise StockDataError(error_message)
    
    # Get and return the stock summary
    return get_stock_summary(symbol, period)

def main():
    """Main application function."""
    try:
        # Set page configuration
        set_page_config()
        set_page_style()
        
        # Render header
        render_header()
        
        # Get user inputs
        stock_symbols, period, comparison_mode = render_input_section()
        
        # Update comparison mode in session state
        st.session_state.comparison_mode = comparison_mode
        
        # Check if we should fetch new data
        should_fetch = st.session_state.trigger_fetch
        
        # Reset trigger
        if st.session_state.trigger_fetch:
            st.session_state.trigger_fetch = False
        
        # Handle invalid symbols
        invalid_symbols = []
        for symbol in stock_symbols:
            is_valid, error_message = validate_stock_symbol(symbol)
            if not is_valid:
                invalid_symbols.append((symbol, error_message))
        
        if invalid_symbols:
            for symbol, error in invalid_symbols:
                render_error(
                    f"Invalid symbol '{symbol}': {error}",
                    "Please enter valid stock symbols like AAPL, MSFT, or GOOGL."
                )
            return
        
        # Dictionary to store all stock data
        stock_data_dict = {}
        company_info_dict = {}
        
        # Fetch data for each stock
        for symbol in stock_symbols:
            # Check if we have data for this stock or need to fetch new data
            current_period = None
            if symbol in st.session_state.stock_summaries:
                current_period = st.session_state.stock_summaries[symbol].get("period")
            
            # Fetch data if needed
            if (symbol not in st.session_state.stock_summaries or
                current_period != period or
                should_fetch):
                
                try:
                    with st.spinner(f"Fetching data for {symbol}..."):
                        # Get stock data
                        stock_summary = fetch_stock_data(symbol, period)
                        
                        # Update session state
                        st.session_state.stock_summaries[symbol] = stock_summary
                        
                        # Log success
                        logger.info(f"Successfully fetched data for {symbol}")
                        
                except StockDataError as e:
                    render_error(
                        f"Error fetching data for {symbol}: {str(e)}",
                        "Please check the stock symbol and try again."
                    )
                    continue
            
            # Store data for comparison if we have it
            if symbol in st.session_state.stock_summaries:
                summary = st.session_state.stock_summaries[symbol]
                stock_data_dict[symbol] = summary["stock_data"]
                company_info_dict[symbol] = summary["company_info"]
        
        # Check if we have any data to display
        if not stock_data_dict:
            render_error(
                "No valid stock data available.",
                "Please enter valid stock symbols and try again."
            )
            return
        
        # COMPARISON MODE
        if comparison_mode:
            st.markdown("# Stock Comparison")
            
            # Show the comparison chart
            render_stock_comparison(stock_data_dict)
            
            # Optionally show company details in expanders
            st.markdown("## Company Details")
            
            for symbol in stock_symbols:
                if symbol in company_info_dict:
                    with st.expander(f"{company_info_dict[symbol].get('longName', symbol)} ({symbol})"):
                        # Display key metrics in a compact format
                        st.markdown("### Key Metrics")
                        metrics_to_show = {
                            "Current Price": f"${company_info_dict[symbol].get('currentPrice', 'N/A')}",
                            "Market Cap": f"${company_info_dict[symbol].get('marketCap', 0) / 1e9:.2f}B" if isinstance(company_info_dict[symbol].get('marketCap'), (int, float)) else "N/A",
                            "P/E Ratio": f"{company_info_dict[symbol].get('trailingPE', 'N/A')}",
                            "Sector": company_info_dict[symbol].get('sector', 'N/A'),
                            "Industry": company_info_dict[symbol].get('industry', 'N/A')
                        }
                        
                        # Display in two columns
                        cols = st.columns(2)
                        for i, (key, value) in enumerate(metrics_to_show.items()):
                            with cols[i % 2]:
                                st.markdown(f"**{key}:** {value}")
                        
                        # Display business summary if available
                        if company_info_dict[symbol].get('longBusinessSummary'):
                            st.markdown("### Business Summary")
                            st.write(company_info_dict[symbol].get('longBusinessSummary'))
        
        # SINGLE STOCK MODE
        else:
            # Get the (only) stock symbol and its data
            symbol = stock_symbols[0]
            stock_summary = st.session_state.stock_summaries[symbol]
            
            # Display company header
            render_company_header(
                stock_summary["company_name"], 
                stock_summary["stock_symbol"]
            )
            
            # Display key metrics
            render_key_metrics(stock_summary["company_info"])
            
            # Display stock chart
            if "stock_data" in stock_summary and isinstance(stock_summary["stock_data"], pd.DataFrame):
                render_stock_chart(
                    stock_summary["stock_data"], 
                    stock_summary["stock_symbol"]
                )
            
            # Display financial data tables
            render_financial_data_tables(stock_summary["company_info"])
            
            # Display recent data table
            if "stock_data" in stock_summary and isinstance(stock_summary["stock_data"], pd.DataFrame):
                render_recent_data_table(
                    stock_summary["stock_data"], 
                    stock_summary["stock_symbol"]
                )
            
            # Display company information
            render_company_information(stock_summary["company_info"])
        
        # Render footer
        render_footer()
        
    except Exception as e:
        logger.error(f"Unhandled application error: {str(e)}")
        logger.error(traceback.format_exc())
        render_error(
            "An unexpected error occurred.",
            f"Error details: {str(e)}"
        )

if __name__ == "__main__":
    main()