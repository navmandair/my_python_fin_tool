#import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime
from datetime import date
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
  
  EndDate = input("Enter End Date (YYYY-mm-dd) default today: ")
  if EndDate == "":
    EndDate = datetime.now().date()
  else:
    EndDate = datetime.strptime(EndDate, '%Y-%m-%d')

  Duration = input("Duration Years(default inception): ")
  if Duration != "":
    StartDate = date(EndDate.year - int(Duration), EndDate.month, EndDate.day)
  else:
    StartDate = datetime(1900, 1, 1).date()

  CalBasedOn = input("Which data to use (Low-1, High-2, Adj Close-3) (default Close): ")
  if CalBasedOn == "1":
    CalBasedOn = 'Low'
  elif CalBasedOn == "2":
    CalBasedOn = 'High'
  elif CalBasedOn == "3":
    CalBasedOn = 'Adj Close'
  else:
    CalBasedOn = 'Close'
  
  for Ticker in Tickers:
    info(Ticker)
    if API == "yf":
      rawdata = yf.download(Ticker, start=StartDate, end=EndDate)
    #if API == "pdr":
    #  rawdata = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval="d")

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
      #print(f"Total Amount Invested = {TotalAmountInvested}")
      #print(f"Total Shares Own = {TotalShareBought}")
      #AvgPrice = TotalAmountInvested / TotalShareBought
      #print(f"Avg Price paid per share = {AvgPrice}")
      #print(f"Total Value = {TotalShareBought*LastPrice}")
      #print(f"Total Return $ = {(TotalShareBought*LastPrice)-TotalAmountInvested}")
      TotalReturn = ((TotalShareBought * LastPrice) -
                      TotalAmountInvested) / TotalAmountInvested * 100
      TotalYearsInvested = ((ActualEndDate-ActualStartDate).days/365) 
      print(f"{(TotalReturn/TotalYearsInvested):.2f}% p.a, {calendar.day_name[ActualEndDate.weekday()]} at {CalBasedOn} price [{ActualStartDate} - {ActualEndDate}]")
    print("-------------------------------------------------")
  



main()