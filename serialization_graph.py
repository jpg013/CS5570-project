from data_operation import OperationType

class SerializationGraphNode:
  """ SerializationGraphNode """
  node_id = None
  
  def __init__(self, id=None):
    if id is None:
      raise ValueError("SerializationGraphNode requires a valid id")
    
    self.node_id = id

class SerializationGraphLink:
  """ 
      SerializationGraphLink has two properties, node_a, and node_b. Node_b depends on
      node_a (is a functional dependency as defined in class) meaning that one or more 
      operations in node_b are functionally dependent on 1 or more operations in node_a.
      For the link to be valid, both of these properties must be defined, and *cannot* 
      reference the same node
  """
  
  node_a = None
  node_b = None

  def __init__(self, node_a=None, node_b=None):
    if node_a is None or node_b is None:
      raise ValueError('SerializationGraphEdge requires two valid SerializationGraphNodes')
    
    if node_a is node_b:
      raise ValueError('SerializationGraphEdge requires two unique SerializationGraphNodes')

    self.node_a = node_a
    self.node_b = node_b

class SerializationGraph:
  """ 
      SerializationGraph builds a graph of nodes/edges from the transactions of a given history
  """

  # List holding the serialization graph nodes for a given history
  sg_nodes = []

  # List holding the serialization graph edges for a given history
  sg_edges = []

 # List holding the sg cycles in the form  
  cyles = []

  def __init__(self, history=None):
    if history is None:
      raise ValueError("history must be defined.")
    
    self.init_graph_nodes(history)
    self.build_graph_edges(history)
    self.pretty_print()
    #self.walk_edges_to_find_cycles()

  def pretty_print(self):
   for edge in self.sg_edges:
    print(f'Transaction{edge.node_a.node_id} --> Transaction{edge.node_b.node_id}')
  
  def walk_edges_to_find_cycles(self):
   print('hi')
   #for egde in self.sg_edges:
    #for x in self.

  def is_cycle(self, edge_a, edge_b):
   return edge_a.node_a

  def init_graph_nodes(self, history):
    for tx in history.transactions:
      self.sg_nodes.append(SerializationGraphNode(tx.transaction_id))

  def get_node(self, id): 
    return next(x for x in self.sg_nodes if x.node_id is id)

  def build_graph_edges(self, history):
    schedule = history.schedule[0:]
    
    for idx, val in enumerate(schedule):
      curr_node = self.get_node(val.transaction_id)

      if curr_node is None:
        raise Exception("Undefined sg_node for data operation")

      # Check for functional dependencies
      dependency = self.find_functional_dependency(val, schedule[idx+1:])

      if dependency is None:
        continue

      dep_node = self.get_node(dependency.transaction_id)

      # Create a graph edge
      self.sg_edges.append(SerializationGraphLink(curr_node, dep_node))

  def find_functional_dependency(self, data_operation, schedule):
    if len(schedule) is 0:
      return

    for val in schedule:
      # Can't conflict with operations in same transaction
      if val.transaction_id is data_operation.transaction_id:
        continue

      # Don't care about commits or aborts
      if val.operation_type is OperationType.COMMIT or val.operation_type is OperationType.ABORT:
        continue

      # read/read do not conflict
      if val.operation_type is OperationType.READ and data_operation.operation_type is OperationType.READ:
        continue

      # Cannot have functional dependency on different data items
      if val.data_item is not data_operation.data_item:
        continue

      # passed all the cases, they must conflict
      return val