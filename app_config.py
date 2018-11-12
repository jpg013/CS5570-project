default_tx_count = {
  "min": 1,
  "max": 4
}

default_data_set = set(["u", "x", "y", "z"])

class AppConfig:
  __config = {
    # Number of transactions per history
    "transaction_count": {
      "min": 1,
      "max": 4
    },
    # Set of allowed data items
    "data_set": set(["u", "x", "y", "z"])
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
