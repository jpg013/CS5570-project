from transaction import Transaction
import random
from app_config import AppConfig
import sys

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
        return self

    def print_pretty(self):
        """Helper method for pretty printing out the history schedule"""
        for item in self.schedule:
            item.print_pretty()

            if item is not self.schedule[-1]:
                print(" --> ", end="")
            else:
                print("")

    def format_pretty(self):
        """Same as print_pretty but returns a string and doesn't print to stdout"""
        format = ""
        
        for item in self.schedule:
            format += item.format_pretty()

            if item is not self.schedule[-1]:
                format +=  " --> "
            

        return format

    def serialize(self):
        return {
            'transactions': list(map(lambda x: x.serialize(), self.transactions)),
            'schedule': list(map(lambda x: x.serialize(), self.schedule)),
        }
        
    def interleave_transaction_schedule(self):
        """Create a schedule by interleaving the transaction data operations"""
        if len(self.transactions) == 0:
            raise ValueError('transactions must have length')

        ops = []

        for tx in self.transactions:
            ops = ops + tx.data_operations

        random.shuffle(ops)

        while len(ops) > 0:
            op = ops.pop(0)
      
            if op.is_abort() or op.is_commit():
                # Require all other data operations for tx to be completed
                in_progress = any(op.transaction is item.transaction for item in ops)

                if in_progress == False:
                    self.schedule.append(op)  
                else:
                    ops.append(op)
                    random.shuffle(ops)
            else:
                self.schedule.append(op)

