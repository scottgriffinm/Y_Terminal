#! python3
#! G_Terminal.py

'''
This is a terminal interface that facilitates a financial analysis tool.

'''

'''
TODO:
'''

import sys
import os
import time
import random
import pandas as pd
import yfinance as yf
from tickerAnalysis import tickerAnalysis



def insertSpace():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    


version = '0.0170'

# Inspirational quotes list
inspirationalQuotes = [
    '''You can't take no breaks. - Ray Lewis''',
    '''I feel like I have something to prove.
I'm just not this cool fashion kid that be around ASAP Rocky.
- Playboi Carti.''',
    '''I was the first to wear colored skinny jeans.
- Playboi Carti''',
    '''I was never really good at anything except for the ability to learn.
- Kanye West''',
    '''I played the coronet first, and then I upgraded to the trumpet.
First song I learned on there was 'Hot Cross Buns.'
- Lil Uzi Vert'''
    ]



# Main loop
while True:

    print(f'''
Welcome to the

G _ T E R M I N A L

version {version}



Menu
-----------------------------------------------
(type a command below and hit enter)

-h      How to use the G_Terminal
-v      Version and information
-a      Historical analysis tool
-m      Motivation

''')

    while True: # command choice loop
        choice = input()

        if choice == '-h': # Help message
            insertSpace() # a bunch of newlines
            print('''
---------------------------------------------------------------------------------------------------------------
How to use the G_Terminal:

    You enter in commands by typing the commands and pressing the enter key.
---------------------------------------------------------------------------------------------------------------
Historical analysis tool (-a):

    The usage of this tool is to enter in the ticker of the stock/cryptocurrency/index that you want to analyze,
    as it is listed on finance.yahoo.com. So if you are unsure of what the ticker for Bitcoin is, you would
    go to finance.yahoo.com and type in Bitcoin. The ticker for the price of Bitcoin in U.S dollars is (BTC-USD).

    The exact process of analysis is as follows:
    
        1. All of the monthly price data (on finance.yahoo.com) for the tickers entered is collected and stored.
        2. Monthly return on investment based solely on price is calculated for each of the tickers.
        3. All dividend data is collected for each of the tickers.
        4. The monthly average and standard deviation of returns is calculated for each of the tickers, as well
        as expected monthly dividends.
        5. (4.) is repeated, but for a yearly timeframe.
        6. A probability distribution of returns is created for a monthly and yearly timeframe, based on the
        Standard Normal Table.

    For this version you can analyze up to three (3) tickers at once.
---------------------------------------------------------------------------------------------------------------
Version and information (-v):

    This displays the current version of the G_Terminal as well as some information about it.
---------------------------------------------------------------------------------------------------------------
Motivation (-m):

    Gives the user some motivation to work hard.
---------------------------------------------------------------------------------------------------------------
Secret guh (im not telling you):

    Secret guh.
---------------------------------------------------------------------------------------------------------------

''')
            while True:
                print('Press enter to return to menu.')
                choice = input()
                if choice == '':
                    insertSpace()
                    break
            break
            
        elif choice == '-v': # Version message
            insertSpace()
            print('''
G_Terminal
version {version}
no copyright go bananas

Written by Scott Griffin in Python 3
email->scottgriffinm@gmail.com
''')
            while True:
                print('Press enter to return to menu.')
                choice = input()
                if choice == '':
                    insertSpace()
                    break
            break

        
        elif choice == '-a': # Ticker analysis function
            insertSpace()
            tickerAnalysis() 
            break
        
        
        elif choice == '-m':
            insertSpace()
            random.shuffle(inspirationalQuotes)
            print(inspirationalQuotes[0])
            
            while True:
                print('Press enter to return to menu.')
                choice = input()
                if choice == '':
                    insertSpace()
                    break
            break

        elif choice == 'guh': # Secret guh
            insertSpace()
            print('''
              0
             /|\\
              |
             / \\
            ''')
            print('CONGRATULATIONS!!!\nYou found the secret guh.')
            
            while True:
                print('Press enter to return to menu.')
                choice = input()
                if choice == '':
                    insertSpace()
                    break
            break
                

        else: # Invalid input
            print('Invalid input. Type -h and hit enter for help.')
            continue

        







    
    
    
