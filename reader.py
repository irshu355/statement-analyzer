import fitz
import re
import sys, json
from maybank.maybanksavingsstmt import MaybankSavingsStmt
from operator import itemgetter

doc = fitz.open('statement.pdf')

# f=open("page0.txt","w+")
# f.write(content)

# Maybank statements:


maybankstmt = MaybankSavingsStmt(doc)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)

debits = maybankstmt.findOutflows()
credits = maybankstmt.findInflows()







# txt = "The rain in Spain for some time"
# x = re.search("^The.*spain", txt)

# if (x):
#   print("YES! We have a match!")
# else:
#   print("No match")



