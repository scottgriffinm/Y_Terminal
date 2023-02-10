#! python3
#! tickerAnalysis.py

# This script takes a stock ticker or a series of stock tickers and outputs
# a probability distribution of price growth (based on a normal distribution)
# as well as expected dividend yield, for the next month and year.

import sys
import os
import time
import pandas as pd
import yfinance as yf

'''
TODO:

'''        

def tickerAnalysis():
        
    global tickerList
    tickerList = []

    print('''
Type the ticker of the stock you want to analyze, then hit enter.\n
You can analyze a maximum of three stocks at a time.\n
If you want to delete the last ticker you entered, type "delete last" and hit
enter: ''', end='')

    while True:
        ticker = input()

        if (ticker == 'done') & (len(tickerList) > 0): # if user is done inputing tickers move on
            break
        
        elif ((ticker == 'delete last') & (len(tickerList) > 0)): # user wants to delete last input and there is an input to delete
            tickerList = tickerList[:-1] # removes last value from tickerList
            print('\n')
            print('TICKERS'.center(12+4,'-')) # printing table
            for t in tickerList:
                print(str(t).rjust(4))

        elif ((ticker == 'delete last') & (len(tickerList) == 0)): # user wants to delete last input but there are no inputs to delete
            print('''There arent any tickers to delete. ''')

        elif (len(tickerList) == 3):
            print('''You are already at the maximum number of stocks, 3. You can delete the last entry by typing "delete last" and hitting enter. ''')

        else:
            tickerSearch = yf.Ticker(ticker) #turns input into a yf ticker object
            tickerHist = tickerSearch.history(period='5d') # quick historical data grab to check if the ticker exists

            if tickerHist.empty: # if the dataframe is empty (ticker not on yf)
                print('''Please try again. ''')
                
            else: # The ticker exists
                ticker = ticker.upper()
                tickerList.append(ticker)
                print('\n')
                print('TICKERS'.center(12+4,'-')) # printing table
                for t in tickerList:
                    print(str(t).rjust(4))
                print('''\nType next ticker, or type "done" when finished: ''')
    
    print('[Generating Report...]')
    time.sleep(1)
    
    # Download and store historical data for each stock (including dividends)
    data = yf.download(
        tickers = tickerList,
        period = 'max',
        interval = '1mo',
        group_by = 'ticker',
        auto_adjust = True,
        ) # access individual ticker data in the dataframe with data['<ticker>']
            # then to access a column data[('<ticker>'), ('<column>')]


    # If theres more than one ticker
    if len(tickerList)>1:
        
        # Drop irrelevant data (open, high, low, volume), calculate and add relevant columns, add dividends

        # For more than one ticker
        for t in tickerList:
            del data[(t),('Open')] # Had to delete the columns this way because the drop method didnt work with multiple tickers for some reason
            del data[(t),('High')]
            del data[(t),('Low')]
            del data[(t),('Volume')]
            returns = data[(t),('Close')].pct_change() # calculating returns
            data[(t),('Return')] = returns # adding returns data to dataframe
            yahooTick = yf.Ticker(t) # making each ticker a yahoo ticker object
            divData = yahooTick.get_dividends() # dividend data
            data[(t),('Dividends')] = divData # addind dividend data series to dataframe
            
            
            
    else: # If theres only one ticker
        data = data.drop(columns=['Open','High','Low','Volume']) # removing irrelevant data
        returns = data['Close'].pct_change() # calculating returns
        data['Return'] = returns # adding returns data to dataframe
        yahooTick = yf.Ticker(tickerList[0]) # maing each ticker a yahoo ticker object
        divData = yahooTick.get_dividends() # dividend data
        data['Dividends'] = divData # addind dividend data series to dataframe
        

    # Statistics dataframe
    stats = pd.DataFrame({
        'ticker': [],
        'upper10PctMon': [],
        'upper20PctMon': [], # monthly stats
        'middle40PctMon': [],
        'lower20PctMon': [],
        'lower10PctMon': [],
        'expectedDivMon': [],
        'avgReturnMon': [],
        'stdDevMon': [],
        
        'upper10PctYr': [],
        'upper20PctYr': [], # yearly stats
        'middle40PctYr': [],
        'lower20PctYr': [],
        'lower10PctYr': [],
        'expectedDivYr': [],
        'avgReturnYr': [],
        'stdDevYr': [],
        'price':[]
        }, columns=['ticker','upper10PctMon','upper20PctMon','middle40PctMon','lower20PctMon','lower10PctMon','expectedDivMon','avgReturnMon','stdDevMon',
                    'upper10PctYr','upper20PctYr','middle40PctYr','lower20PctYr','lower10PctYr','expectedDivYr','avgReturnYr','stdDevYr','price'])


    # PROBABILITY DISTRIBUTION CALCULATED FROM STANDARD NORMAL TABLE VALUES
    if (len(tickerList)) > 1: # theres more than one ticker
        
        for t in tickerList: # for each ticker

            # Monthly Stats
            expectedDivMon = data[(t),('Dividends')].mean() # expected monthly dividends
            avgReturnMon = data[(t),('Return')].mean() # average monthly return
            stdDevMon = data[(t),('Return')].std() # standard deviation of monthly returns
            
            u10pmHigh = round(100*((3.9*stdDevMon)+avgReturnMon), 2) # higher value of the upper 10% probability distribution, rounded to 2 decimals
            u10pmLow = round(100*((1.28*stdDevMon)+avgReturnMon), 2) # lower value of upper 10% probability distribution, rounded to 2 decimals
            upper10PctMon = f'{u10pmLow}% to {u10pmHigh}%' # making the string that will display the range of returns for upper 10% probability distribution

            # Repeat for the other percentage values in the probability distribution
            u20pmHigh = u10pmLow
            u20pmLow = round(100*((0.52*stdDevMon)+avgReturnMon), 2)
            upper20PctMon = f'{u20pmLow}% to {u20pmHigh}%'

            m40pmHigh = u20pmLow
            m40pmLow = round(100*((-0.52*stdDevMon)+avgReturnMon), 2)
            middle40PctMon = f'{m40pmLow}% to {m40pmHigh}%'

            l20pmHigh = m40pmLow
            l20pmLow = round(100*((-1.28*stdDevMon)+avgReturnMon), 2)
            lower20PctMon = f'{l20pmLow}% to {l20pmHigh}%'

            l10pmHigh = l20pmLow
            l10pmLow = round(100*((-3.9*stdDevMon)+avgReturnMon), 2)
            lower10PctMon = f'{l10pmLow}% to {l10pmHigh}%'
            
            
            # Yearly Stats
                                            # Translating monthly stats into yearly stats
            expectedDivYr = expectedDivMon*12 # expected yearly dividends
            avgReturnYr = ((1+avgReturnMon)**12)-1 # yearly average return
            stdDevYr = stdDevMon*3.46410161514 # yearly std dev of returns (3.46410161514 is the square root of 12)

            u10pyHigh = round(100*((3.9*stdDevYr)+avgReturnYr), 2) # higher value of the upper 10% probability distribution, rounded to 2 decimals
            u10pyLow = round(100*((1.28*stdDevYr)+avgReturnYr), 2) # lower value of upper 10% probability distribution, rounded to 2 decimals
            upper10PctYr = f'{u10pyLow}% to {u10pyHigh}%' # making the string that will display the range of returns for upper 10% probability distribution

            # Repeat for the other percentage values in the probability distribution
            u20pyHigh = u10pyLow
            u20pyLow = round(100*((0.52*stdDevYr)+avgReturnYr), 2)
            upper20PctYr = f'{u20pyLow}% to {u20pyHigh}%'

            m40pyHigh = u20pyLow
            m40pyLow = round(100*((-0.52*stdDevYr)+avgReturnYr), 2)
            middle40PctYr = f'{m40pyLow}% to {m40pyHigh}%'

            l20pyHigh = m40pyLow
            l20pyLow = round(100*((-1.28*stdDevYr)+avgReturnYr), 2)
            lower20PctYr = f'{l20pyLow}% to {l20pyHigh}%'

            l10pyHigh = l20pyLow
            l10pyLow = round(100*((-3.9*stdDevYr)+avgReturnYr), 2)
            lower10PctYr = f'{l10pyLow}% to {l10pyHigh}%'

            
            # convert to a percent, and round the average returns and standard deviations to 2 decimal places, also round expected dividends
            #, and turn into a string with a percent sign (or add a dollar sign for dividends)
            avgReturnMon = round(100*avgReturnMon, 2)
            avgReturnYr = round(100*avgReturnYr, 2)
            avgReturnMon = f'{avgReturnMon}%'
            avgReturnYr = f'{avgReturnYr}%'

            stdDevMon = round(100*stdDevMon, 2)
            stdDevYr = round(100*stdDevYr, 2)
            stdDevMon = f'{stdDevMon}%'
            stdDevYr = f'{stdDevYr}%'
            
            expectedDivMon = round(expectedDivMon, 2)
            expectedDivYr = round(expectedDivYr, 2)
            expectedDivMon = f'${expectedDivMon}'
            expectedDivYr = f'${expectedDivYr}'
            # change null expected dividends to display None
            if expectedDivMon == '$nan':
                expectedDivMon = 'None'
            if expectedDivYr == '$nan':
                expectedDivYr = 'None'

            # Current price
            price = round(data[t].iloc[-1][0],2)
            

            # Add Values to stats dataframe
            stats.loc[len(stats.index)] = [t,upper10PctMon,upper20PctMon,middle40PctMon,lower20PctMon,lower10PctMon,expectedDivMon,avgReturnMon,stdDevMon,
                    upper10PctYr,upper20PctYr,middle40PctYr,lower20PctYr,lower10PctYr,expectedDivYr,avgReturnYr,stdDevYr,price]

                   
            
    else: # theres only one ticker

        t = tickerList[0] 
        
        # Monthly Stats
        expectedDivMon = data['Dividends'].mean() # expected monthly dividends
        avgReturnMon = data['Return'].mean() # average monthly return
        stdDevMon = data['Return'].std() # standard deviation of monthly returns
        
        u10pmHigh = round(100*((3.9*stdDevMon)+avgReturnMon), 2) # higher value of the upper 10% probability distribution, rounded to 2 decimals
        u10pmLow = round(100*((1.28*stdDevMon)+avgReturnMon), 2) # lower value of upper 10% probability distribution, rounded to 2 decimals
        upper10PctMon = f'{u10pmLow}% to {u10pmHigh}%' # making the string that will display the range of returns for upper 10% probability distribution

        # Repeat for the other percentage values in the probability distribution
        u20pmHigh = u10pmLow
        u20pmLow = round(100*((0.52*stdDevMon)+avgReturnMon), 2)
        upper20PctMon = f'{u20pmLow}% to {u20pmHigh}%'

        m40pmHigh = u20pmLow
        m40pmLow = round(100*((-0.52*stdDevMon)+avgReturnMon), 2)
        middle40PctMon = f'{m40pmLow}% to {m40pmHigh}%'

        l20pmHigh = m40pmLow
        l20pmLow = round(100*((-1.28*stdDevMon)+avgReturnMon), 2)
        lower20PctMon = f'{l20pmLow}% to {l20pmHigh}%'

        l10pmHigh = l20pmLow
        l10pmLow = round(100*((-3.9*stdDevMon)+avgReturnMon), 2)
        lower10PctMon = f'{l10pmLow}% to {l10pmHigh}%'
        
        
        # Yearly Stats
                                        # Translating monthly stats into yearly stats
        expectedDivYr = expectedDivMon*12 # expected yearly dividends
        avgReturnYr = ((1+avgReturnMon)**12)-1 # yearly average return
        stdDevYr = stdDevMon*3.46410161514 # yearly std dev of returns (3.46410161514 is the square root of 12)

        u10pyHigh = round(100*((3.9*stdDevYr)+avgReturnYr), 2) # higher value of the upper 10% probability distribution, rounded to 2 decimals
        u10pyLow = round(100*((1.28*stdDevYr)+avgReturnYr), 2) # lower value of upper 10% probability distribution, rounded to 2 decimals
        upper10PctYr = f'{u10pyLow}% to {u10pyHigh}%' # making the string that will display the range of returns for upper 10% probability distribution

        # Repeat for the other percentage values in the probability distribution
        u20pyHigh = u10pyLow
        u20pyLow = round(100*((0.52*stdDevYr)+avgReturnYr), 2)
        upper20PctYr = f'{u20pyLow}% to {u20pyHigh}%'

        m40pyHigh = u20pyLow
        m40pyLow = round(100*((-0.52*stdDevYr)+avgReturnYr), 2)
        middle40PctYr = f'{m40pyLow}% to {m40pyHigh}%'

        l20pyHigh = m40pyLow
        l20pyLow = round(100*((-1.28*stdDevYr)+avgReturnYr), 2)
        lower20PctYr = f'{l20pyLow}% to {l20pyHigh}%'

        l10pyHigh = l20pyLow
        l10pyLow = round(100*((-3.9*stdDevYr)+avgReturnYr), 2)
        lower10PctYr = f'{l10pyLow}% to {l10pyHigh}%'

        
        # convert to a percent, and round the average returns and standard deviations to 2 decimal places, also round expected dividends
        #, and turn into a string with a percent sign (or add a dollar sign for dividends)
        avgReturnMon = round(100*avgReturnMon, 2)
        avgReturnYr = round(100*avgReturnYr, 2)
        avgReturnMon = f'{avgReturnMon}%'
        avgReturnYr = f'{avgReturnYr}%'

        stdDevMon = round(100*stdDevMon, 2)
        stdDevYr = round(100*stdDevYr, 2)
        stdDevMon = f'{stdDevMon}%'
        stdDevYr = f'{stdDevYr}%'
        
        expectedDivMon = round(expectedDivMon, 2)
        expectedDivYr = round(expectedDivYr, 2)
        expectedDivMon = f'${expectedDivMon}'
        expectedDivYr = f'${expectedDivYr}'
        # change null expected dividends to display None
        if expectedDivMon == '$nan':
            expectedDivMon = 'None'
        if expectedDivYr == '$nan':
            expectedDivYr = 'None'

        # Current price
        price = round(data.iloc[-1][0],2)
        
        # Add Values to stats dataframe
        stats.loc[len(stats.index)] = [t,upper10PctMon,upper20PctMon,middle40PctMon,lower20PctMon,lower10PctMon,expectedDivMon,avgReturnMon,stdDevMon,
                upper10PctYr,upper20PctYr,middle40PctYr,lower20PctYr,lower10PctYr,expectedDivYr,avgReturnYr,stdDevYr,price]



    # Set tickers to index value
    stats = stats.set_index('ticker')

    # Display report
    print('''
    BEGINNING OF REPORT:

           NEXT MONTH
           __________________________________''')
          
    for ticker in tickerList:
          r1 = stats.loc[ticker,'upper10PctMon']
          r2 = stats.loc[ticker,'upper20PctMon']
          r3 = stats.loc[ticker,'middle40PctMon']
          r4 = stats.loc[ticker,'lower20PctMon']
          r5 = stats.loc[ticker,'lower10PctMon']
          r6 = stats.loc[ticker,'expectedDivMon']
          r7 = stats.loc[ticker,'avgReturnMon']
          r8 = stats.loc[ticker,'stdDevMon']
          price = stats.loc[ticker, 'price']

          print(f'''
             {ticker}: ${price}
           
            Probability |     Return
                 10%    |  {r1}
                 20%    |  {r2}
                 40%    |  {r3}
                 20%    |  {r4}
                 10%    |  {r5}
           
            Expected Dividends = {r6}     
            Average Return = {r7}
            Standard Deviation = {r8}
           __________________________________''')

    print('''

           NEXT YEAR
           __________________________________''')
          
    for ticker in tickerList:
          r9 = stats.loc[ticker,'upper10PctYr']
          r10 = stats.loc[ticker,'upper20PctYr']
          r11 = stats.loc[ticker,'middle40PctYr']
          r12 = stats.loc[ticker,'lower20PctYr']
          r13 = stats.loc[ticker,'lower10PctYr']
          r14 = stats.loc[ticker,'expectedDivYr']
          r15 = stats.loc[ticker,'avgReturnYr']
          r16 = stats.loc[ticker,'stdDevYr']
          price = stats.loc[ticker, 'price']

          print(f'''
             {ticker}: ${price}
           
            Probability |     Return
                 10%    |  {r9}
                 20%    |  {r10}
                 40%    |  {r11}
                 20%    |  {r12}
                 10%    |  {r13}
           
            Expected Dividends = {r14}     
            Average Return = {r15}
            Standard Deviation = {r16}
           __________________________________''')

    print('END OF REPORT\n')

    print('Export to excel sheet? y/(n)')
    while True:
        choice = input()
        
        if choice == 'y':
            print('''[Creating .csv files...}''')
            compression_Ticker_Data = dict(method='zip',
                                           archive_name='Ticker_Data.csv')
            compression_Ticker_Stats = dict(method='zip',
                                            archive_name='Ticker_Stats.csv')
            data.to_csv('Ticker_Data.zip', compression = compression_Ticker_Data)
            stats.to_csv('Ticker_Stats.zip', compression = compression_Ticker_Stats)
            print('''[Ticker_Stats.zip, Ticker_Data.zip files created in Y_Terminal folder.]\n''')
            break
        
        if (choice != '') & (choice != 'n') & (choice != 'y'):
            print('Invalid input. Please input either y or n.')
            continue
        
        break



        

