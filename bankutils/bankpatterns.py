import globals
from banks import Bank
from enum import Enum
class BankPatterns():
    def __init__(self, bank):
        self.bank = bank
        pass

    def getShoppingPatterns(self):
        return{
           Bank.my_maybank: ['.*sales? debit.*'] 
        }.get(self.bank, Bank.my_maybank)

    def getUncategorizedPatterns(self):
        return{
           Bank.my_maybank: ['.*withdrawal.*','.*transfer a/c.*','.*account transfer.*','^transfer.*','^ibk.*'] 
        }.get(self.bank, Bank.my_maybank)


    def getUtilitiesPatterns(self):
        return{
           Bank.my_maybank: ['.*umobile.*','.*digi.*','.*maxis.*'] 
        }.get(self.bank, Bank.my_maybank)

    def getStopWords(self):
        return{
            Bank.my_maybank: self.getGlobalStopWords() + ['mydebit','fpx','payment via','fr', 'tt','dr','pymt', 'a/c','a/|/'] #/|/ is for /
        }.get(self.bank, Bank.my_maybank)
    def getGlobalStopWords(self):
        return ['pymt from','pa?ym(en)?t','pymt','via']

    
    


    
