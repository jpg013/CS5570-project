from serialization_graph import SerializationGraph
from graph_path import GraphPath

class SerializationGraphCycle:
    """SerializationGraphCycle represents a cycle between two serialization graph nodes.
    The order is not important, however, the nodes must be distinct.
    """
  
    def __init__(self, node_a=None, node_b=None):
        if node_a is None or node_b is None:
            raise ValueError('SerializationGraphCycle requires two valid SerializationGraphNodes')
      
        if node_a is node_b:
            raise ValueError('SerializationGraphCycle requires two distinct SerializationGraphNodes')

        self.node_a = node_a
        self.node_b = node_b

    def is_same(self, node_a, node_b):
        """Takes 2 SGNodes and returns whether or not the cycle contains these nodes"""
      
        # Must be distinct
        if node_a is node_b:
            return False
      
        return (
            (self.node_a is node_a or self.node_a is node_b) and 
            (self.node_b is node_a or self.node_b is node_b)
        )

class SerializableEngine:
    """ SerializableEngine class """

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        self.cycles = []
  
    def run(self):
        self.serialization_graph = SerializationGraph(self.history)
        self.serialization_graph.pretty_print()
        self.find_all_graph_cycles()

    def find_all_graph_cycles(self): 
        """Go through each node in the graph and look at it's functional dependency set. 
        For each item in the set, see if that items functional dependency set contains 
        the first node.
        """

        self.cycles = []
        
        if not self.serialization_graph:
            raise Exception('SerializationGraph must be defined.')
        
        for root_node in self.serialization_graph.graph_nodes:
            self.walk_path(root_node)

    def walk_path(self, node=None, path=None):
        if node is None:
            raise Exception('Node must be defined.')
        
        if path is None:
            path = GraphPath()
        else:
            path = path.clone()
            
        if path.creates_cycle(node) is True:
            path.add(node)
            return self.create_cycle_from_path(path)
        elif path.has_non_root_node(node):
            return
        else:
            path.add(node)

        for key in node.edges.keys():
            return self.walk_path(key, path)

    def create_cycle_from_path(self, cycle=None):
        if cycle is None:
            raise Exception('cycle must be defined.')

        exists = False
        for item in self.cycles:
            if item.get_cycle_set() == cycle.get_cycle_set():
                exists = True
                break

        if exists is True:
            return
        
        self.cycles.append(cycle)

        cycle.pretty_print()
        
        
        


        
                

    

  
    

