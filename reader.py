import fitz
import re
import sys, json
from maybank.maybanksavingsstmt import MaybankSavingsStmt
from operator import itemgetter
import pandas
import time
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl
import globals
from statementutils import utils
from csvwriter import CSVWriter
from scrapper import Scrapper
from enums import Bank, Countries
import numpy
from statementutils.statementpatterns import StatementPatterns
doc = fitz.open('statement2.pdf')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
# Maybank statements:
maybankstmt = MaybankSavingsStmt(doc)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)
credits = maybankstmt.findOutflows()
debits = maybankstmt.findInflows()
bank  = Bank.my_maybank
csvWriter = CSVWriter()
csvWriter.write(credits)

scrap_text  = 'airasia berhad'
scrap = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n Home\n\nAbout Us\n\nInvestor Relations\n\n\n\n\n\n\n\n\n\n\nInvestor relations\n\nWelcome to AirAsia\'s Investor relations page\n\n\r\n\t\t\t       At AirAsia, we adhere to stringent regulatory requirements, placing high emphasis on transparency and practicing good corporate governance. Our vision is to provide a consistent communication platform to our stakeholders globally.\r\n\t\t\t      \r\n\t\t\t       Catch the latest updates and insights on AirAsia and the Group’s IR initiatives:\r\n\t\t\t     \n\nFollow @AirAsia_IR\n\n\n\n\n\n\n\nAirAsia Group Berhad\n\n\n\n\nAirAsia Group Berhad\n\r\n\t\t\t\t\t\t\t\t AirAsia Berhad was listed on the Main Market of Bursa Malaysia Securities Berhad in November 2004. AirAsia Group Berhad (AAGB) has assumed the listing status of AirAsia Berhad as of 16 April 2018 as a completion of internal reorganisation. Since pioneering the short-haul low-cost carrier (LCC) model in Asean in 2001, AirAsia has grown from a domestic airline in Malaysia into Asia\'s leading low-cost airline serving more than 130 destinations across Asia Pacific. Together with its affiliates in Thailand, Indonesia, the Philippines, India and Japan, AirAsia is the largest low-cost carrier in Asia by passengers carried. AirAsia has been named the World’s Best Low-Cost Airline by Skytrax for nine years in a row from 2009 to 2017 and the World’s Leading Low-Cost Airline at the annual World Travel Awards for five consecutive years from 2013 to 2017.\r\n\t\t\t\t\t\t\t\n\n\r\n\t\t\t\t\t\t\t\t More Detail ≫\r\n\t\t\t\t\t\t\t\n\n\n\n\n\n\n\n\n\n\n\n\n\nAirAsia X Berhad\n\n\n\n\nAirAsia X Berhad\n\r\n\t\t\t\t\t\t\t\t AirAsia X is the long-haul, low-cost affiliate carrier of the AirAsia Group that currently flies to destinations in the Asia Pacific region and beyond. The airline currently serves 23 destinations across Asia, Australia, New Zealand, the Middle East and Africa. AirAsia X operates a core fleet of 30 A330-300s. The airline has carried over 19 million guests since it commenced long-haul service in 2007. AirAsia X was awarded World\'s Best Low Cost Airline Premium Cabin and Best Low Cost Airline Premium Seat at the annual Skytrax World Airline Awards for four consecutive years from 2013 to 2016.\r\n\t\t\t\t\t\t\t\n\n\r\n\t\t\t\t\t\t\t\t More Detail ≫\r\n\t\t\t\t\t\t\t\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nAsia Aviation \r\n\t\t\t\t\t Public Company Limited  ("Asia Aviation")\n\n\n\n\nAsia Aviation\n\r\n\t\t\t\t\t\t\t\t Asia Aviation was listed on the Stock Exchange of Thailand in May 2012 and is the investment holding company of Thai AirAsia Co., Ltd. Thai AirAsia commenced its inaugural commercial flight on 4 February 2004 from Bangkok to Hat Yai. The airline rapidly expanded its domestic and international route network. As of December 2016, the airline has doubled its number of destinations from five years ago, covering 20 domestic and 29 international cities utilising a fleet of 49 Airbus A320 aircraft and two state-of-the-art Airbus A320neo.\r\n\t\t\t\t\t\t\t\n\n\r\n\t\t\t\t\t\t\t\t More Detail ≫\r\n\t\t\t\t\t\t\t\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPT AirAsia Indonesia Tbk \n\n\n\n\nPT AirAsia Indonesia Tbk\n\r\n\t\t\t\t\t\t\t\t PT AirAsia Indonesia Tbk (AAID) is officially a parent company of PT Indonesia AirAsia (IAA) starting 29 December 2017. PT AirAsia Indonesia Tbk, previously PT Rimau Multi Putra Pratama Tbk (RMPP) is a publicly listed company in the Indonesia Stock Exchange (IDX). Change of company name from RMPP to AAID has been approved by the Ministry of Law and Human Rights of the Republic of Indonesia.\r\n\t\t\t\t\t\t\t\n\n\r\n\t\t\t\t\t\t\t\t More Detail ≫\r\n\t\t\t\t\t\t\t\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'

dt = numpy.dtype([('position', 'int'), ('matches', 'int')])
occrurances = numpy.array([], dtype = dt)
tokenized = scrap_text.split()
for i in range(len(tokenized)):
    count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(tokenized[i]), scrap.lower()))
    occrurances = numpy.append(occrurances, numpy.array((i,count), dtype=dt))
occrurances = numpy.sort(occrurances, order='matches')
occrurances = numpy.flipud(occrurances)

texts = re.findall(r"([^.]*?"+tokenized[occrurances.item(0)[0]]+"[^.]*\.)",scrap.lower())

leng = len(texts)


# first tokenize
# second find number of occrurances for each.
# 


# found_results = []
# found_results.append({'keyword': 'xx','href':'#', 'rank': 1, 'title': 'AirAsia Group Berhad is the low cost!!!', 'description': "Catch the latest updates and insights on AirAsia and the Group's IR initiatives: Follow @ ... AirAsia Group Berhad ..."})
# found_results.append({'keyword': 'xx','href':'#', 'rank': 2, 'title': 'AirAsia: Book Cheap Flights Online To Over 130 Destinations!', 'description': "Catch the latest updates and insights on AirAsia and the Group's IR initiatives: Follow @ ... AirAsia Group Berhad ..."})
# sc1.findBestmatch(found_results,'xx')

pandas.set_option('display.max_colwidth', -1)
df = pandas.DataFrame.from_records([c.to_dict() for c in credits])

print(df.values)

print('printing the dataset')
dfDataset = pandas.read_csv("dataset.csv") 

# print(df.columns)
# print(df['amount'])
groupby_withdrawals = df.groupby(by=['desc'])
spending_avg = groupby_withdrawals.head()
# print(groupby_withdrawals.sum())
# print(groupby_withdrawals.count())

# cleanse

# stop = stopwords.words('english') + ['via','*', 'tt','dr','a/','pymt', 'a/c']
df['desc'] = df['desc']
# df['desc'] = df['desc'].apply(lambda x: x.lower())
# df['desc'] = df['desc'].apply(lambda x: ' '.join([word for word in x.lower().split() if word not in (stop)]))
df['desc'] = df['desc'].apply(lambda x: re.sub(r'(\S+\d+){1,}','',x))

sc = Scrapper()
statementPatterns = StatementPatterns(bank)
size = df.head().size
#17

# df = df.iloc[16:]
stop_words = stopwords.words('english') + ['via','*', 'tt','dr','a/','pymt', 'a/c']
txn_names = dfDataset['txn']
txn_names = utils.cleanTransDataset(txn_names, Countries.malaysia )

tokenizer = TfidfVectorizer(min_df=1, stop_words = stop_words) # initiate here your own tokenizer (TfidfVectorizer, CountVectorizer, with stopwords...)


cacheDesc = set()
txn_list = dfDataset["txn"].values
s = pandas.Series(txn_list)


for row in df.itertuples():
    desc = row[3].lower()

    filters = statementPatterns.getStopWords()
    for i in range(len(filters)):

        fltr = filters[i]
        fltr = r"\b"+fltr+r"\b"
        desc = re.sub(fltr,'',desc)
    if not desc.strip():
        sc.writeToDs(row[3].lower() +" uncategorized transaction ",row[3].lower())
        continue

    # descStripped = ' '.join([word for word in desc.split() if word not in (stop)])
    descStripped = desc
    descStripped = re.sub(r'\W+', ' ', descStripped)
    descStripped = descStripped.strip()


    if descStripped in cacheDesc:
        continue
    if descStripped in s.to_list():
        continue


    cacheDesc.add(descStripped)
    if utils.hasValue(statementPatterns.getUncategorizedPatterns(),descStripped):
        print('write ', desc)
        sc.writeToDs(desc +" uncategorized transaction",descStripped)
    elif utils.hasValue(statementPatterns.getShoppingPatterns(),descStripped):
        print('write ', descStripped)
        sc.writeToDs(desc +" shopping online shopping purchase",descStripped)
    elif utils.hasValue(statementPatterns.getUtilitiesPatterns(),descStripped):
        print('write ', descStripped)
        sc.writeToDs(desc + " utilities phone bills bills",descStripped)
    else:
        cleansed = utils.cleanseDesc(descStripped,Countries.malaysia)
        test_set = pandas.Series([utils.cleanseDesc(descStripped,Countries.malaysia)])
        score = utils.create_tokenizer_score(test_set,txn_names, tokenizer=tokenizer)
        print(score)
        if score['score'].iloc[0] > 0.5:
            continue

        print('scrapping ', descStripped)
        try:
            sc.query(descStripped)
        except Exception as e:
            print(e)
        finally:
            time.sleep(2)
    



# # console print
# print("========Debits============")
# print("==========================")
# for debit in debits:
#     print('{0}: {1}===== {2}\n'.format(debit.date, debit.desc, debit.amount))
# print("\n")
# print("==========================")
# print("\n\n\n")

# print("========Credits============")
# print("==========================")
# for credit in credits:
#     print('{0}: {1}===== {2}\n'.format(credit.date, credit.desc, credit.amount))
# print("\n")
# print("==========================")