from transaction import Transaction
import random
from app_config import AppConfig

class History:
  """ History class """
  
  # list of transactions in the history
  transactions = []
  
  # çomplete schedule of all transaction data operations including commits/aborts 
  schedule = []

  def __init__(self):
    self.generate_transactions()
    self.make_schedule()

  def get_transaction_cardinality(self):
    # Return the number of transactions for the history
    return random.randint(
      AppConfig.get("transaction").get("min"), 
      AppConfig.get("transaction").get("max")
    )

  def get_transaction_data_cardinality(self):
    # Return the number of transaction data items for the history
    return random.randint(
      AppConfig.get("transaction_data").get("min"), 
      AppConfig.get("transaction_data").get("max")
    )

  def generate_data_item(self):
    # Return data item value
    return random.randint(
      AppConfig.get("data_item").get("min"), 
      AppConfig.get("data_item").get("max")
    )

  def generate_transactions(self):
    # Generate random number of transactions with data items
    transaction_cardinality = self.get_transaction_cardinality()
    tx_id_counter = 1
    
    while len(self.transactions) < transaction_cardinality:
      # make the random data items for the transaction
      tx_data_items = self.make_data_items_for_tx()
      self.transactions.append(Transaction(tx_id_counter, tx_data_items))
      tx_id_counter += 1

  def make_data_items_for_tx(self):
    # returns list of data_items
    data_items = []
    data_cardinality = self.get_transaction_data_cardinality()

    while len(data_items) < data_cardinality:
      data = self.generate_data_item()
      
      if data not in data_items:
        data_items.append(data)
    
    return data_items

  def pretty_print(self):
    for item in self.schedule:
      if item == self.schedule[-1]:
        print(item.pretty_format())
      else:
        print(item.pretty_format(), end=" --> ")
  
  def make_schedule(self):
    if len(self.transactions) == 0:
      raise ValueError('transactions must have length')

    ops = []

    self.schedule = []

    for tx in self.transactions:
      ops = ops + tx.data_operations

    random.shuffle(ops)
    
    while len(ops) > 0:
      op = ops.pop(0)

      if op.is_abort() or op.is_commit():
        # Require all other data operations for tx to be completed
        in_progress = any(op.transaction_id == item.transaction_id for item in ops)

        if in_progress:
          ops.append(op)
          random.shuffle(ops)
        else:
          self.schedule.append(op)  
      else:
        self.schedule.append(op)

