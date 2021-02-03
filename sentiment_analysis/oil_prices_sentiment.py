import pandas as pd
import requests

from bs4 import BeautifulSoup

url_list = []
news_text = []
headlines = [] 

# Parameters of range function correspond to page numbers in the website with news listings
for i in range(1, 3): 
    url = 'https://oilprice.com/Energy/Crude-Oil/Page-{}.html'.format(i)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    for links in soup.find_all('div', {'class': 'categoryArticle'}):
        for info in links.find_all('a'):
            if info.get('href') not in url_list:
                url_list.append(info.get('href'))

for url in url_list:
    temp = []
    headlines.append(www.split('/')[-1].replace('-', ' '))
    request = requests.get(www)
    soup = BeautifulSoup(request.text, 'html.parser')
    for news in soup.find_all('p'):
            temp.append(news.text)
    
    # Identify last line of news article
    for last_sentence in reversed(temp):
        if last_sentence.split(' ')[0] == 'By' and last_sentence.split(' ')[-1] == 'Oilprice.com':
            break
        elif last_sentence.split(' ')[0] == 'By':
            break
    
    # Prune non-news related text from scraped data to create news text
    joined_text = ' '.join(temp[temp.index('More Info')+1: temp.index(last_sentence)])
    news_text.append(joined_text)
  
news_df = pd.DataFrame({'Headline': headlines,
                        'News': news_text,
                       })

news_df.to_csv('sentiment_analysis/crude_oil_news_articles.csv', index=False)
