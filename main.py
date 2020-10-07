import pandas_datareader as pdr
from datetime import datetime
import calendar

StartDates = [4, 5, 6, 7, 8]
#Interval = "m"
#Ticker = "VGT"
Amount = 50
while 1:
  Ticker = input("Enter Ticker: ")
  Interval = input("Enter Interval here on of (d,w,m): ")
  #Amount = input("Enter Amount: ")

  for StartDay in StartDates:
    StartDate = datetime(2010, 1, StartDay).date()
    EndDate = datetime.now().date()
    data = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval=Interval)

    data['Amount Invested'] = Amount
    data['Share Bought'] = Amount / data['Close']
    del data['Open']
    del data['Low']
    del data['High']
    del data['Adj Close']
    del data['Volume']

    TotalAmountInvested = data['Amount Invested'].sum()
    TotalShareBought = data['Share Bought'].sum()
    AvgPrice = TotalAmountInvested / TotalShareBought
    LastPrice = data.tail(1).get('Close').values[0]
    #print(f"Ticker: {Ticker}  interval:  {Interval}" )
    print(f"StartDate = {StartDate} {calendar.day_name[StartDate.weekday()]}")
    print(f"EndDate = {EndDate} {calendar.day_name[EndDate.weekday()]}")
    #print(f"Total Amount Invested = {TotalAmountInvested}")
    #print(f"Total Shares Own = {TotalShareBought}")
    #print(f"Avg Price paid per share = {AvgPrice}")
    #print(f"Total Value = {TotalShareBought*LastPrice}")
    #print(f"Total Return $ = {(TotalShareBought*LastPrice)-TotalAmountInvested}")
    TotalReturn = ((TotalShareBought * LastPrice) -
                TotalAmountInvested) / TotalAmountInvested * 100
    print("Total Return % = {:.2f}".format(TotalReturn))
    print()
