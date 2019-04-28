import fitz
import re
import sys, json
from maybank.maybanksavingsstmt import MaybankSavingsStmt
from operator import itemgetter

doc = fitz.open('statement.pdf')

# Maybank statements:
maybankstmt = MaybankSavingsStmt(doc)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)
credits = maybankstmt.findOutflows()
debits = maybankstmt.findInflows()



# console print
print("========Debits============")
print("==========================")
for debit in debits:
    print('{0}: {1}===== {2}\n'.format(debit.date, debit.desc, debit.amount))
print("\n")
print("==========================")
print("\n\n\n")

print("========Credits============")
print("==========================")
for credit in credits:
    print('{0}: {1}===== {2}\n'.format(credit.date, credit.desc, credit.amount))
print("\n")
print("==========================")