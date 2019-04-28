from itertools import cycle
import re
from abstsavingsanalyzer import AbstStmtSavingsAnalyzer
from models.debit import *
from models.credit import *
from decimal import Decimal

class MaybankSavingsStmt(AbstStmtSavingsAnalyzer):
    regexddMMyyyy= r"^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{2}$"
    #
    # normalize text to remove unwanted texts
    #

    def normalize(self):
        content = ""
        for page in self.doc:
            pageContent=page.getText()
            pageContent =re.sub(r"^URUSNIAGA.*[\s\S+]+STATEMENT BALANCE",'',pageContent)
            pageContent = re.sub(r"Maybank Islamic Berhad.*[\s\S+]+Please notify us of any change of address in writing.",'',pageContent)
            content+=pageContent
        self.pdfContent = content
    
        
    def matchesAmount(self, str):
        #1.00, 100.00, 1,000.00, 10,000.00 1,000,000.00
        regex = r'^((\d){1,3},*){1,5}\.(\d){2}(\+|-)$'
            # /. is used to match literal period
        if re.match(regex, str):
            return True 
        return False

    def isDebit(self, str):
        #1.00, 100.00, 1,000.00, 10,000.00 1,000,000.00
        regex = r'^((\d){1,3},*){1,5}\.(\d){2}(\+|-)$'
        if re.match(regex, str):
            if(str[-1]=='+'):
                return False
            return True
        return False

    def __findNextDateIndexPattern(self,i, contents):
        contents = contents[i:]
        j = 1
        while j < len(contents):
            contents[j] =contents[j].strip()
            date = contents[j]
            if re.match(self.regexddMMyyyy,contents[j]) or re.match(r"^ending balance*",contents[j],flags=re.IGNORECASE):
                break
            j+=1
        contents = contents[:j]

        j = 0
        while j < len(contents):
            if j != len(contents)-2 and self.matchesAmount(contents[j]):
                contents.append(contents.pop(j))
                contents.append(contents.pop(j))
                break
            j+=1

        
        _amount = contents[-2]
        amount = Decimal(_amount[:-1].replace(',',''))
        desc = ''
        date = contents[0]
        contents = contents[1:]


        for _ in range(len(contents)-2):
            desc+=contents[_]

        if self.isDebit(contents[-2]): 
            return Debit(amount,desc, date)
        else:
            return Credit(amount,desc, date)
        



    def __setPointerToRecordStart(self):
        indexStart = re.search(r"[\d+/\d+/\d+]{8,10}",self.pdfContent).start()
        substr = self.pdfContent[indexStart:len(self.pdfContent)-1]
        contents = substr.splitlines()
        return contents


    def grabTransactions(self,type):
        contents = self.__setPointerToRecordStart()
        i = 0
        trans = []
        while i < len(contents):
            if re.match(self.regexddMMyyyy,contents[i]):
                debit = self.__findNextDateIndexPattern(i,contents)
                if isinstance(debit, Debit if type == 'debits' else Credit):
                    trans.append(debit)
            i+=1
        return trans


    def findInflows(self):
        return self.grabTransactions("credits")

    def findOutflows(self):
       return self.grabTransactions("debits")


    def getOpeningBalance(self):
        contents = self.pdfContent.splitlines()
        licycle = cycle(contents)

        nextItem = next(licycle)

        running = True

        while(running):
            thisItem = nextItem
            if(thisItem == 'BEGINNING BALANCE'):
                return next(licycle)
            nextItem = next(licycle)
