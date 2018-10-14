import random
from data_operation import generate_read_writes_types, DataOperation, generate_commit_abort_type

class Transaction:
    """ Transaction class takes a list of data_items and generates  
        a random list of data operations (read/write) for the data items,
        including a commit/abort operation. The Transaction class also exposes
        a make_generator method which will allow the program to iterate through
        each data_operation by calling next() until the tranasction ops are exhausted. 
    """
  
    def __init__(self, id):
        self.data_operations = []
        self.transaction_id = id

    def commit_type(self):
        commit_op = next(x for x in self.data_operations if x.is_abort() or x.is_commit() )
        return commit_op.operation_type

    def set_data_operations(self, data_operations):
        self.data_operations = data_operations

    def generate_data_operations(self, data_items):
        if len(data_items) < 1:
            raise ValueError('data_items list must have at least one item')
        
        for item in data_items:
            # Generate random data Operations
            data_ops = list(map(lambda type: DataOperation(type, self.transaction_id, item, ), generate_read_writes_types()))
            self.data_operations = self.data_operations + data_ops
      
        
        # Randomly shuffle all the data operations.
        random.shuffle(self.data_operations)

        # Add a commit / abort data operation at the end
        self.data_operations.append(DataOperation(generate_commit_abort_type(), self.transaction_id, None))
        
    def pretty_print(self):
        for op in self.data_operations:
            op.pretty_print()

            if op is not self.data_operations[-1]:
                print(" --> ", end="")
            else:
                print("")
        