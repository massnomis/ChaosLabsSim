from asyncore import write
from operator import le
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from helpers import calculate_borrow_total, calculate_supply_total, monte_carlo_simulation
# import gql
from gql import gql, Client
st.set_page_config(layout="wide")

st.title("Compound Solvency Analysis using Monte Carlo Simulations")
api = 'https://node-api.flipsidecrypto.com/api/v2/queries/be234be0-dc93-4067-8d02-03b7bf2f8210/data/latest'

response = requests.get(api)
data = response.json()
df = pd.DataFrame(data)
# st.write(df)

montecarlo_duration = st.slider('How many days of simmulations', 1, 250, 60)
iterations = 10


rolling_volatility_days = st.slider(
    'How many days do you want to lookback for historical volatility?', 15, 60, 30)

token = st.selectbox(
    'Select a token', df['UNDERLYING_SYMBOL'].unique(), index=8)


df = df[df['UNDERLYING_SYMBOL'] == token]

# Get all markets data from Compound

request_data_markets = """{
  markets( first: 30, orderBy: collateralFactor, orderDirection:desc) {
    underlyingName
    underlyingSymbol
    collateralFactor
    totalBorrows
    totalSupply
    exchangeRate
    underlyingPriceUSD
  }
}
"""

api_ping = 'https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2'
market_responses = requests.post(
    api_ping, json={'query': request_data_markets})
market_json = market_responses.json()
markets_data = pd.DataFrame(market_json['data']['markets'])

total_supply = calculate_supply_total(markets_data)
total_borrow = calculate_borrow_total(markets_data)


monte_carlo_df, volatility = monte_carlo_simulation(
    df, montecarlo_duration, iterations, rolling_volatility_days)


last_price = df['MEDIAN_PRICE']
last_price = last_price.iloc[0]

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)


kpi1.metric(
    label="Total Supply",
    value=f"{total_supply/1000000000 :.2f}B USD",
)

kpi2.metric(label="Total Borrow", value=f"{total_borrow/1000000 :.2f}M USD")

kpi3.metric(
    label="Historical Volatility",
    value=f"{volatility*100 :.2f}%",
)

kpi4.metric(
    label="Last Price",
    value=f"{last_price :.3f} USD",
)

kpi5.metric(
    label="Min Price",
    value=f"{monte_carlo_df.to_numpy().min() :.3f} USD",
)

kpi6.metric(
    label="Max Price",
    value=f"{monte_carlo_df.to_numpy().max() :.3f} USD",
)

st.write("Compound Markets Data")
markets_data['VAR'] = markets_data['underlyingPriceUSD'].astype(float)*markets_data['collateralFactor'].astype(
    float)*markets_data['totalSupply'].astype(float)*markets_data['exchangeRate'].astype(float)

st.write(markets_data)


st.plotly_chart(px.bar(markets_data, x='underlyingSymbol',
                y='VAR', title='Liabilities of the Protocol'), use_container_width=True)


change1 = markets_data['VAR']/markets_data['underlyingPriceUSD'].astype(float)
change2 = change1.T

if (token == 'WETH'):
    token = 'ETH'

index_to_choose = markets_data.index[markets_data['underlyingSymbol'] == token].tolist()[
    0]

change3 = change2.iloc[index_to_choose]

st.title('Price change and Insolvency risk')


# for each collumn in monte_carlo_df, divide the new price by the underlyingPriceUSD and multiply by VAR
for collumn in monte_carlo_df:
    monte_carlo_df['sim1'] = monte_carlo_df[1]
    monte_carlo_df['sim2'] = monte_carlo_df[2]
    monte_carlo_df['sim3'] = monte_carlo_df[3]
    monte_carlo_df['sim4'] = monte_carlo_df[4]
    monte_carlo_df['sim5'] = monte_carlo_df[5]
    monte_carlo_df['sim6'] = monte_carlo_df[6]
    monte_carlo_df['sim7'] = monte_carlo_df[7]
    monte_carlo_df['sim8'] = monte_carlo_df[8]
    monte_carlo_df['sim9'] = monte_carlo_df[9]
    monte_carlo_df['newVAR1'] = (monte_carlo_df[1] * change3)
    monte_carlo_df['newVAR2'] = (monte_carlo_df[2] * change3)
    monte_carlo_df['newVAR3'] = (monte_carlo_df[3] * change3)
    monte_carlo_df['newVAR4'] = (monte_carlo_df[4] * change3)
    monte_carlo_df['newVAR5'] = (monte_carlo_df[5] * change3)
    monte_carlo_df['newVAR6'] = (monte_carlo_df[6] * change3)
    monte_carlo_df['newVAR7'] = (monte_carlo_df[7] * change3)
    monte_carlo_df['newVAR8'] = (monte_carlo_df[8] * change3)
    monte_carlo_df['newVAR9'] = (monte_carlo_df[9] * change3)
    monte_carlo_df['sim1NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim1NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim1Solvency'] = monte_carlo_df['sim1NewSupply'] / monte_carlo_df['sim1NewBorrow']
    monte_carlo_df['sim2NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim2NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim2Solvency'] = monte_carlo_df['sim2NewSupply'] / monte_carlo_df['sim2NewBorrow']
    monte_carlo_df['sim3NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim3NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim3Solvency'] = monte_carlo_df['sim3NewSupply'] / monte_carlo_df['sim3NewBorrow']
    monte_carlo_df['sim4NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim4NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim4Solvency'] = monte_carlo_df['sim4NewSupply'] / monte_carlo_df['sim4NewBorrow']
    monte_carlo_df['sim5NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim5NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim5Solvency'] = monte_carlo_df['sim5NewSupply'] / monte_carlo_df['sim5NewBorrow']
    monte_carlo_df['sim6NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim6NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim6Solvency'] = monte_carlo_df['sim6NewSupply'] / monte_carlo_df['sim6NewBorrow']
    monte_carlo_df['sim7NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim7NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim7Solvency'] = monte_carlo_df['sim7NewSupply'] / monte_carlo_df['sim7NewBorrow']
    monte_carlo_df['sim8NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim8NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim8Solvency'] = monte_carlo_df['sim8NewSupply'] / monte_carlo_df['sim8NewBorrow']
    monte_carlo_df['sim9NewSupply'] = calculate_supply_total(markets_data)
    monte_carlo_df['sim9NewBorrow'] = calculate_borrow_total(markets_data)
    monte_carlo_df['sim9Solvency'] = monte_carlo_df['sim9NewSupply'] / monte_carlo_df['sim9NewBorrow']

    # monte_carlo_df['newVAR10'] = (monte_carlo_df[10] * change3)

st.plotly_chart(px.line(monte_carlo_df, x=monte_carlo_df.index, y=[
                'newVAR1', 'newVAR2', 'newVAR3', 'newVAR4', 'newVAR5', 'newVAR6', 'newVAR7', 'newVAR8', 'newVAR9'], title="Asset Liabilities (protocol)"), use_container_width=True)
# st.write(monte_carlo_df.columns)
st.plotly_chart(px.line(monte_carlo_df, x=monte_carlo_df.index, y=[
                'sim1', 'sim2', 'sim3', 'sim4', 'sim5', 'sim6', 'sim7', 'sim8', 'sim9'], title="Monte Carlo Sim"), use_container_width=True)

st.title("Solvency")


new_supply_list1 = []
new_borrow_list1 = []
new_insolvency_list1 = []
for temp_price in monte_carlo_df['sim1']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list1.append(new_supply)
    new_borrow_list1.append(new_borrow)
    new_insolvency_list1.append(new_supply/new_borrow)

# st.plotly_chart(px.line(y=new_insolvency_list1, title="Supply / Borrow"),
#                 use_container_width=True)


new_supply_list2 = []
new_borrow_list2 = []
new_insolvency_list2 = []
for temp_price in monte_carlo_df['sim2']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list2.append(new_supply)
    new_borrow_list2.append(new_borrow)
    new_insolvency_list2.append(new_supply/new_borrow)

# st.plotly_chart(px.line(y=new_insolvency_list, title="Supply / Borrow"),
#                 use_container_width=True)

new_supply_list3 = []
new_borrow_list3 = []
new_insolvency_list3 = []
for temp_price in monte_carlo_df['sim3']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list3.append(new_supply)
    new_borrow_list3.append(new_borrow)
    new_insolvency_list3.append(new_supply/new_borrow)


new_supply_list4 = []
new_borrow_list4 = []
new_insolvency_list4 = []
for temp_price in monte_carlo_df['sim4']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list4.append(new_supply)
    new_borrow_list4.append(new_borrow)
    new_insolvency_list4.append(new_supply/new_borrow)

new_supply_list5 = []
new_borrow_list5 = []
new_insolvency_list5 = []
for temp_price in monte_carlo_df['sim5']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list5.append(new_supply)
    new_borrow_list5.append(new_borrow)
    new_insolvency_list5.append(new_supply/new_borrow)

new_supply_list6 = []
new_borrow_list6 = []
new_insolvency_list6 = []
for temp_price in monte_carlo_df['sim6']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list6.append(new_supply)
    new_borrow_list6.append(new_borrow)
    new_insolvency_list6.append(new_supply/new_borrow)

new_supply_list7 = []
new_borrow_list7 = []
new_insolvency_list7 = []
for temp_price in monte_carlo_df['sim7']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list7.append(new_supply)
    new_borrow_list7.append(new_borrow)
    new_insolvency_list7.append(new_supply/new_borrow)

new_supply_list8 = []
new_borrow_list8 = []
new_insolvency_list8 = []
for temp_price in monte_carlo_df['sim8']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list8.append(new_supply)
    new_borrow_list8.append(new_borrow)
    new_insolvency_list8.append(new_supply/new_borrow)

new_supply_list9 = []
new_borrow_list9 = []
new_insolvency_list9 = []
for temp_price in monte_carlo_df['sim9']:
    temp_markets_data = markets_data.copy()
    temp_markets_data["underlyingPriceUSD"][int(
        index_to_choose)] = temp_price

    new_supply = calculate_supply_total(temp_markets_data)
    new_borrow = calculate_borrow_total(temp_markets_data)
    new_supply_list9.append(new_supply)
    new_borrow_list9.append(new_borrow)
    new_insolvency_list9.append(new_supply/new_borrow)

# mega_insolvency_list = []
# for i in range(len(new_insolvency_list)):
mega_insolvency_list = pd.DataFrame()
mega_insolvency_list = pd.DataFrame(mega_insolvency_list)
# mega_insolvency_list.append(
#         (new_insolvency_list1 + new_insolvency_list2 + new_insolvency_list3 + new_insolvency_list4 + new_insolvency_list5 + new_insolvency_list6 + new_insolvency_list7 + new_insolvency_list8 + new_insolvency_list9))

# add all the lists together
mega_insolvency_list['sim1'] = new_insolvency_list1
mega_insolvency_list['sim2'] = new_insolvency_list2
mega_insolvency_list['sim3'] = new_insolvency_list3
mega_insolvency_list['sim4'] = new_insolvency_list4
mega_insolvency_list['sim5'] = new_insolvency_list5
mega_insolvency_list['sim6'] = new_insolvency_list6
mega_insolvency_list['sim7'] = new_insolvency_list7
mega_insolvency_list['sim8'] = new_insolvency_list8
mega_insolvency_list['sim9'] = new_insolvency_list9
# st.write(mega_insolvency_list)


st.plotly_chart(px.line(mega_insolvency_list, title="Solvency Ratio"), use_container_width=True)



# st.write(mega_insolvency_list)

# st.plotly_chart(px.line(x = new_insolvency_list9.index ,y=['new_insolvency_list1'], title="Supply / Borrow"),
#                 use_container_width=True)
# st.plotly_chart(px.line(y=new_insolvency_list2, title="Supply / Borrow"),
#                 use_container_width=True)
# st.plotly_chart(px.line(y=new_insolvency_list3, title="Supply / Borrow"),
#                 use_container_width=True)
# st.plotly_chart(px.line(y=new_insolvency_list4, title="Supply / Borrow"),
#                 use_container_width=True)
# st.plotly_chart(px.line(y=new_insolvency_list5, title="Supply / Borrow"),
#                 use_container_width=True)
# st.plotly_chart(px.line(y=new_insolvency_list6, title="Supply / Borrow"),
#                 use

# st.plotly_chart(px.line(y=new_insolvency_list, title="Supply / Borrow"),
#                 use_container_width=True)


# monte_carlo_df
# monte_carlo_df


# Var_check =
# from scipy.stats import norm
# st.write(monte_carlo_df)
st.write('VAR needs to be within a certain confidence range, such as 1.5, 1.75 and 2 standard deviations from the mean')

# user enters the starting price
# user enters the lowest price


starting_price = st.number_input(
    'Enter the starting price', 0.0, 100000.0, )
lowest_price = st.number_input('Enter the lowest price', 0.0, 100000.0, 1200.0)

VAR = starting_price - lowest_price
st.write('VAR is (per asset)', VAR)
st.write("multiply by the number of assets to get the total VAR for the asset")

# caluclate the t distribution


#  Calculate the Value at Risk of the protocol given N measurements of (4)#

request_data_accounts = """
{
  account(id: "0x8888882f8f843896699869179fb6e4f7e3b58888") {
    id
    tokens(first: 12) {
      id
      symbol
      cTokenBalance
      totalUnderlyingSupplied
      totalUnderlyingRedeemed
      totalUnderlyingBorrowed
      supplyBalanceUnderlying
      lifetimeSupplyInterestAccrued
      borrowBalanceUnderlying
      lifetimeBorrowInterestAccrued
    }
    health
    totalBorrowValueInEth
    totalCollateralValueInEth
  }
}
"""

st.write("to get the best and worst case scenarios, we need to get the data for individual account")

st.title("below is a list of the largest borrowers, and the top borrower's lending/borrowing info")
addy_list = 'https://node-api.flipsidecrypto.com/api/v2/queries/f7d6368b-635d-44a6-a6ca-ad08314ae661/data/latest'
addy_list = requests.get(addy_list)
addy_list = addy_list.json()
addy_list = pd.DataFrame(addy_list)
borrower_address = addy_list['BORROWER_ADDRESS']
st.write(borrower_address)

responsez = requests.post(api_ping, json={'query': request_data_accounts})
response_jsonz = responsez.json()
dataz = response_jsonz['data']
liq_info = dataz['account']['tokens']
liq_info = pd.DataFrame(liq_info)
liq_info = liq_info.drop(columns=['id'])
liq_info = liq_info.set_index('symbol')
liq_info['totalUnderlyingRedeemed'] = liq_info['totalUnderlyingRedeemed'].astype(
    float)
liq_info['totalUnderlyingSupplied'] = liq_info['totalUnderlyingSupplied'].astype(
    float)
liq_info['totalUnderlyingBorrowed'] = liq_info['totalUnderlyingBorrowed'].astype(
    float)

liq_info['current_lend'] = liq_info['totalUnderlyingSupplied'] - \
    liq_info['totalUnderlyingRedeemed']
liq_info = liq_info.drop(columns=['cTokenBalance', 'totalUnderlyingSupplied', 'totalUnderlyingRedeemed',
                         'totalUnderlyingBorrowed', 'lifetimeSupplyInterestAccrued', 'lifetimeBorrowInterestAccrued', 'current_lend'])

liq_info['LONG'] = liq_info['supplyBalanceUnderlying']
liq_info['SHORT'] = liq_info['borrowBalanceUnderlying']
st.write(liq_info)



st.write('''
Assumptions:
''')
st.code('''
No Correlations between assets''')
st.code('''
Historical Volatility is a good estimate of future volatility

''')
st.code('''
No Liquidations
''')





  
