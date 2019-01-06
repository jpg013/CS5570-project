import random
from enum import Enum

class OperationType(Enum):
    READ   = "READ"
    WRITE  = "WRITE"
    COMMIT = "COMMIT"
    ABORT  = "ABORT"

    @classmethod
    def has_value(cls, value):
        return any(value == item for item in cls)

type_switcher = {
  0: OperationType.READ,
  1: OperationType.WRITE,
  2: OperationType.COMMIT,
  3: OperationType.ABORT,  
}