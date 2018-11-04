from transaction import Transaction
import random
from app_config import AppConfig
import sys

class History:
    """ History class """
  
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
        for item in self.schedule:
            item.pretty_print()

            if item is not self.schedule[-1]:
                print(" --> ", end="")
            else:
                print("")

    def format_pretty(self):
        format = ""
        
        for item in self.schedule:
            format += item.format_pretty()

            if item is not self.schedule[-1]:
                format +=  " --> "
            

        return format

    def randomize_schedule(self):
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

