import random
from enum import Enum

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
  
  def __init__(self, operation_type, transaction, data_item=None):
    if operation_type is None:
      raise ValueError('operation_type must be defined.')

    if transaction is None:
      raise ValueError('transaction must be defined.')

    if OperationType.has_value(operation_type) is False:
      raise ValueError('{} is not of enum type OperationType'.format(operation_type))
    
    self.operation_type = operation_type
    self.transaction = transaction

    # If operation type is Abort/Commit it will not have associated data item
    self.data_item = data_item

  def __hash__(self):
        return hash(str(self.transaction.id) + ':' + str(self.operation_type) + ':' + str(self.data_item))

  def __eq__(self, other):
      return (
          (self.operation_type == other.operation_type) and
          (self.transaction is other.transaction) and
          (self.data_item is other.data_item)
      )

  def __ne__(self, other):
      # Not strictly necessary, but to avoid having both x==y and x!=y
      # True at the same time
      return not(self == other)

  def is_abort(self):
      return self.operation_type == OperationType.ABORT

  def is_commit(self):
      return self.operation_type == OperationType.COMMIT

  def is_write(self):
      return self.operation_type == OperationType.WRITE
  
  def is_read(self):
      return self.operation_type == OperationType.READ

  def format_pretty(self):
      formatted_item = ""
  
      if self.operation_type == OperationType.READ:
          formatted_item += "read_" + str(self.transaction.id) + "_[" + str(self.data_item) + "]"
      elif self.operation_type == OperationType.WRITE:
          formatted_item += "write_" + str(self.transaction.id) + "_[" + str(self.data_item) + "]"
      elif self.operation_type == OperationType.ABORT:
          formatted_item += "abort_" + str(self.transaction.id)
      elif self.operation_type == OperationType.COMMIT:
          formatted_item += "commit_" + str(self.transaction.id)
      
      return formatted_item

  def pretty_print(self):
    print(self.format_pretty(), end="")