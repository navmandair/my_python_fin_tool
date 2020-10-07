import pandas_datareader as pdr
from datetime import datetime
import calendar

StartDates = [4, 5, 6, 7, 8]
Interval = "m",
Ticker = "VGT"
for Date in StartDates:
  StartDay = Date
  EndDay = StartDay + 2
  StartDate = datetime(2010, 1, StartDay)
  #EndDate = datetime.today()
  EndDate = datetime(2020, 1, EndDay)
  Amount = 50

  data = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval="m")

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
  print(Ticker + " interval " + Interval )
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
