from transaction import Transaction
import random

class History:
    """History class as defined in concurrency control and recovery. A complete history is a sequence of interleaved 
    transactions. The given history class can be implemented in two ways. By instantiating with a list of transactions and 
    calling interleave_transaction_schedule() to randomly interleave the transaction data_operations, or by manually setting the
    transaction schedule with set_schedule."""
  
    def __init__(self, transactions=None):
        if transactions is None:
            raise Exception('history transactions must be defined')
        
        # list of transactions in the history
        self.transactions = transactions
    
        # complete schedule of all transaction data operations including commits/aborts 
        self.schedule = []

    def set_schedule(self, schedule):
        """Manually set the history schedule"""
        self.schedule = schedule

    def to_string(self):
        """Same as print_pretty but returns a string and doesn't print to stdout"""
        str_val = ""
        
        for item in self.schedule:
            str_val += item.to_string()

            if item is not self.schedule[-1]:
                str_val +=  " --> "

        return str_val

    def to_json(self):
        return {
            'transactions': list(map(lambda x: x.to_json(), self.transactions)),
            'schedule': list(map(lambda x: x.to_json(), self.schedule)),
        }
        
    def interleave_transaction_schedule(self):
        """Create a schedule by interleaving the transaction data operations"""
        if len(self.transactions) == 0:
            raise ValueError('transactions must have length')

        generators = []

        for tx in self.transactions:
            generators.append(tx.new_generator())

        # Shuffle randomly
        random.shuffle(generators)

        more = lambda: any(not g.is_exhausted() for g in generators)
        next = lambda: random.choice(list(filter(lambda x: not x.is_exhausted(), generators))).next()
        
        self.schedule = []

        while(more()):
            self.schedule.append(next())