import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import plotly.graph_objects as go


def calculate_volatility(dataframe, periods=30):

    price_history = dataframe["AVG_PRICE"]
    log_returns = np.log(price_history / price_history.shift(-1))
    std_dev_log_returns = np.std(log_returns.values[0:periods])
    volatility = std_dev_log_returns * np.sqrt(365)

    return volatility


# create a monte carlo simulation given the number of days, the price, and the volatility given in df

def monte_carlo_simulation(df, days_simulated, iterations=10, rolling_volatility_days=30,  use_rolling_volatility=False):
    df = df.copy()

    volatility = calculate_volatility(df, rolling_volatility_days)

    df['daily_returns'] = df['MEDIAN_PRICE'].pct_change()
    last_price = df['MEDIAN_PRICE']
    # make it only from the selected token
    last_price = last_price.iloc[0]

    rolling_volatility = df['RELATIVE_STDDEV'].rolling(
        rolling_volatility_days).mean()
    rolling_volatility = rolling_volatility.dropna()
    rolling_volatility = rolling_volatility.iloc[0]
    # st.write("rolling volatility: ", rolling_volatility)
    # make the user say how many days of rolling volatility they want
    # st.write(volatility)
    simulation_df = pd.DataFrame(index=range(
        0, days_simulated), columns=range(0, iterations))
    # name each collum day 1, day 2, etc
    # simm
    if use_rolling_volatility:
        st.write("most recent rolling volatility: ", rolling_volatility)
        for x in range(iterations-1):
            count = 0
            daily_vol = rolling_volatility
            price_series = []
            price = last_price * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            for y in range(days_simulated-1):
                if count == 251:
                    daily_vol = rolling_volatility
                    count = 0
                price = price_series[count] * \
                    (1 + np.random.normal(0, daily_vol))
                price_series.append(price)
                count += 1
            simulation_df[x] = price_series
    else:
        for x in range(iterations):
            count = 0
            daily_vol = volatility / 365
            price_series = []
            price_series.append(last_price)
            for y in range(days_simulated-1):
                if count == 251:
                    daily_vol = volatility
                    count = 0
                price = price_series[count] * (1 + np.random.normal(
                    0, daily_vol)*np.sqrt(days_simulated))
                price_series.append(price)
                count += 1
            simulation_df[x] = price_series


    return simulation_df, volatility  # return the simulation and the last price


def calculate_supply_total(markets_data):
    total = np.sum(
        markets_data['totalSupply'].astype(float) * markets_data['underlyingPriceUSD'].astype(
            float) * markets_data['exchangeRate'].astype(float))
    return total


def calculate_borrow_total(markets_data):
    total = np.sum(markets_data['totalBorrows'].astype(
        float) * markets_data['underlyingPriceUSD'].astype(float))
    return total
