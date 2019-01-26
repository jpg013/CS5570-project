transaction_cardinality = {
  "min": 1,
  "max": 4
}

data_set_cardinality = set(["u", "x", "y", "z"])

class TransactionConfig:
  __config = {
    # Number of transactions per history
    "transaction_cardinality": {
      "min": transaction_cardinality["min"],
      "max": transaction_cardinality["max"]
    },
    # Set of allowed data items
    "data_set_cardinality": data_set_cardinality
  }

  @staticmethod
  def get(name):
    return TransactionConfig.__config[name]

  @staticmethod
  def set(name, val):
    TransactionConfig.__config[name] = val

  @staticmethod
  def restore_defaults():
    TransactionConfig.__config['transaction_cardinality'] = transaction_cardinality
    TransactionConfig.__config['data_set_cardinality'] = data_set_cardinality

