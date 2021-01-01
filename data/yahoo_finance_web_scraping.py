# Code snippet for scraping Yahoo! Finance for balance sheet, income statement
# and cash flow statement using BeautifulSoup

import pandas as pd
import requests

from bs4 import BeautifulSoup

tickers = ['AAPL', 'MSFT']
financials = {}

for ticker in tickers:
    temp_dict = {}

    # Get balance sheet
    url = 'https://uk.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all('div', {'class': 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})

    for t in table:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dict[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]

    # Get income statement
    url = 'https://uk.finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all('div', {'class': 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})

    for t in table:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dict[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]

    # Get cash flow statement
    url = 'https://uk.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all('div', {'class': 'M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})

    for t in table:
        rows = t.find_all('div', {'class': 'rw-expnded'})
        for row in rows:
            temp_dict[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[1]

    # Commented out because of change to uk.finance.yahoo.com HTML
    # TODO: find new HTML for key statistics table
    # # Get key statistics
    # url = 'https://uk.finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
    # page = requests.get(url)
    # page_content = page.content
    # soup = BeautifulSoup(page_content, 'html.parser')
    # table = soup.findAll('table', {'class': 'table-qsp-stats Mt(10px)'})

    # for t in table:
    #     rows = t.find_all('tr')
    #     for row in rows:
    #         if len(row.get_text(separator='|').split('|')[0:2]) > 0:
    #             temp_dict[row.get_text(separator='|').split('|')[0]] = row.get_text(separator='|').split('|')[-1]

    financials[ticker] = temp_dict

combined_financials = pd.DataFrame(financials)
tickers = combined_financials.columns

for ticker in tickers:
    combined_financials = combined_financials[~combined_financials[ticker].str.contains('[a-z]').fillna(False)]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(combined_financials)
