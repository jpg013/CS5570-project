from enum import Enum

class RecoverableValue(Enum):
  """Enum helper class to hold recoverable/aca/strict values for a given ReadFromRelationship"""
  IS_RECOVERABLE     = "IS_RECOVERABLE"
  IS_NOT_RECOVERABLE = "IS_NOT_RECOVERABLE"
  IS_ACA             = "IS_ACA"
  IS_NOT_ACA         = "IS_NOT_ACA"
  IS_STRICT          = "IS_STRICT"
  IS_NOT_STRICT      = "IS_NOT_STRICT"
  NOT_AVAILABLE      = "NOT_AVAILABLE"