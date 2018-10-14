from serialization_graph import SerializationGraph
from graph_path import GraphPath

class SerializableEngine:
    """ SerializableEngine class """

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        self.cycles = []
  
    def run(self):
        self.serialization_graph = SerializationGraph(self.history)
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


from data_operation import OperationType

class SerializationGraphNode:
    """SerializationGraphNode represents a transaction in a committed history."""
  
    def __init__(self, id=None):
        if id is None:
            raise ValueError("SerializationGraphNode requires a valid id")
    
        self.node_id = id
        
        # edges dictionary
        self.edges = {}

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        return self.node_id == other.node_id

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class SerializationGraph:
    """SerializationGraph builds a graph structure from the transactions of a given history"""

    def __init__(self, history=None):
        if history is None:
            raise ValueError("history must be defined.")

        # List holding the serialization graph nodes
        self.graph_nodes = []

        # build and construct graph
        self.build_graph_nodes(history)
        self.build_graph_edges(history)

    def pretty_print(self):
        for node in self.graph_nodes:
            for key, value in node.edges.items():
                print('edge: {0} -> {1}'.format(node.node_id, key.node_id))
                print('because', end=": ")
                
                for data_ops in value:
                    data_ops[0].pretty_print()
                    print(" --> ", end="")
                    data_ops[1].pretty_print()
                    print("")
                
    def build_graph_nodes(self, history):
        for tx in history.transactions:
            self.graph_nodes.append(SerializationGraphNode(tx.transaction_id))

    def get_node(self, id): 
        return next(x for x in self.graph_nodes if x.node_id is id)

    def build_graph_edges(self, history):
        schedule = history.schedule[0:]
    
        for idx, val in enumerate(schedule):
            curr_node = self.get_node(val.transaction_id)

            if curr_node is None:
                raise Exception("Undefined graph_node for data operation")

            # Check for functional dependencies
            conflict_op = self.find_conflict(val, schedule[idx+1:])

            if conflict_op is None:
                continue
                
            conflict_node = self.get_node(conflict_op.transaction_id)

            if conflict_node is None:
                raise Exception("Undefined graph_node for data operation")

            if conflict_node not in curr_node.edges:
                curr_node.edges[conflict_node] = set()

            curr_node.edges[conflict_node].add((val, conflict_op))

    def find_conflict(self, op, schedule):
        """Given a data operation and schedule, will enumerate the entire schedule looking for a 
        functional dependency. Returns the DataOperation if found, or None if not
        """
        
        if len(schedule) is 0:
            return None

        for curr in schedule:
            # Cannot have functional dependency on different data items
            if curr.data_item != op.data_item:
                continue
            
            # Don't care about commits or aborts
            if curr.operation_type == OperationType.COMMIT or curr.operation_type == OperationType.ABORT:
                continue

            # read/read do not conflict
            if curr.operation_type == OperationType.READ and op.operation_type == OperationType.READ:
                continue

            if curr.transaction_id == op.transaction_id:
                # If a duplicate data operation is found in the schedule that will be the functional dependency
                # Special cases for same transaction and same data item
                if curr.operation_type == op.operation_type:
                    raise Exception('duplicate data item found in schedule')
                
                continue
                
            # passed all the non-conflicting cases, so they conflict
            return curr
        
        return None
        
        
        


        
                

    

  
    


