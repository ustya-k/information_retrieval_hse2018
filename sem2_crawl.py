
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import re
import random
import time
import os


global user_agent_list
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def get_soup(url):
    time.sleep(random.uniform(1, 5))
    headers = {'User-Agent': random.choice(user_agent_list)}
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        return None
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    return soup



def get_date(soup):
    txt = soup.find('div', class_='title-info-metadata-item').get_text()
    if 'сегодня' in txt:
        return '9 октября'
    if 'вчера' in txt:
        return '8 октября'
    res = re.search('размещено (.*?) в')
    return res.group(1)



def parse_ad(url):
    cats = ['Заголовок', 'Дата размещения', 'Цена', 'Адрес', 'Контактное лицо', 'Текст объявления']
    ad = {cat: None for cat in cats}
    soup = get_soup(url)
    if soup is None:
        return None
    
    # title
    try:
        ad['Заголовок'] = soup.find('span', attrs={'class': 'title-info-title-text'}).get_text()
    except:
        pass
    # date
    try:
        ad['Дата размещения'] = get_date(soup)
    except:
        pass
    # price
    try:
        ad['Цена'] = soup.find('span', attrs={'class': 'js-item-price'})['content']
    except:
        pass
    # address
    try:
        ad['Адрес'] = soup.find('meta', itemprop='addressLocality')['content']
    except:
        pass
    # owner
    try:
        ad['Контактное лицо'] = soup.find('div', class_='seller-info-prop seller-info-prop_short_margin').find('div', class_='seller-info-value').get_text()
        ad['Контактное лицо'] = ad['Контактное лицо'].strip()
    except:
        pass
    # text
    try:
        ad['Текст объявления'] = soup.find('div', attrs={'class': 'item-description-text'}).get_text(' ', strip=True)
    except:
        pass
    return ad



def parse_list_ads(url):
    ad_urls = {} # id: url
    soup = get_soup(url)
    if soup is None:
        return ad_urls
    items = soup.find_all('a', class_='description-title-link')
    for item in items:
        try:
            ad_urls[item['id']] = item['href']
        except:
            pass
    return ad_urls



def save_ad(ad, url):
    txt = ''
    cats = ['Заголовок', 'Дата размещения', 'Цена', 'Адрес', 'Контактное лицо', 'Текст объявления']
    for cat in cats:
        if ad[cat] is not None:
            txt += '%s: %s\n' % (cat, ad[cat])
    if txt != '':
        with open('ads/' + url + '.txt', 'w', encoding='utf-8') as f:
            f.write(txt)



def process_ad_urls(ad_urls, common_beg):
    for id_ in ad_urls:
        ad = parse_ad(common_beg + ad_urls[id_])
        save_ad(ad, id_)



def save_dict(d, name):
    if type(d) is set:
        output = '\n'.join(d)
    else:
        output = '\n'.join(['%s\t%s' % (key, d[key]) for key in d])
    with open(name + '.tsv', 'w', encoding='utf-8') as f:
        f.write(output)



def get_ads(url, ids, amount=10000):
    '''
    url: str
    ids: set, already parsed ids
    '''
    url_beg = 'https://www.avito.ru'
    page = 1
    while len(ids) < amount:
        page = (page + 1) % 100
        ad_urls = parse_list_ads(url % page)
        save_dict(ad_urls, 'temp')
        
        urls_to_parse = set(ad_urls) - ids
        process_ad_urls({id_: ad_urls[id_] for id_ in urls_to_parse}, url_beg)
        
        ids.update(urls_to_parse)
        save_dict(ids, 'ids')



def get_parsed_ids(file, path=False):
    if path:
        return {f.replace('.txt', '') for f in os.listdir(file)}
    with open(file, 'r', encoding='utf-8') as f:
        return set(f.read().split())

url = 'https://www.avito.ru/rossiya/gotoviy_biznes?p=%d&view=list'

