import fitz
import re
import sys, json
from maybanksavingsstmt import MaybankSavingsStmt
from operator import itemgetter

beginning_balance = 'BEGINNING BALANCE'

doc = fitz.open('statement.pdf')

content = ""

for page in doc:
    pageContent=page.getText()
    pageContent =re.sub(r"^URUSNIAGA.*[\s\S+]+STATEMENT BALANCE",'',pageContent)
    pageContent = re.sub(r"Maybank Islamic Berhad.*[\s\S+]+Please notify us of any change of address in writing.",'',pageContent)
    content+=pageContent

print(content)



# f=open("page0.txt","w+")
# f.write(content)

# Maybank statements:


maybankstmt = MaybankSavingsStmt(content)
openingBalance = maybankstmt.getOpeningBalance()
print('opening balance: ',openingBalance)

maybankstmt.findInflows()





# txt = "The rain in Spain for some time"
# x = re.search("^The.*spain", txt)

# if (x):
#   print("YES! We have a match!")
# else:
#   print("No match")



