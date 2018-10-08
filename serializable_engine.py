from serialization_graph import SerializationGraph

class SerializableEngine:
  """ SerializableEngine class """

  def __init__(self, history):
    if history is None:
      raise ValueError("History must be defined.")
    
    self.history = history
    self.serialization_graph = SerializationGraph(self.history)

  
    

