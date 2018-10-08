from data_operation import OperationType

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

class SerializationGraphNode:
    """ SerializationGraphNode """
  
    def __init__(self, id=None):
        if id is None:
            raise ValueError("SerializationGraphNode requires a valid id")
    
        self.node_id = id

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

        # List holding the serialization graph nodes for a given history
        self.sg_nodes = []

        # Dictionary holding the graph structure. The keys are Sgnodes, and the values are sets of SGNodes that
        # are functionally dependent on the key node.
        self.graph = {}

        # list of SerializationGraphCycles.  
        self.cycles = []

    
        self.build_graph_nodes(history)
        self.construct_graph(history)
        self.find_all_cycles()
        self.pretty_print_graph()
        print(self.cycles)

    def check_dependencies_for_cycle(self, parent, child, check_set=None):
        if check_set is None:
            check_set = set()

        if child in check_set:
            return
        
        check_set.add(child)

        dep_set = self.graph[child]

        if parent in dep_set:
            return True

        for dep in dep_set:
            return self.check_dependencies_for_cycle(parent, dep, check_set)

    def find_all_cycles(self):
        # Go through each node in the graph and look at it's functional dependency set. 
        # For each item in the set, see if that items functional dependency set contains 
        # the first node.

        for parent_node, dep_set in self.graph.items():
            for dep_node in dep_set:
                has_cycle = self.check_dependencies_for_cycle(parent_node, dep_node)
                
                if has_cycle == True:
                    self.add_cycle(parent_node, dep_node)    
    
    def pretty_print_graph(self):
        for key, val in self.graph.items():
            for item in val:
                print(f'Transaction{key.node_id} --> Transaction{item.node_id}')
  
    def add_cycle(self, node_a, node_b):
        """Adds a cycle if it does not already exist."""
        exists = any(cycle.is_same(node_a, node_b) for cycle in self.cycles)

        if exists != True:
            self.cycles.append(SerializationGraphCycle(node_a, node_b))
  
    def is_cycle(self, edge_a, edge_b):
        """Determines whether two edges are a cycle. To be true they must be a 
        reflection of each other. E.g. T1 -> T2 && T2 -> T1. In other words, T2 must
        be functionally dependent on T1 and T1 must be functionally dependent on T2.
        """
        return edge_a.node_a is edge_b.node_b and edge_a.node_b is edge_b.node_a

    def build_graph_nodes(self, history):
        for tx in history.transactions:
            self.sg_nodes.append(SerializationGraphNode(tx.transaction_id))

    def get_node(self, id): 
        return next(x for x in self.sg_nodes if x.node_id is id)

    def construct_graph(self, history):
        schedule = history.schedule[0:]
    
        for idx, val in enumerate(schedule):
            curr_node = self.get_node(val.transaction_id)

            if curr_node is None:
                raise Exception("Undefined sg_node for data operation")

            if curr_node not in self.graph:
                # Init set of dependencies
                self.graph[curr_node] = set()

            # Check for functional dependencies
            dependency = self.find_functional_dependency(val, schedule[idx+1:])

            if dependency is None:
                continue

            dep_node = self.get_node(dependency.transaction_id)

            # Add to dependecy set
            self.graph[curr_node].add(dep_node)

    def find_functional_dependency(self, op, schedule):
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

            # If a duplicate data operation is found in the schedule that will be the functional dependency
            # Special cases for same transaction and same data item
            if curr.transaction_id == op.transaction_id and curr.data_item == op.data_item:
                # This should not happen in the current history implementation, but if the exact same
                # data operation is found then return None
                if curr.operation_type == op.operation_type:
                    return None
                
                # If a data operation exists in the schedule that operates is in the same transaction and
                # operates on the same data item and the later is a write, then that will be the funct dep.
                # So return, See the following example for why I am doing this:
                # write_2_[2] --> read_3_[3] --> write_3_[3] --> write_4_[4] --> commit_2 --> write_1_[3] --> abort_1 --> commit_4 --> abort_3
                # Transaction3 --> Transaction1
                # Transaction3 --> Transaction1
                if curr.operation_type == OperationType.WRITE:
                    return None

                # Data operations in the same transaction cannot conflict so continue
                continue
                
            # passed all the cases, they conflict
            return curr
        
        return None