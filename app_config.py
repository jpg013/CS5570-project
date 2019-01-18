default_tx_count = {
  "min": 1,
  "max": 4
}

default_data_set = set(["u", "x", "y", "z"])

class TransactionConfig:
  __config = {
    # Number of transactions per history
    "transaction_count": {
      "min": default_tx_count.min,
      "max": default_tx_count.max
    },
    # Set of allowed data items
    "data_set": default_data_set,
    "transaction_id_range": {
      "min": 1,
      "max": 1000,
    }
  }

  @staticmethod
  def get(name):
    return AppConfig.__config[name]

  @staticmethod
  def set(name, val):
    AppConfig.__config[name] = val

  @staticmethod
  def restore_defaults():
    AppConfig.__config['transaction_count'] = default_tx_count
    AppConfig.__config['data_set'] = default_data_set

