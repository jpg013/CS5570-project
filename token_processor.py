import re
from data_operation import OperationType, DataOperation
from transaction import Transaction
import collections

token_result_set = collections.namedtuple('TokenResultSet', ['transactions', 'data_operations'])

def parse_operation_type(op_char):
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
    
def parse_transaction_id(t=""):
    digits = re.findall(r'\d+', t)

    if len(digits) != 1:
        raise Exception('invalid token - {0}'.format(t))
    
    return int(digits[0])

def parse_data_item(t=""):
    data_items = re.findall(r'\((.*?)\)', t)
   
    if len(data_items) != 1:
        raise Exception('invalid token - {0}'.format(t))
    
    return data_items[0]
    
def create_transactions_from_input(input=''):
    """Take a string of inputs, splits them into terms and converts them to data operations 
    or throws an error if invalid"""
    
    # Example input "r1(x) w1(x) a1"
    tokens = input.split()
    data_operations = []
    transactions = []
    tx_ids = set()

    for t in tokens:
        if len(t) < 2:
            raise Exception('invalid token {0}'.format(t))
    
        operation_type = parse_operation_type(t[0])
        transaction_id = parse_transaction_id(t)
        tx_ids.add(transaction_id)
        data_item = None

        if (operation_type is OperationType.READ or operation_type is OperationType.WRITE):
            data_item = parse_data_item(t)
        
        data_operations.append(DataOperation(operation_type, transaction_id, data_item))

    for tx_id in tx_ids:
        tx = Transaction(tx_id)

        ops = list(filter(lambda x: x.transaction_id == tx_id, data_operations))
        tx.set_data_operations(ops)
        transactions.append(tx)

    return token_result_set(transactions, data_operations)
    





        
