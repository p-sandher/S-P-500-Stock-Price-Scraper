'''
main.py
  Author(s): Puneet Sandher
  Project: COVID-19 SK Data Visualizer 
  Date of Last Update: May 20, 2021
  Functional Summary
      This program uses streamlit to display the following about the current       
      S&P 500: 
      1. Filter companies by one or more industries
      2. Display plots of closing prices of stocks
      3. Download a CSV file of company lists
      
     Commandline Parameters: 0
  How to Run:
  streamlit run S&P 500 Stock Prices.py
        
'''

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

@st.cache
def collectInfo():   
  url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  htmlText=pd.read_html(url, header=0)
  data=htmlText[0]
  return data

# downloadFile converts the data to a CSV file 
def downloadFile(data):
  csv=data.to_csv(index=False)
  convert=base64.b64encode(csv.encode()).decode()
  file=f'<a href="data:file/csv;base64,{convert}" download="S&P500.csv">Download CSV File</a>'
  return file


data=collectInfo()
giwcsSector = data.groupby('GICS Sector')

st.title('S&P 500')
st.sidebar.header('Filters')

sectorTypes = sorted (data['GICS Sector'].unique())
selectedSector=st.sidebar.multiselect('Sector', sectorTypes, sectorTypes)

dataSelectedSector = data[(data['GICS Sector'].isin(selectedSector))]
st.dataframe(dataSelectedSector)
st.markdown(downloadFile(dataSelectedSector), unsafe_allow_html=True)

# Displaying plots

companyData = yf.download(
  tickers=list(dataSelectedSector[:10].Symbol),
  period="ytd",
  interval ="1d",
  proxy=None,
  threads=True,
  auto_adjust=True, 
  group_by='ticker', 
  prepost=True
)

companyDisplayCount = st.sidebar.slider('Number of Companies to Display', 1, 10)

def plotCompany(symbol):
  plotInfo = pd.DataFrame(companyData[symbol].Close)
  plotInfo['Date'] = plotInfo.index
  fig = plt.fill_between(plotInfo.Date,plotInfo.Close)
  fig = plt.plot(plotInfo.Date,plotInfo.Close)
  fig = plt.xlabel('Date')
  fig = plt.ylabel('Closing Price')
  plt.savefig(fig)
  return st.pyplot(fig)

if st.button('Display Plots'):
  st.header('Stock Closing Price')
  for j in list(dataSelectedSector.Symbol)[:companyDisplayCount]:
    fig = plotCompany(j)
