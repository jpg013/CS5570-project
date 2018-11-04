import random
from data_operation import DataOperation

class Transaction:
    """ Transaction class takes a list of data_items and generates  
        a random list of data operations (read/write) for the data items,
        including a commit/abort operation. The Transaction class also exposes
        a make_generator method which will allow the program to iterate through
        each data_operation by calling next() until the tranasction ops are exhausted. 
    """
  
    def __init__(self, id):
        self.data_operations = []
        self.id = id

    def commit_type(self):
        commit_op = next(x for x in self.data_operations if x.is_abort() or x.is_commit() )
        return commit_op.operation_type

    def add_data_operation(self, data_operation):
        self.data_operations.append(data_operation)
        
    def pretty_print(self):
        prettyOps = ""
        for op in self.data_operations:
            prettyOps += op.format_pretty()
            op.pretty_print()
            if op is not self.data_operations[-1]:
                prettyOps += " --> "
                print(" --> ", end="")
            else:
                print("")
        return prettyOps

            
        
