import re
from data_operation import DataOperation
from operation_type import OperationType
from transaction import Transaction
from history import History

class HistoryQueryBuilder:
    """HistoryQueryBuilder is responsible for string query inputs of data operation and producing 
    valid histories if query is semantically correct, or producing an error if not."""

    def __init__(self, query):
        if not isinstance(query, str):
            raise Exception('query argument must be a string.')

        self.query = query
        self.error = None
        
        self.parse_query()
        
    def parse_query(self):
        """Parses query into tokens based on separated white space.
        Example query "r1[x] w1[x] a1" would be split into ['r1[x]', 'w1[x]', 'a1']
        """
    
        self.tokens = self.query.split()

    def build(self):
        data_operations = []
        transaction_dict = {}

        for t in self.tokens:
            if len(t) < 2:
                raise Exception('invalid token {0}'.format(t))
        
            operation_type = self.parse_operation_type(t)
            transaction_id = self.parse_transaction_id(t)

            data_item = None

            if (operation_type is OperationType.READ or operation_type is OperationType.WRITE):
                data_item = self.parse_data_item(t)
            
            if transaction_id not in transaction_dict:
                transaction_dict[transaction_id] = Transaction(transaction_id)
            
            tx = transaction_dict[transaction_id]

            data_operation = DataOperation(operation_type, tx.id, data_item)
            data_operations.append(data_operation)
            tx.add_data_operation(data_operation)

        hist = History(transaction_dict.values())
        hist.set_schedule(data_operations)

        return hist

    def parse_operation_type(self, token=''):
        op_char = token[0]
        
        if op_char == 'r':
            return OperationType.READ
        elif op_char == 'w':
            return OperationType.WRITE
        elif op_char == 'a':
            return OperationType.ABORT
        elif op_char == 'c':
            return OperationType.COMMIT
        else:
            raise Exception('invalid operation type character {0}'.format(op_char))
    
    def parse_transaction_id(self, t=''):
        digits = re.findall(r'\d+', t)

        if len(digits) != 1:
            raise Exception('invalid token - {0}'.format(t))
        
        return int(digits[0])

    def parse_data_item(self, t=''):
        data_items = re.findall(r'\[(.*?)\]|\((.*?)\)/g', t)
    
        if len(data_items) != 1:
            raise Exception('invalid token - {0}'.format(t))

        data_item = data_items[0][0]

        return data_item
        