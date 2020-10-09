import pandas_datareader as pdr
from datetime import datetime
import calendar

StartDates = [0, 1, 2, 3, 4]
Interval = "d"
#Ticker = "VGT"
Amount = 50
while 1:
  Ticker = input("Enter Ticker: ")
  DefaultStartDate = datetime(1900, 1, 1).date()
  StartDate = input("Enter Start Date (YYYY-mm-dd): ")
  if StartDate == "":
    StartDate = DefaultStartDate
  else:
    StartDate = datetime.strptime(StartDate, '%Y-%m-%d')
  EndDate = datetime.now().date()
  rawdata = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval=Interval)
  rawdata['DATE'] = rawdata.index.to_pydatetime()
  rawdata['WEEKDAY'] = rawdata['DATE'].dt.weekday
  rawdata['Amount Invested'] = Amount
  rawdata['Share Bought'] = Amount / rawdata['Close']
  del rawdata['Open']
  del rawdata['Low']
  del rawdata['High']
  del rawdata['Adj Close']
  del rawdata['Volume']

  for Day in StartDates:
      data = rawdata.query(f'WEEKDAY == {Day}')
      
      TotalAmountInvested = data['Amount Invested'].sum()
      TotalShareBought = data['Share Bought'].sum()
      AvgPrice = TotalAmountInvested / TotalShareBought
      ActualStartDate = data.head(1).index.to_pydatetime()[0].date()
      LastPrice = data.tail(1).get('Close').values[0]
      #print(f"StartDate: {StartDate} Ticker: {Ticker}  interval:  {Interval}" )
      print(f"{ActualStartDate} {calendar.day_name[ActualStartDate.weekday()]} - {EndDate} {calendar.day_name[EndDate.weekday()]}")
      #print(f"Total Amount Invested = {TotalAmountInvested}")
      #print(f"Total Shares Own = {TotalShareBought}")
      #print(f"Avg Price paid per share = {AvgPrice}")
      #print(f"Total Value = {TotalShareBought*LastPrice}")
      #print(f"Total Return $ = {(TotalShareBought*LastPrice)-TotalAmountInvested}")
      TotalReturn = ((TotalShareBought * LastPrice) -
                  TotalAmountInvested) / TotalAmountInvested * 100
      print("Total Return % = {:.2f}".format(TotalReturn))
  print("-------------------------------------------------")
  print()
