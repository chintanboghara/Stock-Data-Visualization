"""
Components for displaying financial metrics and data visualizations.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, List
from src.utils.visualization import (
    create_stock_chart,
    create_comparison_chart,
    format_financial_metrics, 
    format_financial_ratios, 
    convert_df_to_csv
)

def render_key_metrics(company_info: Dict[str, Any]) -> None:
    """
    Render key company metrics in a three-column layout.
    
    Args:
        company_info (Dict[str, Any]): Company information dictionary
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Current Price", 
            f"${company_info.get('currentPrice', 'N/A'):,.2f}" if isinstance(company_info.get('currentPrice'), (int, float)) else "N/A",
            f"{company_info.get('regularMarketChangePercent', 0):.2f}%" if isinstance(company_info.get('regularMarketChangePercent'), (int, float)) else "N/A"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "Market Cap", 
            f"${company_info.get('marketCap', 0) / 1e9:.2f}B" if isinstance(company_info.get('marketCap'), (int, float)) else "N/A"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            "52 Week Range", 
            f"${company_info.get('fiftyTwoWeekLow', 0):.2f} - ${company_info.get('fiftyTwoWeekHigh', 0):.2f}" 
            if isinstance(company_info.get('fiftyTwoWeekLow'), (int, float)) and isinstance(company_info.get('fiftyTwoWeekHigh'), (int, float)) 
            else "N/A"
        )
        st.markdown('</div>', unsafe_allow_html=True)

def render_stock_chart(stock_data: pd.DataFrame, stock_symbol: str) -> None:
    """
    Render the stock price chart.
    
    Args:
        stock_data (pd.DataFrame): Historical stock data
        stock_symbol (str): Stock ticker symbol
    """
    st.markdown('<div class="subheader">Stock Price History</div>', unsafe_allow_html=True)
    fig = create_stock_chart(stock_data, stock_symbol)
    st.plotly_chart(fig, use_container_width=True)

def render_financial_data_tables(company_info: Dict[str, Any]) -> None:
    """
    Render financial metrics and ratios in tables.
    
    Args:
        company_info (Dict[str, Any]): Company information dictionary
    """
    st.markdown('<div class="subheader">Key Financial Metrics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(format_financial_metrics(company_info), use_container_width=True)
    with col2:
        st.dataframe(format_financial_ratios(company_info), use_container_width=True)

def render_recent_data_table(stock_data: pd.DataFrame, stock_symbol: str) -> None:
    """
    Render recent stock price data table with download button.
    
    Args:
        stock_data (pd.DataFrame): Historical stock data
        stock_symbol (str): Stock ticker symbol
    """
    st.markdown('<div class="subheader">Recent Stock Price Data</div>', unsafe_allow_html=True)
    
    # Create tabs for different data views
    tab1, tab2 = st.tabs(["Recent Data", "Full Data"])
    
    with tab1:
        # Show recent data with sorting
        recent_data = stock_data.tail(10).sort_index(ascending=False)
        st.dataframe(recent_data, use_container_width=True)
    
    with tab2:
        # Show full data with filtering options
        all_data = stock_data.sort_index(ascending=False)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            # Add date range filter
            min_date = all_data.index.min().date()
            max_date = all_data.index.max().date()
            start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
        
        # Filter data based on date range
        filtered_data = all_data[(all_data.index.date >= start_date) & (all_data.index.date <= end_date)]
        st.dataframe(filtered_data, use_container_width=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        csv = convert_df_to_csv(stock_data)
        st.download_button(
            label="Download All Stock Data as CSV",
            data=csv,
            file_name=f"{stock_symbol}_stock_data.csv",
            mime="text/csv",
        )
    
    with col2:
        csv_recent = convert_df_to_csv(recent_data)
        st.download_button(
            label="Download Recent Data as CSV",
            data=csv_recent,
            file_name=f"{stock_symbol}_recent_stock_data.csv",
            mime="text/csv",
        )

def render_stock_comparison(stock_data_dict: Dict[str, pd.DataFrame]) -> None:
    """
    Render a comparison chart of multiple stocks.
    
    Args:
        stock_data_dict (Dict[str, pd.DataFrame]): Dictionary mapping stock symbols to their data
    """
    st.markdown('<div class="subheader">Stock Price Comparison</div>', unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Price Change %", "Performance Stats"])
    
    with tab1:
        # Create normalized comparison chart
        fig = create_comparison_chart(stock_data_dict)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation
        st.info("This chart shows percentage change from the first date in the selected period. This allows for comparing stocks at different price points.")
        
    with tab2:
        # Calculate performance metrics for each stock
        performance_data = []
        for symbol, data in stock_data_dict.items():
            if not data.empty:
                # Calculate metrics
                first_price = data['Close'].iloc[0]
                last_price = data['Close'].iloc[-1]
                total_return = (last_price / first_price - 1) * 100
                
                # Calculate volatility (standard deviation of daily returns)
                daily_returns = data['Close'].pct_change().dropna()
                volatility = daily_returns.std() * 100
                
                # Calculate max drawdown
                cumulative_return = (1 + daily_returns).cumprod()
                max_return = cumulative_return.cummax()
                drawdown = (cumulative_return / max_return - 1) * 100
                max_drawdown = drawdown.min()
                
                # Add to performance data
                performance_data.append({
                    'Symbol': symbol,
                    'Starting Price': f"${first_price:.2f}",
                    'Current Price': f"${last_price:.2f}",
                    'Total Return': f"{total_return:.2f}%",
                    'Volatility': f"{volatility:.2f}%",
                    'Max Drawdown': f"{max_drawdown:.2f}%"
                })
        
        # Create DataFrame and display
        if performance_data:
            perf_df = pd.DataFrame(performance_data)
            st.dataframe(perf_df, use_container_width=True)
        else:
            st.warning("No data available for performance comparison.")
    
    # Allow downloading comparison data
    if stock_data_dict:
        st.markdown("### Download Comparison Data")
        
        # Create a combined dataframe with all stocks
        all_close_prices = pd.DataFrame()
        
        for symbol, data in stock_data_dict.items():
            if not data.empty:
                all_close_prices[symbol] = data['Close']
        
        # Create download button if we have data
        if not all_close_prices.empty:
            csv = convert_df_to_csv(all_close_prices)
            st.download_button(
                label="Download Comparison Data as CSV",
                data=csv,
                file_name="stock_comparison_data.csv",
                mime="text/csv",
            )

def render_company_information(company_info: Dict[str, Any]) -> None:
    """
    Render detailed company information.
    
    Args:
        company_info (Dict[str, Any]): Company information dictionary
    """
    # Show company information in an expander
    with st.expander("Company Information"):
        # Company description
        if company_info.get('longBusinessSummary'):
            st.markdown("### Business Summary")
            st.write(company_info.get('longBusinessSummary'))
        
        # Company details in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Company Details")
            details = {
                "Sector": company_info.get('sector', 'N/A'),
                "Industry": company_info.get('industry', 'N/A'),
                "Employees": f"{company_info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(company_info.get('fullTimeEmployees'), (int, float)) else 'N/A',
                "Country": company_info.get('country', 'N/A'),
                "Website": company_info.get('website', 'N/A')
            }
            
            for key, value in details.items():
                st.markdown(f"**{key}:** {value}")
        
        with col2:
            st.markdown("### Trading Information")
            trading_info = {
                "Exchange": company_info.get('exchange', 'N/A'),
                "Currency": company_info.get('currency', 'N/A'),
                "Market": company_info.get('market', 'N/A'),
                "Quote Type": company_info.get('quoteType', 'N/A'),
                "Shares Outstanding": f"{company_info.get('sharesOutstanding', 'N/A'):,}" if isinstance(company_info.get('sharesOutstanding'), (int, float)) else 'N/A'
            }
            
            for key, value in trading_info.items():
                st.markdown(f"**{key}:** {value}")