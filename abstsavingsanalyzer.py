from abc import ABC, abstractmethod

class AbstStmtSavingsAnalyzer(ABC):

    def __init__(self, doc):
        self.doc = doc
        super().__init__()
        self.normalize()

    @abstractmethod
    def normalize(self):
        pass
        
    @abstractmethod
    def findInflows(self):
        pass

    @abstractmethod
    def findOutflows(self):
        pass

    @abstractmethod
    def getOpeningBalance(self):
        pass

        
        