from data_operation import DataOperation
from operation_type import OperationType, type_switcher
from app_config import TransactionConfig
from transaction import Transaction
import random

def make_data_read_operation(tx_id=None, data_item=None):
    if tx_id is None:
        tx_id = generate_transaction_id()
    
    if data_item is None:
        data_item = generate_data_item()

    return DataOperation(tx_id, OperationType.READ, data_item)

def make_data_write_operation(tx_id=None, data_item=None): 
    if tx_id is None:
        tx_id = generate_transaction_id()
    
    if data_item is None:
        data_item = generate_data_item()
    
    return DataOperation(tx_id, OperationType.WRITE, data_item)

def make_data_commit_operation(tx_id=None): 
    if tx_id is None:
        tx_id = get_transaction_id()
    
    return DataOperation(tx_id, OperationType.COMMIT)

def make_data_abort_operation(tx_id):
    if tx_id is None:
        tx_id = get_transaction_id()
    
    return DataOperation(tx_id, OperationType.ABORT)


# Helper method to randomly generate list of read/write data operations
def generate_read_or_writes_types(): 
    # Each data item may have a read, write, or both
    count = random.randint(1, 2)
    
    if count is 1:
        return [type_switcher.get(random.randint(0,1))]
    else:
        return [OperationType.READ, OperationType.WRITE]

def generate_commit_or_abort_type():
    return type_switcher.get(random.randint(2,3))

def generate_data_item():
    # Return random data item
    return random.sample(TransactionConfig.get("data_set_cardinality"), 1)[0]

def generate_data_set_cardinality():
    # Return random transaction data item cardinality
    return random.randint(1, len(TransactionConfig.get("data_set_cardinality")))

def get_transaction_cardinality():
    # Return transaction cardinality
    return random.randint(
        TransactionConfig.get("transaction_cardinality")["min"],
        TransactionConfig.get("transaction_cardinality")["max"]
    )

def generate_transaction_id():
    # Return transaction cardinality
    return random.randint(
        TransactionConfig.get("transaction_id_range")["min"],
        TransactionConfig.get("transaction_id_range")["max"]
    )

def generate_transaction_data_items():
        # s.remove(random.sample(s, 1)[0])
        data_set = set(TransactionConfig.get("data_set_cardinality"))
        data_items = []

        for i in range(generate_data_set_cardinality()):
            item = random.sample(data_set, 1)[0]
            data_set.remove(item)
            data_items.append(item)

        return data_items    

def generate_transaction(id=None):
    # Generates a transaction with random data operations
    tx = Transaction()
    data_items = generate_transaction_data_items()
    data_operations = []
        
    for item in data_items:
        # Generate random data Operations
        data_operations = data_operations + list(map(lambda t: DataOperation(tx.id, t, item), generate_read_or_writes_types()))

    # Randomly shuffle all the data operations.
    random.shuffle(data_operations)

    # Add a commit / abort data operation at the end
    data_operations.append(DataOperation(tx.id, generate_commit_or_abort_type()))

    for op in data_operations:
        tx.add_data_operation(op)
    
    return tx

def generate_history_transactions():
    return list(map(lambda i: generate_transaction() , range(get_transaction_cardinality()))) 