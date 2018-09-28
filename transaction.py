import random
from enum import Enum

class OperationType(Enum):
  READ   = 'READ'
  WRITE  = 'WRITE'
  COMMIT = 'COMMIT'
  ABORT  = 'ABORT'

typeSwitcher = {
  0: OperationType.READ,
  1: OperationType.WRITE,
  2: OperationType.COMMIT,
  3: OperationType.ABORT,  
} 

class DataOperation:
  """ DataOperation class holds two properties, data_item (Int) and and operation type (String). """
  
  # Stores data item that the operation acts on. It can be None if the Operation type is COMMIT or ABORT
  data_item = None

  # Stores the operation type, corresponds to the OperationType enum
  operation_type = None
  
  def __init__(self, data_item, operation_type):
    if data_item is None:
      raise ValueError('data_item must be defined.')

    if operation_type is None:
      raise ValueError('operation_type must be defined.')
    
    self.data_item = data_item
    self.operation_type = operation_type

class Transaction:
  """ Transaction class """
  
  # Stores the list of (1 - 2 / data items) operations (read/write) for the transaction
  transaction_operations = None
  
  # Stores the list of (1 - 4) data items for the transaction
  data_items = None

  def __init__(self, data_items):
    if (type(data_items)) is not list:
      raise ValueError('data_items must be defined.')

    if len(data_items) < 1:
      raise ValueError('data_items list must have at least one item')

    self.data_items = data_items
    self.transaction_operations = [] # set default
    self.build_data_operations()
  
  def build_data_operations(self):
    if self.data_items is None:
      raise ValueError('data_items must be defined.')

    if len(self.data_items) < 1:
      raise ValueError('data_items list must have at least one item')
    
    for data_item in self.data_items:
       # Each data item may have 1 - 2 operations per transaction on it
      tx_operation_count = random.randint(1, 2)
      
      if tx_operation_count is 1:
        self.transaction_operations.append(self.generate_random_read_write_op(data_item))
      else:
        self.transaction_operations.append(DataOperation(data_item, OperationType.READ))
        self.transaction_operations.append(DataOperation(data_item, OperationType.WRITE))

    # Add a commit or abort operation
    self.transaction_operations.append(self.generate_terminal_op)

  def generate_random_read_write_op(self, data_item):
    operation_type = typeSwitcher.get(random.randint(1,2))
    return DataOperation(data_item, operation_type)

  def generate_terminal_op(self, data_item):
    operation_type = typeSwitcher.get(random.randint(3,4))
    return DataOperation(data_item, operation_type)

   