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