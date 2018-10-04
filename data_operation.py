class OperationType(Enum):
  READ   = "READ"
  WRITE  = "WRITE"
  COMMIT = "COMMIT"
  ABORT  = "ABORT"

  @classmethod
  def has_value(cls, value):
    return any(value == item for item in cls)

type_switcher = {
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

  # Stores the transaction id
  transaction_id = None
  
  def __init__(self, operation_type, transaction_id, data_item):
    if operation_type is None:
      raise ValueError('operation_type must be defined.')

    if transaction_id is None:
      raise ValueError('transaction_id must be defined.')

    if OperationType.has_value(operation_type) is False:
      raise ValueError('{} is not of enum type OperationType'.format(operation_type))
    
    self.operation_type = operation_type
    self.transaction_id = transaction_id

    if data_item is not None:
      self.data_item = data_item

  def pretty_format(self):
    formatted_item = ""
  
    if self.operation_type == OperationType.READ:
      formatted_item += "read_" + str(self.transaction_id) + "_[" + str(self.data_item) + "]"
    elif self.operation_type == OperationType.WRITE:
      formatted_item += "write_" + str(self.transaction_id) + "_[" + str(self.data_item) + "]"
    elif self.operation_type == OperationType.ABORT:
      formatted_item += "abort_" + str(self.transaction_id)
    elif self.operation_type == OperationType.COMMIT:
      formatted_item += "commit_" + str(self.transaction_id)

    return formatted_item  
