import requests
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup
from lxml.html import fromstring
from requests import get
import os.path
import csv
class Scrapper():
    def __init__(self):
        self.api_key = 'AIzaSyDDO4EvyHPHHHkM9By6gDef4M23o73ztSQ'
        self.cx = '011606764591163428756:h3frrbtvmyw'
        self.url = 'https://www.googleapis.com/customsearch/v1'

    def query(self,q):

        params = dict(
            key=self.api_key,
            cx=self.cx,
            q=q
        )

        # raw = get("https://www.google.com/search?q=StackOverflow").text
        # page = fromstring(raw)

        # for result in page.cssselect(".r a"):
        #     url = result.get("href")
        #     if url.startswith("/url?"):
        #         url = parse_qs(urlparse(url).query)['q']
        #     print(url[0])

        escaped_search_term = q.replace(' ', '+')
        USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, 10, 'en')
        response = requests.get(google_url, headers=USER_AGENT)
        response.raise_for_status()
 
        self.parse_results(response.text, q)


    def parse_results(self,html, keyword):
        soup = BeautifulSoup(html, 'html.parser')
        found_results = []
        rank = 1
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            description = result.find('span', attrs={'class': 'st'})
            if link and title:
                link = link['href']
                title = title.get_text()
                if description:
                    description = description.get_text()
                if link != '#':
                    found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                    rank += 1
        self.writeToDs(found_results[0].get('title'),found_results[0].get('description'),keyword)   
       
    def writeToDs(self, title, desc, keyword):
        mode = 'w'
        fname = 'dataset.csv'
        if os.path.isfile(fname):
            mode = 'a'
            

        with open(fname, mode = mode) as spendings_file:
            scrap_writer = csv.writer(spendings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            scrap_writer.writerow([keyword, title + ' ' + desc])


    def scrap(self, req_url, keyword):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=req_url, headers=headers) 

        webpage = urlopen(req).read()
        
        soup = BeautifulSoup(webpage, "lxml")
        desc = self.getDescription(soup)
        title = self.getTitle(soup)
        self.writeToDs(title, desc, keyword)



    def getTitle(self,soup):
        node = soup.find("meta",  property="og:title")
        if not node:
            return soup.title.string.strip()
        return node['content']

    def getDescription(self,soup):
        node = soup.find("meta",  property="og:description")
        if not node:
            results = soup.find_all('meta', attrs={'name': 'description'})
            node = results[0]
        return node['content']


    
    

    