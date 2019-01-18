default_tx_count = {
  "min": 1,
  "max": 4
}

default_data_set = set(["u", "x", "y", "z"])

class TransactionConfig:
  __config = {
    # Number of transactions per history
    "transaction_count": {
      "min": default_tx_count['min'],
      "max": default_tx_count['max']
    },
    # Set of allowed data items
    "data_set": default_data_set
  }

  @staticmethod
  def get(name):
    return TransactionConfig.__config[name]

  @staticmethod
  def set(name, val):
    TransactionConfig.__config[name] = val

  @staticmethod
  def restore_defaults():
    TransactionConfig.__config['transaction_count'] = default_tx_count
    TransactionConfig.__config['data_set'] = default_data_set

