class AppConfig:
  __config = {
    # Number of transactions per history
    "transaction_count": {
      "min": 1,
      "max": 3
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