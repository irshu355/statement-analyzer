import requests
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup
from lxml.html import fromstring
from requests import get
import collections
import string
import os.path
import statementutils.utils
import pandas as pd
import re
from nltk.tokenize import word_tokenize
import csv
from nltk.corpus import stopwords
import numpy
from statementutils.normalization_utils import Normalization
class Scrapper():
    def __init__(self):
        self.api_key = 'AIzaSyDDO4EvyHPHHHkM9By6gDef4M23o73ztSQ'
        self.cx = '011606764591163428756:h3frrbtvmyw'
        self.url = 'https://www.googleapis.com/customsearch/v1'
        self.normalization = Normalization()
    def query(self,q):
        #using google search api
        # params = dict(
        #     key=self.api_key,
        #     cx=self.cx,
        #     q=q
        # )

        # r = requests.get(self.url, params=params)
        # json = r.json()

        # items =  json["items"]
        # matches = [x for x in items if not 'mime' in x]
        # self.scrap(matches[0]["link"],q)

        #uncomment for using google url scrapping
        escaped_search_term ='+'.join(q.split())
        USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        google_url = 'https://www.google.com.my/search?q={}&num={}&hl={}'.format(escaped_search_term, 10, 'en')
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
                if not description:
                    continue
                else:
                    description = description.get_text()
                if link != '#':
                    found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description,'href':link})
                    rank += 1
        self.findBestmatch(found_results,keyword)
        #self.writeToDs(found_results[0].get('title'),found_results[0].get('description'),keyword)
       
    def findBestmatch(self,results,keyword):
        fname = 'scrap_meta/result-{0}.csv'.format(keyword)

        # with open(fname, mode = 'w') as results_file:
        #     scrap_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     for i in range(len(results)):
        #         scrap_writer.writerow([results[i].get('rank'),results[i].get('title'),results[i].get('description')])

        words = numpy.array([])
        for i in range(len(results)):
            results[i]['title'] =  self.normalization.do(results[i].get('title'))
            results[i]['description'] = self.normalization.do(results[i].get('description'))
            token_title = word_tokenize(results[i]['title'])
            token_desc = word_tokenize(results[i]['description'])
            words = numpy.append(words,token_title)
            words = numpy.append(words,token_desc)
            results[i]['tokens'] = numpy.array(token_title+token_desc)

        #tokenize words
        # words + = word_tokenize(results[i]['title'])
        # words + = word_tokenize(results[i]['description'])


        df = pd.DataFrame({ 'words': words })
        print(df["words"])
        groupby = df.groupby(by=['words']).size().reset_index(name='count').sort_values(by=['count'],ascending=False)
        
        # now we have the most used words in the document
        # remove first and second word
        # loop through each title and desc inside results
        # take the top 3, and find intersection
        # find 3 titles and descriptions from the list.
        # then crawl and retrieve the title and meta of those websites
        # append them one after another and insert into the dataset

        df = groupby.iloc[2:7]
        print(groupby.values)
        print(df['words'])
        values = df['words'].to_numpy()
        print(values)
        dt = numpy.dtype([('position', 'int'), ('matches', 'int')])
        ranking = numpy.array([], dtype = dt )
        for i in range(len(results)):
            result_tokens = results[i]['tokens']
            intersect = numpy.intersect1d(values,result_tokens)
            ranking = numpy.append(ranking,numpy.array((i,intersect.size), dtype=dt))
        ranking = numpy.sort(ranking, order='matches')
        ranking = ranking[0:3]
        ranking = numpy.flipud(ranking)
        scrap_data = numpy.array([])
        for x in numpy.nditer(ranking):
           scrap_text = self.scrap(results[x.item(0)[0]]['href'],keyword)
           scrap_data = numpy.append(scrap_data,scrap_text[0]+'. '+scrap_text[1])
        joined = '.'.join(scrap_data)
        joined = re.sub(r'[^a-zA-Z0-9.]+', ' ', joined)
        self.writeToDs(joined, keyword)
        



    def writeToDs(self, line,keyword):
        mode = 'w'
        fname = 'dataset.csv'
        if os.path.isfile(fname):
            mode = 'a'

        with open(fname, mode = mode) as spendings_file:
            scrap_writer = csv.writer(spendings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            scrap_writer.writerow([keyword, line])

    def scrap(self, req_url, keyword):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=req_url, headers=headers)

        webpage = urlopen(req).read()
        
        soup = BeautifulSoup(webpage, "lxml")
        desc = self.getDescription(soup)
        title = self.getTitle(soup)
        if not desc: desc = ''
        return (title,desc)



    def getTitle(self,soup):
        node = soup.find("meta",  property="og:title")
        if not node or not node['content']:
            return soup.title.string.strip()
        return node['content']

    def getDescription(self,soup):
        node = soup.find("meta",  property="og:description")
        if not node:
            results = soup.find_all('meta', attrs={'name': 'description'})
            if len(results) == 0:
                return ''
            node = results[0]
        return node['content']


    
    

    