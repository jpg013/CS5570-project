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

    def validate(self):
        """validates that the transaction passes the formal definition of a transaction:
        1) Ti is a superset of {ri[x], wi[x]} Union {ai, ci}
        2) ai is in Ti, iff ci is not in Ti
        3) if t is ci or ai, then for an other operation p in Ti, p <i t
        4) if ri[x], w[x] is in Ti, then either ri[x] < wi[x] or wi[x] < ri[x]
        Number 4 is given by virtue of how we are storing the data operations, i.e. the index
        of the data_operations array describes the ordering, so all data operations are automatically
        ordered. 
        """
                
        if len(self.data_operations) < 2:
            raise Exception('transaction must have at least one read/write data operation and one abort/commit operation')

        abort_or_commit_found = False
        
        for op in self.data_operations:
            if op.transaction.id is not self:
                raise Exception('transaction contains a data operation corresponding to different transaction')

            if op.is_abort() or op.is_commit():
                if abort_or_commit_found is True:
                    raise Exception('transaction contains multiple commits/aborts')
                
                abort_or_commit_found = True
                
                if self.data_operations[-1] is not op:
                    raise Exception('{0} is not the last data_operation for transaction'.format(op.operation_type.name))

        return True

    def add_data_operation(self, data_operation):
        self.data_operations.append(data_operation)
        
    def pretty_print(self):
        for op in self.data_operations:
            op.pretty_print()

            if op is not self.data_operations[-1]:
                print(" --> ", end="")
            else:
                print("")
        