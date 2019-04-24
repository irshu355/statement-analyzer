from abc import ABC, abstractmethod

class AbstStmtSavingsAnalyzer(ABC):

    def __init__(self, statement):
        self.statement = statement
        super().__init__()


    @abstractmethod
    def findInflows(self):
        pass

    @abstractmethod
    def findOutflows(self):
        pass

    @abstractmethod
    def getOpeningBalance(self):
        pass

        
        