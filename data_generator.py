from data_operation import DataOperation
from operation_type import OperationType
from app_config import TransactionConfig
import random

def make_data_read_operation():
    return DataOperation(OperationType.READ, make_data_item())


def make_data_write_operation(): 
    return DataOperation(OperationType.WRITE, make_data_item())


def make_data_commit_operation(): 
    return DataOperation(OperationType.COMMIT)


def make_data_abort_operation():
    return DataOperation(OperationType.ABORT)


def make_data_item():
    # Return data item value
    return random.sample(TransactionConfig.get('data_set'), 1)[0]