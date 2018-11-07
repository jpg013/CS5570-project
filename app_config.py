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