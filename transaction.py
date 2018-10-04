import random
from enum import Enum

class Transaction:
  """ Transaction class """
  
  # Map of data_item to list of transactions
  tx_op_map = {}

  # List of randomly interleaved data operations for the transaction
  interleaved_data_operations = []
  
  # Stores the list of (1 - 4) data items for the transaction
  data_items = None

  # cursor variable for iterating through the interleaved data operations
  cursor = 0

  # Transaction ID
  transaction_id = None

  def __init__(self, id, data_items):
    if (type(data_items)) is not list:
      raise ValueError('data_items must be defined.')

    if len(data_items) < 1:
      raise ValueError('data_items list must have at least one item')

    self.transaction_id = id
    self.data_items = data_items
    self.build_transaction_operation_map()
    self.interleave_operations()
  
  def build_transaction_operation_map(self):
    if self.data_items is None:
      raise ValueError('data_items must be defined.')

    if len(self.data_items) < 1:
      raise ValueError('data_items list must have at least one item')
    
    for data_item in self.data_items:
      # init the map item

      self.tx_op_map[data_item] = []
       
      # Each data item may have 1 - 2 operations per transaction on it
      tx_op_count = random.randint(1, 2)
      
      if tx_op_count is 1:
        op_type = typeSwitcher.get(random.randint(0,1))
        self.tx_op_map[data_item].append(DataOperation(data_item, op_type, self.transaction_id))
      else:
        self.tx_op_map[data_item].append(DataOperation(data_item, OperationType.READ, self.transaction_id))
        self.tx_op_map[data_item].append(DataOperation(data_item, OperationType.WRITE, self.transaction_id))

  def get_tx_op_count(self):
    count = 0

    for key, value in self.tx_op_map.items():
      count += len(value)

    return count

  def flatten_tx_op_map(self):
    arr = []

    for key, value in self.tx_op_map.items():
      arr.append(value[:])

    return arr

  def interleave_operations(self):
    total_count = self.get_tx_op_count()
    interleaved_operations = []
    items = self.flatten_tx_op_map()
    
    while len(items) > 0:
      idx = random.randint(0, len(items) - 1)

      sub_item = items[idx]

      if len(sub_item) == 0:
        items.remove(sub_item)
        continue

      interleaved_operations.append(sub_item.pop(0))

    if len(interleaved_operations) != total_count:
      raise Exception('interleaved_operations length different than total count')

    # Append the TerminalOperation
    interleaved_operations.append(TerminalOperation(self.transaction_id))

    self.interleaved_data_operations = interleaved_operations

  def next(self):
    """ iterate the next data operation for the transaction. Will return None if iterator is finished """
    if self.is_finished():
      return None

    op = self.interleaved_data_operations[self.cursor]
    
    self.cursor += 1

    return op
    
  def is_finished(self):
   return self.cursor >= len(self.interleaved_data_operations)