from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords

session = requests.session()
import time
from fake_useragent import UserAgent
import random

ua = UserAgent(verify_ssl=False)
headers = {'User-Agent': ua.random}
count = {
    'number': 0
}
print(headers)

sites = ['https://winxopedia.fandom.com/ru/wiki/%D0%91%D0%BB%D1%83%D0%BC',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D1%82%D0%B5%D0%BB%D0%BB%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A4%D0%BB%D0%BE%D1%80%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D1%83%D0%B7%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D0%B5%D0%BA%D0%BD%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9B%D0%B5%D0%B9%D0%BB%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D0%BA%D0%B0%D0%B9',
         'https://winxopedia.fandom.com/ru/wiki/%D0%91%D1%80%D0%B5%D0%BD%D0%B4%D0%BE%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A0%D0%B8%D0%B2%D0%B5%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D0%B8%D0%BC%D0%BC%D0%B8',
         'https://winxopedia.fandom.com/ru/wiki/%D0%93%D0%B5%D0%BB%D0%B8%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9D%D0%B0%D0%B1%D1%83',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A0%D0%BE%D0%B9',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9D%D0%B5%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F_%D1%82%D1%80%D0%B0%D0%BD%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%94%D0%B8%D1%81%D1%8D%D0%BD%D1%87%D0%B0%D0%BD%D1%82%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A7%D0%B0%D1%80%D0%BC%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%AD%D0%BD%D1%87%D0%B0%D0%BD%D1%82%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%91%D0%B5%D0%BB%D0%B8%D0%B2%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%93%D0%B0%D1%80%D0%BC%D0%BE%D0%BD%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%91%D0%BB%D1%83%D0%BC%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%B8%D1%84%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%91%D0%B0%D1%82%D1%82%D0%B5%D1%80%D1%84%D0%BB%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D0%B0%D0%B9%D0%BD%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D1%80%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%94%D0%B0%D1%80%D0%BA%D0%B0%D1%80',
         'https://winxopedia.fandom.com/ru/wiki/%D0%92%D0%B0%D0%BB%D1%82%D0%BE%D1%80',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A7%D1%91%D1%80%D0%BD%D1%8B%D0%B9_%D0%BA%D1%80%D1%83%D0%B3',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%BD%D1%83%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%90%D0%BB%D1%84%D0%B5%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9A%D0%BE%D0%B4%D0%B5%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9E%D0%B1%D0%BB%D0%B0%D1%87%D0%BD%D0%B0%D1%8F_%D0%91%D0%B0%D1%88%D0%BD%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9A%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6_%D0%90%D0%BB%D1%84%D0%B5%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%92%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5_%D0%B7%D0%B2%D1%91%D0%B7%D0%B4%D1%8B',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A0%D0%BE%D0%BA%D1%81%D0%B8',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%BE%D1%80%D0%B3%D0%B0%D0%BD%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%94%D0%B8%D0%B0%D0%BD%D0%B0_(%D1%81%D1%82%D0%B0%D1%80%D1%88%D0%B0%D1%8F_%D1%84%D0%B5%D1%8F)',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9D%D0%B5%D0%B1%D1%83%D0%BB%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%90%D0%B2%D1%80%D0%BE%D1%80%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D0%B8%D0%B1%D0%B8%D0%BB%D0%BB%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%93%D1%80%D0%B8%D1%84%D1%84%D0%B8%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A4%D0%B0%D1%80%D0%B0%D0%B3%D0%BE%D0%BD%D0%B4%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9E%D1%80%D0%B8%D1%82%D0%B5%D0%BB',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9B%D0%B8%D0%BD%D1%84%D0%B5%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%90%D0%BD%D0%B4%D1%80%D0%BE%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D0%BE%D0%BB%D1%8F%D1%80%D0%B8%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%94%D0%BE%D0%BC%D0%B8%D0%BD%D0%BE',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%B5%D0%BB%D0%BE%D0%B4%D0%B8%D1%8F',
         'https://winxopedia.fandom.com/ru/wiki/%D0%97%D0%B5%D0%BD%D0%B8%D1%82',
         'https://winxopedia.fandom.com/ru/wiki/%D0%AD%D1%80%D0%B0%D0%BA%D0%BB%D0%B8%D0%BE%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%B0%D0%B3%D0%B8%D0%BA%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9E%D0%BC%D0%B5%D0%B3%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9E%D0%B1%D1%81%D0%B8%D0%B4%D0%B8%D0%B0%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A2%D0%B5%D0%BD%D1%8C_%D0%A4%D0%B5%D0%BD%D0%B8%D0%BA%D1%81%D0%B0_(%D0%BC%D0%B0%D0%B3%D0%B8%D1%8F)',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A7%D0%B5%D1%80%D0%B5%D0%BF_%D0%94%D1%80%D0%B0%D0%BA%D0%BE%D0%BD%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%B0%D0%BD%D0%B4%D1%80%D0%B0%D0%B3%D0%BE%D1%80%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9B%D1%83%D0%BD%D0%B0_(%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0)',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9C%D0%B0%D1%80%D0%B8%D0%BE%D0%BD',
         'https://winxopedia.fandom.com/ru/wiki/%D0%AD%D1%80%D0%B5%D0%BD%D0%B4%D0%BE%D1%80',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0',
         'https://winxopedia.fandom.com/ru/wiki/%D0%A0%D0%B0%D0%B4%D0%B8%D1%83%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%93%D0%B0%D1%80%D0%BC%D0%BE%D0%BD%D0%B8%D1%83%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B8%D0%BE%D1%81',
         'https://winxopedia.fandom.com/ru/wiki/%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8_%D0%A2%D1%80%D0%B8%D0%BA%D1%81'
         ]

all_texts = list()

for link in sites:
    link_i = session.get(link, proxies={'https://135.181.61.25': '36135'}, headers=headers)
    time.sleep(random.uniform(5, 8.4))
    soup_link_i = BeautifulSoup(link_i.content, 'html.parser')
    time.sleep(random.uniform(3, 6.2))
    text = soup_link_i.find('div', class_='mw-content-ltr').text
    all_texts.append(text)
    print('Done!')
with open('winx_text.txt', 'w', encoding='utf-8') as file:
    for text in all_texts:
        new_text = str()
        text = text.replace('{\s}', '\n')
        text = text.replace('.', '')
        text = text.replace('!', '')
        text = text.replace('?', '')
        text = re.sub('\n\n', '\n', text)
        text = text.replace('-', '')
        text = text.replace(':', '')
        text = text.replace(',', '')
        text = text.replace(';', '')
        text = text.replace('\t', '')
        text = text.replace('{', '')
        text = text.replace('}', '')
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('"', '')
        words = text.split(' ')
        for word in words:
            if word not in stopwords.words('russian'):
                new_text = new_text + word + ' '
        file.write(new_text)
        file.write('\n')
