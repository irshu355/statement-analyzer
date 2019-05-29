class Debit:
    amount = 0.00
    desc = 'transaction description'
    date = 'when'
    def __init__(self, amount, desc, date):
        self.amount = amount
        self.desc = desc
        self.date = date

    def to_dict(self):
        return {
        'amount': self.amount,
        'date': self.date,
        'desc': self.desc
    }

    
