import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def main():
    st.title("Mini Strategy Analysis Project")
    st.write("""
        **Strategy**:  
        1. If a day’s volume > X% * average volume (last 20 days), and  
        2. The stock is up >= Y% from the previous day’s close,  
        then we “buy” at close on that day and hold for Z days to measure returns.
    """)

    # ----- User Inputs -----
    ticker_input = st.text_input("Ticker (e.g., AAPL, GOOGL)", value="AAPL")
    start_date = st.date_input("Start Date", value=datetime(2020,1,1))
    end_date = st.date_input("End Date", value=datetime.today())
    volume_threshold = st.number_input("Volume Breakout Threshold (in %)", value=200, min_value=1)
    change_threshold = st.number_input("Daily Price Change Threshold (in %)", value=2, min_value=0)
    holding_period = st.number_input("Holding Period (in days)", value=10, min_value=1)

    # Convert numeric thresholds to decimal
    volume_multiplier = volume_threshold / 100.0  # e.g. 200 -> 2.0
    price_change_multiplier = change_threshold / 100.0  # e.g. 2 -> 0.02

    if st.button("Generate Report"):
        if not ticker_input:
            st.error("Please enter a valid ticker.")
            return
        
        # 1) Get data
        try:
            df = yf.download(ticker_input, start=start_date, end=end_date, progress=False)
        except Exception as e:
            st.error(f"Error fetching data for {ticker_input}: {e}")
            return
        
        print(df.columns)
        # Remove the second level
        df.columns = df.columns.droplevel('Ticker')  # or droplevel(1) if you prefer        
        print(df.head())


        if df.empty:
            st.error("No data returned for the given date range. Please adjust and try again.")
            return
        
        # We only need columns: ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # 2) Create columns for the 20-day average volume and daily % change
        df['20d_avg_volume'] = df['Volume'].rolling(window=20).mean()
        df['PrevClose'] = df['Close'].shift(1)
        df['DailyPctChange'] = (df['Close'] - df['PrevClose']) / df['PrevClose'] * 100
        
        # 3) Identify breakout days
        # Conditions:
        #   Condition A: Volume > volume_multiplier * 20d_avg_volume
        #   Condition B: DailyPctChange >= change_threshold
        df['Breakout'] = (
            (df['Volume'] > volume_multiplier * df['20d_avg_volume']) & 
            (df['DailyPctChange'] >= change_threshold)
        )
        
        # 4) For each breakout day, buy at close, hold for Z days, compute return
        breakout_days = []
        for i in range(len(df)):
            if df['Breakout'].iloc[i]:
                buy_date = df.index[i]
                buy_price = df['Close'].iloc[i]
                
                # Sell date will be i+holding_period
                sell_index = i + holding_period
                if sell_index < len(df):
                    sell_date = df.index[sell_index]
                    sell_price = df['Close'].iloc[sell_index]
                    pct_return = (sell_price - buy_price) / buy_price * 100
                else:
                    # Not enough days to hold for the entire period
                    sell_date = None
                    sell_price = None
                    pct_return = None
                
                breakout_days.append({
                    'Buy Date': buy_date,
                    'Buy Price': buy_price,
                    'Sell Date': sell_date,
                    'Sell Price': sell_price,
                    'Return (%)': pct_return
                })
        
        # Convert to DataFrame
        results_df = pd.DataFrame(breakout_days)
        
        if not results_df.empty and results_df['Return (%)'].notna().any():
            avg_return = results_df['Return (%)'].dropna().mean()
            st.write(f"**Number of breakouts**: {len(results_df)}")
            st.write(f"**Average return**: {avg_return:.2f}%")
        else:
            st.write("No breakout signals found or insufficient data to compute returns.")
        
        st.dataframe(results_df)

        # 5) Provide download link for CSV
        csv_data = results_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"{ticker_input}_breakout_report.csv",
            mime="text/csv"
        )

if __name__ == '__main__':
    main()
