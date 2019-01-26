from data_operation import DataOperation
from operation_type import OperationType
from app_config import TransactionConfig
import random

def make_data_read_operation(tx_id=None, data_item=None):
    if tx_id is None:
        tx_id = get_transaction_cardinality()
    
    if data_item is None:
        data_item = get_data_set_cardinality()

    return DataOperation(tx_id, OperationType.READ, data_item)

def make_data_write_operation(tx_id=None, data_item=None): 
    if tx_id is None:
        tx_id = get_transaction_cardinality()
    
    if data_item is None:
        data_item = get_data_set_cardinality()
    
    return DataOperation(tx_id, OperationType.WRITE, data_item)

def make_data_commit_operation(tx_id=None): 
    if tx_id is None:
        tx_id = get_transaction_cardinality()
    
    return DataOperation(tx_id, OperationType.COMMIT)

def make_data_abort_operation(tx_id):
    if tx_id is None:
        tx_id = get_transaction_cardinality()
    
    return DataOperation(tx_id, OperationType.ABORT)

def get_data_set_cardinality():
    # Return data item value
    return random.sample(TransactionConfig.get("data_set_cardinality"), 1)[0]

def get_transaction_cardinality():
    # Return transaction
    return random.randint(
        TransactionConfig.get("transaction_cardinality")["min"],
        TransactionConfig.get("transaction_cardinality")["max"]
    )
