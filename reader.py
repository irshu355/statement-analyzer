import fitz
import re
import sys, json
from maybank.maybanksavingsstmt import MaybankSavingsStmt
from operator import itemgetter
import pandas
import time
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl
import globals
import utils
from csvwriter import CSVWriter
from scrapper import Scrapper 
doc = fitz.open('statement.pdf')
nltk.download('stopwords')
# Maybank statements:
maybankstmt = MaybankSavingsStmt(doc)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)
credits = maybankstmt.findOutflows()
debits = maybankstmt.findInflows()

csvWriter = CSVWriter()
csvWriter.write(credits)

sample = 'fpx payment fr 2349Dkj238 celcom planet sdn bh'
#MTUT2510TCH007


res = re.findall('(\S+\d+){1,}',sample)



df = pandas.DataFrame.from_records([c.to_dict() for c in credits])
# print(df.columns)
# print(df['amount'])
groupby_withdrawals = df.groupby(by=['desc'])
spending_avg = groupby_withdrawals.head()
# print(groupby_withdrawals.sum())
# print(groupby_withdrawals.count())

# cleanse

stop = stopwords.words('english') + ['via','transfer','*', 'a/c','account','tt','dr','a/','pymt']

# df['desc'] = df['desc'].apply(lambda x: x.lower())
df['desc'] = df['desc'].apply(lambda x: ' '.join([word for word in x.lower().split() if word not in (stop)]))
df['desc'] = df['desc'].apply(lambda x: re.sub(r'(\S+\d+){1,}','',x))


sc = Scrapper()
size = df.head().size
#17

# df = df.iloc[16:]

for row in df.itertuples():

    if utils.hasValue(globals.uncategorised_patterns,row[3]):
        print('write ', row[3])
        sc.writeToDs(row[3],"uncategorized",row[3])
    else:
        print('scrapping ', row[3])
        try:
            sc.query(row[3])
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)
    



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