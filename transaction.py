import random
from data_operation import generate_read_writes_types, DataOperation, generate_commit_abort_type

class Transaction:
  """ Transaction class takes a list of data_items and generates  
      a random list of data operations (read/write) for the data items,
      including a commit/abort operation. The Transaction class also exposes
      a make_generator method which will allow the program to iterate through
      each data_operation by calling next() until the tranasction ops are exhausted. 
  """
  
  data_operations = []

  # Stores the list of data items for the transaction
  data_items = None

  # Transaction ID
  transaction_id = None

  def __init__(self, id, data_items):
    if (type(data_items)) is not list:
      raise ValueError('data_items must be defined.')

    if len(data_items) < 1:
      raise ValueError('data_items list must have at least one item')

    self.transaction_id = id
    self.data_items = data_items
    self.make_data_operations(data_items)

  def make_data_operations(self, data_items):
    for item in data_items:
      # Generate random data Operations
      
      data_ops = list(map(lambda type: DataOperation(type, self.transaction_id, item, ), generate_read_writes_types()))

      self.data_operations = self.data_operations + data_ops
      
    # Randomly shuffle all the data operations.
    random.shuffle(self.data_operations)

    # Add a commit / abort data operation at the end
    self.data_operations.append(DataOperation(generate_commit_abort_type(), self.transaction_id, None))