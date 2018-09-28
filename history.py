from transaction import Transaction
import random
from app_config import AppConfig

class History:
  """ History class """
  
  # list of transactions in the history
  transactions = []
  
  # complete history of all transaction data operations including their commit/abort operations
  complete_history = []

  def __init__(self):
    self.generate_transactions()
    self.interleave_transaction_history()

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

    if transaction_cardinality < AppConfig.get("transaction").get("min") or transaction_cardinality > AppConfig.get("transaction").get("max"):
      raise ValueError('invalid transaction_cardinality value')

    while len(self.transactions) < transaction_cardinality:
      # make the random data items for the transaction
      tx_data_items = self.make_data_items_for_tx()
      tx_id = random.randint(1, 1000)
      self.transactions.append(Transaction(tx_id, tx_data_items))
      

  def make_data_items_for_tx(self):
    # returns list of data_items
    data_items = []
    data_cardinality = self.get_transaction_data_cardinality()

    if data_cardinality < AppConfig.get("transaction_data").get("min") or data_cardinality > AppConfig.get("transaction_data").get("max"):
      raise ValueError('invalid data_cardinality value')
    
    while len(data_items) < data_cardinality:
      data = self.generate_data_item()
      
      if data not in data_items:
        data_items.append(data)
    
    return data_items

  def prune_history_transactions(self, history_transactions):
    return list(filter(lambda tx: tx.is_finished() == False, history_transactions))

  def get_next_transaction_operation(self, history_transactions):
    next_op = None
    
    curr = random.randint(0, len(history_transactions) - 1)
    tx = history_transactions[curr]

    return tx.next()

  def interleave_transaction_history(self):
    if len(self.transactions) == 0:
      raise ValueError('transactions must have length')

    history_transactions = self.transactions[:]
    while len(history_transactions) > 0:
      op = self.get_next_transaction_operation(history_transactions)

      if op is None:
        raise ValueError('invalid transaction operation')
      
      self.complete_history.append(op)
      history_transactions = self.prune_history_transactions(history_transactions)



   