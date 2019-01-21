import random
from app_config import AppConfig
import sys
from transaction import Transaction
from data_operation import DataOperation, type_switcher, OperationType

class DataGeneration():
    """DataGeneration is a helper class with several utility methods 
    for generating random data sets for transactions and data operations"""

    def __init__(self):
        self.transaction_count = AppConfig.get('transaction_count')
        self.data_set = AppConfig.get('data_set')
        
    def get_transaction_data_cardinality(self):
        # Return the number of transaction data items for the history
        return random.randint(1, len(self.data_set))

    def generate_data_item(self):
        # Return data item value
        return random.sample(self.data_set, 1)[0]

    def make_transaction_data_sample(self):
        # returns list of data_items
        data_sample = []
        data_cardinality = self.get_transaction_data_cardinality()

        while len(data_sample) < data_cardinality:
            data = self.generate_data_item()
        
            if data not in data_sample:
                data_sample.append(data)

        return data_sample

    def generate_transactions(self):
        # Generate random number of transactions with data items
        transaction_cardinality = self.get_transaction_cardinality()
        transactions = []
        
        for idx in range(transaction_cardinality):
            tx = Transaction(idx+1)
            
            for x in self.generate_tx_data_operations(tx, self.make_transaction_data_sample()):
                tx.add_data_operation(x)
        
            transactions.append(tx)

        return transactions

    def get_transaction_cardinality(self):
        # Return the number of transactions for the history
        return random.randint(
            self.transaction_count.get("min"), 
            self.transaction_count.get("max")
        )

    def generate_tx_data_operations(self, transaction, data_items):
        if len(data_items) < 1:
            raise ValueError('data_items list must have at least one item')

        data_operations = []
        
        for item in data_items:
            # Generate random data Operations
            data_operations = data_operations + list(map(lambda type: DataOperation(type, transaction, item), self.generate_read_writes_types()))
        
        # Randomly shuffle all the data operations.
        random.shuffle(data_operations)

        # Add a commit / abort data operation at the end
        data_operations.append(DataOperation(self.generate_commit_abort_type(), transaction, None))

        return data_operations    

    # Helper method to randomly generate list of read/write data operations
    def generate_read_writes_types(self): 
        # Each data item may have a read, write, or both
        count = random.randint(1, 2)
        
        if count is 1:
            return [type_switcher.get(random.randint(0,1))]
        else:
            return [OperationType.READ, OperationType.WRITE]

    def generate_commit_abort_type(self):
        return type_switcher.get(random.randint(2,3))