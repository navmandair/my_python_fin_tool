import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime
import calendar


def main():
  while 1:
    try:
      TickersInput = input("Enter Ticker: ")
      Tickers = list(TickersInput.split(",")) 
      returns("yf", Tickers)
    except:
      print('Something went wrong ! try again')
    print()

def info(Ticker):
  infodata = yf.Ticker(Ticker).info
  print(f"Symbol: {infodata['symbol']} Name: {infodata['shortName']}")
  InstrumentType = infodata['quoteType']
  if InstrumentType == 'ETF':
    print(f"Category: {infodata['category']}")
    print(f"Beta 3 Yr: {infodata['beta3Year']}")
  else:
    print(f"Sector: {infodata['sector']}")
    print(f"Beta: {infodata['beta']}")


def returns(API, Tickers):  
  StartDates = [0, 1, 2, 3, 4]
  Amount = 50
  StartDate = input("Enter Start Date (YYYY-mm-dd) default inception: ")
  if StartDate == "":
    StartDate = datetime(1900, 1, 1).date()
  else:
    StartDate = datetime.strptime(StartDate, '%Y-%m-%d')

  CalBasedOn = input("Which data to use (Low, High, Open, Close, Adj Close) (default Close): ")
  if CalBasedOn == "":
    CalBasedOn = 'Close'
  
  for Ticker in Tickers:
    info(Ticker)
    EndDate = datetime.now().date()
    if API == "yf":
      rawdata = yf.download(Ticker, start=StartDate, end=EndDate)
    if API == "pdr":
      rawdata = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval="d")

    rawdata['DATE'] = rawdata.index.to_pydatetime()
    rawdata['WEEKDAY'] = rawdata['DATE'].dt.weekday
    rawdata['Amount Invested'] = Amount
    rawdata['Share Bought'] = Amount / rawdata[CalBasedOn]
    del rawdata['Volume']

    for Day in StartDates:
      data = rawdata.query(f'WEEKDAY == {Day}')
      TotalAmountInvested = data['Amount Invested'].sum()
      TotalShareBought = data['Share Bought'].sum()
      ActualStartDate = data.head(1).index.to_pydatetime()[0].date()
      ActualEndDate = data.tail(1).index.to_pydatetime()[0].date()
      LastPrice = data.tail(1).get(CalBasedOn).values[0]
      print(f"{ActualStartDate} {calendar.day_name[ActualStartDate.weekday()]} - {ActualEndDate} {calendar.day_name[ActualEndDate.weekday()]}")
      #print(f"Total Amount Invested = {TotalAmountInvested}")
      #print(f"Total Shares Own = {TotalShareBought}")
      #AvgPrice = TotalAmountInvested / TotalShareBought
      #print(f"Avg Price paid per share = {AvgPrice}")
      #print(f"Total Value = {TotalShareBought*LastPrice}")
      #print(f"Total Return $ = {(TotalShareBought*LastPrice)-TotalAmountInvested}")
      TotalReturn = ((TotalShareBought * LastPrice) -
                      TotalAmountInvested) / TotalAmountInvested * 100
      TotalYearsInvested = ((ActualEndDate-ActualStartDate).days/365) 
      print("Total Return = {:.2f}%, Total Avg Return is = {:.2f}% p.a over {:.2f} years".format(TotalReturn, TotalReturn/TotalYearsInvested, TotalYearsInvested))
    print("-------------------------------------------------")
  



main()