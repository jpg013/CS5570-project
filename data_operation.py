from operation_type import OperationType
import uuid
import json

class DataOperation:
    """DataOperation class. It holds the operation_type enum,
    and a nullable data_item string. If the operation type is abort/commit it 
    does not operate on a data item."""

    data_item = None
  
    def __init__(self, transaction_id, operation_type, data_item=None):
        if not isinstance(transaction_id, int):
            raise ValueError('transaction_id must be of type integer')
        
        if not OperationType.has_value(operation_type):
            raise ValueError('operation_type must be of type OperationType.')

        if OperationType.has_value(operation_type) is False:
            raise ValueError('{} is not of enum type OperationType'.format(operation_type))
    
        self.operation_type = operation_type
        self.transaction_id = transaction_id

        # If operation type is Abort/Commit it will not have associated data item
        if data_item is not None:
            self.data_item = data_item
        
        # Generate a unique uuid for the operation. This is useful for hashing.
        self.id = uuid.uuid4()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id != other.id

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self.id != other.id)

    def is_abort(self):
        return self.operation_type == OperationType.ABORT

    def is_commit(self):
        return self.operation_type == OperationType.COMMIT

    def is_write(self):
        return self.operation_type == OperationType.WRITE
  
    def is_read(self):
        return self.operation_type == OperationType.READ

    def to_string(self):
        if self.operation_type is OperationType.READ:
            return 'read_{0}[{1}]'.format(self.transaction_id, self.data_item)
        elif self.operation_type is OperationType.WRITE:
            return 'write_{0}[{1}]'.format(self.transaction_id, self.data_item)
        elif self.operation_type is OperationType.ABORT:
            return 'abort_{0}'.format(self.transaction_id)
        elif self.operation_type is OperationType.COMMIT:
            return 'commit_{0}'.format(self.transaction_id)

    def to_json(self):
        json_dict = {
            'operation_type': self.operation_type.name,
            'transaction_id': self.transaction_id
        }

        if self.data_item is not None:
            json_dict['data_item'] = self.data_item

        return json.dumps(json_dict)