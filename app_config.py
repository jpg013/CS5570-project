class AppConfig:
  __config = {
    "transaction": {
      "min": 1,
      "max": 2
    },
    "transaction_data": {
      "min": 1,
      "max": 4
    },
    "data_item": {
      "min": 1,
      "max": 4
    }
  }

  @staticmethod
  def get(name):
    return AppConfig.__config[name]