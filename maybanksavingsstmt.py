from itertools import cycle
import re
from abstsavingsanalyzer import AbstStmtSavingsAnalyzer

class MaybankSavingsStmt(AbstStmtSavingsAnalyzer):
    def findInflows(self):
        indexStart = re.search(r"[\d+/\d+/\d+]{8,10}",self.statement).start()
        substr = self.statement[indexStart:len(self.statement)-1]
        contents = substr.splitlines()
        print(substr)
        
    
    def findOutflows(self):
        return ''

    def getOpeningBalance(self):
        contents = self.statement.splitlines()
        licycle = cycle(contents)

        nextItem = next(licycle)

        running = True

        while(running):
            thisItem = nextItem
            if(thisItem == 'BEGINNING BALANCE'):
                return next(licycle)
            nextItem = next(licycle)
        

    