import pandas_datareader as pdr
from datetime import datetime
import calendar

StartDates = [0, 1, 2, 3, 4]
Interval = "d"
#Ticker = "VGT"
Amount = 50
while 1:
  try:
    Ticker = input("Enter Ticker: ")
    StartDate = input("Enter Start Date (YYYY-mm-dd) default inception: ")
    if StartDate == "":
      StartDate = datetime(1900, 1, 1).date()
    else:
      StartDate = datetime.strptime(StartDate, '%Y-%m-%d')

    CalBasedOn = input("Which data to use (Low, High, Open, Close) (default Close): ")
    if CalBasedOn == "":
      CalBasedOn = 'Close'
  
    EndDate = datetime.now().date()
    rawdata = pdr.get_data_yahoo(Ticker, start=StartDate, end=EndDate, interval=Interval)
    rawdata['DATE'] = rawdata.index.to_pydatetime()
    rawdata['WEEKDAY'] = rawdata['DATE'].dt.weekday
    rawdata['Amount Invested'] = Amount
    rawdata['Share Bought'] = Amount / rawdata[CalBasedOn]
    del rawdata['Adj Close']
    del rawdata['Volume']

    for Day in StartDates:
        data = rawdata.query(f'WEEKDAY == {Day}')
        TotalAmountInvested = data['Amount Invested'].sum()
        TotalShareBought = data['Share Bought'].sum()
        AvgPrice = TotalAmountInvested / TotalShareBought
        ActualStartDate = data.head(1).index.to_pydatetime()[0].date()
        ActualEndDate = data.tail(1).index.to_pydatetime()[0].date()
        LastPrice = data.tail(1).get(CalBasedOn).values[0]
        #print(f"StartDate: {StartDate} Ticker: {Ticker}  interval:  {Interval}" )
        print(f"{ActualStartDate} {calendar.day_name[ActualStartDate.weekday()]} - {ActualEndDate} {calendar.day_name[ActualEndDate.weekday()]}")
        #print(f"Total Amount Invested = {TotalAmountInvested}")
        #print(f"Total Shares Own = {TotalShareBought}")
        #print(f"Avg Price paid per share = {AvgPrice}")
        #print(f"Total Value = {TotalShareBought*LastPrice}")
        #print(f"Total Return $ = {(TotalShareBought*LastPrice)-TotalAmountInvested}")
        TotalReturn = ((TotalShareBought * LastPrice) -
                    TotalAmountInvested) / TotalAmountInvested * 100
        TotalYearsInvested = ((ActualEndDate-ActualStartDate).days/365) 
        print("Total Return = {:.2f}%, Total Avg Return is = {:.2f}% over {:.2f} years".format(TotalReturn, TotalReturn/TotalYearsInvested, TotalYearsInvested))
  except:
    print('Something went wrong ! try again')
  print("-------------------------------------------------")
  print()
