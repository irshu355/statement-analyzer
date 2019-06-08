import globals
from enums import Bank
from enums import Countries
from enum import Enum
class StatementPatterns():
    def __init__(self, bank):
        self.bank = bank
        pass

    def getShoppingPatterns(self):
        return{
           Bank.my_maybank: ['.*sales? debit.*'] 
        }.get(self.bank, Bank.my_maybank)

    def getUncategorizedPatterns(self):
        return{
           Bank.my_maybank: ['.*withdrawal.*',
           r'.*transfer\s.*',
            r'.*foreign\s.*',
           r'.*account transfer.*',
           r'^transfer.*','^ibk.*',
           r'.*pre(-|\s)?auth debit.*',
           r'.*atm card charges.*'
           ] 
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


    @staticmethod
    def getStates(country):
        return{
           Countries.malaysia: ['kuala lumpur','perlis','kedah','penang','perak','selangor','putrajaya','negeri sembilan','melaka',
           'johor','pahang','kelantan','terengganu','sabah','sarawak','labuan'] 
        }.get(country, Countries.malaysia)

    
    


    
