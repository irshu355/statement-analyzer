import csv
import re

class CSVWriter():
    def __init__(self):
        self.entertainment_patterns = [
            '.*cinem.*',
            '.*gsc.*',
            '.*movie.*',
            '.*tgv.*',
            '.*video.*',
            '.*show.*',
            '.*music.*',
            '.*song.*',
            '.*concert.*',
            '.*film.*',
            '.*media.*',
            '.*gaming.*',
            '.*multiplay.*',
        ]
        self.shopping_patterns = [
            '.*gpay.*',
            '.*sale.*'
        ]

        self.travel_tourism_patterns = [
            '.*airasia.*',
            '.*airlines.*'
        ]

        self.uncategorised_patterns = [
            '.*withdraw.*',
            '.*transfer.*'
        ]
        self.utilities_patterns = [
            '.*celcom.*',
            '.*maxis.*',
            '.*umobile.*',
            '.*digi.*'
        ]

        self.food_dining_patterns = [
            '.*cafe.*'
        ]
        

    

    def write(self,debits):
        with open('spendings.csv', mode='w') as spendings_file:
            spendings_writer = csv.writer(spendings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for debit in debits:
                category = ''
                if re.search("(" + ")|(".join(self.entertainment_patterns) + ")",debit.desc.lower()):
                    category = 'entertainment'
                elif re.search("(" + ")|(".join(self.shopping_patterns) + ")",debit.desc.lower()):
                    category = 'shopping'
                elif re.search("(" + ")|(".join(self.uncategorised_patterns) + ")",debit.desc.lower()):
                    category = 'uncategorised'
                elif re.search("(" + ")|(".join(self.utilities_patterns) + ")",debit.desc.lower()):
                    category = 'utilities'
                elif re.search("(" + ")|(".join(self.food_dining_patterns) + ")",debit.desc.lower()):
                    category = 'food_dining'
                elif re.search("(" + ")|(".join(self.travel_tourism_patterns) + ")",debit.desc.lower()):
                    category = 'food_dining'


                if not category:
                    spendings_writer.writerow([debit.desc, debit.amount])
                else:
                    spendings_writer.writerow([debit.desc, debit.amount,category])
        
        print('done write')