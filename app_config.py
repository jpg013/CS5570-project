class AppConfig:
  __config = {
    # Number of transactions per history
    "transaction_count": {
      "min": 1,
      "max": 4
    },
    # Number of data_items per transaction
    "transaction_data_count": {
      "min": 1,
      "max": 4
    },
    # Set of allowed data items
    "data_set": set(["w", "x", "y", "z"])
  }

  @staticmethod
  def get(name):
    return AppConfig.__config[name]