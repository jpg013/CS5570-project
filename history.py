from transaction import Transaction
import random
from app_config import AppConfig
import sys

class History:
    """ History class """
  
    def __init__(self):
        # list of transactions in the history
        self.transactions = []
    
        # complete schedule of all transaction data operations including commits/aborts 
        self.schedule = []

    def set_transactions(self, transactions):
        self.transactions = transactions

    def get_transaction_cardinality(self):
        # Return the number of transactions for the history
        return random.randint(
            AppConfig.get("transaction_count").get("min"), 
            AppConfig.get("transaction_count").get("max")
        )

    def get_transaction_data_cardinality(self):
        # Return the number of transaction data items for the history
        return random.randint(1, len(AppConfig.get("data_set")))

    def generate_data_item(self):
        # Return data item value
        return random.sample(AppConfig.get("data_set"), 1)[0]

    def generate_transactions(self):
        # Generate random number of transactions with data items
        transaction_cardinality = self.get_transaction_cardinality()
    
        for idx in range(transaction_cardinality):
            tx_data_items = self.make_data_items_for_tx()
      
            tx = Transaction(idx+1)
            tx.generate_data_operations(tx_data_items)
      
            self.transactions.append(tx)

    def make_data_items_for_tx(self):
        # returns list of data_items
        data_items = []
        data_cardinality = self.get_transaction_data_cardinality()

        while len(data_items) < data_cardinality:
            data = self.generate_data_item()
      
            if data not in data_items:
                data_items.append(data)
    
        return data_items

    def pretty_print(self):
        for item in self.schedule:
            item.pretty_print()

            if item is not self.schedule[-1]:
                print(" --> ", end="")
            else:
                print("")
    
    def make_schedule(self):
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
                in_progress = any(op.transaction_id == item.transaction_id for item in ops)

                if in_progress == False:
                    self.schedule.append(op)  
                else:
                    ops.append(op)
                    random.shuffle(ops)
            else:
                self.schedule.append(op)

