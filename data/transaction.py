import random
from data_operation import DataOperation
import json

class Transaction:
    """ Transaction class represents the main component model in concurrency control. It contains a list 
    of data_items and a unique integer id. The data_items contained are a sequence of reads/writes and the 
    last data item must always be either the commit or abort operation. """
  
    def __init__(self, id):
        self.data_operations = []
        
        if not isinstance(id, int):
            raise ValueError('id must be of type int')

        self.id = id

    def commit_type(self):
        """Returns the operation_type for the transaction commit/abort operatoin"""
        commit_op = next(x for x in self.data_operations if x.is_abort() or x.is_commit() )
        return commit_op.operation_type if commit_op is not None else None

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
        """Helper method to append a data operation to the transaction operation list."""
        self.data_operations.append(data_operation)
        
    def to_string(self):
        """Helper method for printing out the transaction to stdout""" 
        str_val = 'T{0}'.format(self.id)
        
        for op in self.data_operations:
            str_val += op.to_string()

            if op is not self.data_operations[-1]:
                str_val += ' --> '
                
        return str_val

    def to_json(self):
        json_dict = {
            'id': self.id,
            'data_operations': list(map(lambda x: x.to_json(), self.data_operations)),
        }

        return json.dumps(json_dict)
    
        
