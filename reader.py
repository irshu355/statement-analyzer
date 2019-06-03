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
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl
import globals
from bankutils import utils
from csvwriter import CSVWriter
from scrapper import Scrapper
from banks import Bank
from bankutils.bankpatterns import BankPatterns
doc = fitz.open('statement2.pdf')
nltk.download('stopwords')
# Maybank statements:
maybankstmt = MaybankSavingsStmt(doc)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)
credits = maybankstmt.findOutflows()
debits = maybankstmt.findInflows()
bank  = Bank.my_maybank
csvWriter = CSVWriter()
csvWriter.write(credits)

sample = 'fpx payment fr 2349Dkj238 celcom planet sdn bh'
#MTUT2510TCH007


res = re.findall('(\S+\d+){1,}',sample)


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
bankPatterns = BankPatterns(bank)
size = df.head().size

#17

# df = df.iloc[16:]
stop_words = stopwords.words('english') + ['via','*', 'tt','dr','a/','pymt', 'a/c']
txn_names = dfDataset['txn']
vectorizer = TfidfVectorizer(min_df=1, stop_words= stop_words)
tf_idf_matrix = vectorizer.fit_transform(txn_names)


cacheDesc = set()
txn_list = dfDataset["txn"].values
s = pandas.Series(txn_list)


for row in df.itertuples():
    desc = row[3].lower()

    filters = bankPatterns.getStopWords()
    for i in range(len(filters)):

        fltr = filters[i]
        fltr = r"\b"+fltr+r"\b"
        desc = re.sub(fltr,'',desc)

    # descStripped = ' '.join([word for word in desc.split() if word not in (stop)])
    descStripped = desc
    descStripped = re.sub(r'\W+', ' ', descStripped)
    descStripped = descStripped.strip()

    if descStripped in cacheDesc:
        continue
    if descStripped in s.to_list():
        continue

    cacheDesc.add(descStripped)
    if utils.hasValue(bankPatterns.getUncategorizedPatterns(),descStripped):
        print('write ', desc)
        sc.writeToDs(desc,"uncategorized fund transfer",descStripped)
    elif utils.hasValue(bankPatterns.getShoppingPatterns(),descStripped):
        print('write ', descStripped)
        sc.writeToDs(desc,"shopping online shopping purchase",descStripped)
    elif utils.hasValue(bankPatterns.getUtilitiesPatterns(),descStripped):
        print('write ', descStripped)
        sc.writeToDs(desc,"utilities phone bills bills",descStripped)
    else:
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