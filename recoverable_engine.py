from data_operation import OperationType

class RecoverableNode:
    """RecoverableGraphNode"""
  
    def __init__(self, id=None):
        if id is None:
            raise ValueError("SerializationGraphNode requires a valid id")
    
        self.id = id

        # Dictionary contianing other nodes as keys. The dict values are the 
        # data_operation read/write pairs that cause the relationship
        self.edges = {}

    def pretty_print(self):
        for key, val in self.edges.items():
            print('T{0} reads from T{1} because : '.format(self.id, key.id))
            for s in val:
                for i in s:
                    i.pretty_print()
                    print(' ')
    
    def add_edge(self, node, op_set):
        if node not in self.edges:
            self.edges[node] = []
        
        self.edges[node].append(op_set)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class RecoverableEngine:
    """RecoverableEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        self.graph_nodes = []
        self.commit_abort_order = []
  
    def run(self):
        self.build_graph_nodes()
        self.build_node_edges()
        self.make_commit_abort_order()
        print(self.commit_abort_order)

        for x in self.graph_nodes:
            x.pretty_print()

    def determine_recoverability(self):
        """To determine recoverability, for each graph node edge T1 -> T2, where T1 read from T2,
        c2 < c1 or a1 < a2."""


    def make_commit_abort_order(self):
        for item in self.history.schedule:
            if item.operation_type is OperationType.COMMIT or item.operation_type is OperationType.ABORT:
                self.commit_abort_order.append(item.transaction_id)
    
    def build_graph_nodes(self):
        for tx in self.history.transactions:
            self.graph_nodes.append(RecoverableNode(tx.transaction_id))

    def get_node(self, id): 
        return next(x for x in self.graph_nodes if x.id is id)

    def create_node_edge(self, read_op, write_op):
        read_node = self.get_node(read_op.transaction_id)
        write_node = self.get_node(write_op.transaction_id)

        if read_node is None or write_node is None:
            raise Exception("Undefined graph_node for data operation")

        data_op_set = set([read_op, write_op])
        read_node.add_edge(write_node, data_op_set)       

    def build_node_edges(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x)
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """

        schedule = self.history.schedule[0:]

        for idx, read_op in enumerate(schedule):
            # cannot read from previous data if first element
            if idx == 0:
                continue

            # must be a read operation
            if read_op.operation_type is not OperationType.READ:
                continue
            
            # look for an write to the same data item
            p_slice = schedule[0:idx]
            write_found = None

            for idx, write_op in enumerate(reversed(p_slice)):
                # only care about same data item write op
                if write_op.data_item != read_op.data_item:
                    continue
                
                # Filter out non-writes
                if write_op.operation_type is not OperationType.WRITE:
                    continue

                # break if same transaction
                if write_op.transaction_id != read_op.transaction_id:
                    write_found = write_op
                
                break
            
            if write_found is not None:
                self.create_node_edge(read_op, write_found)


                

                      
        


        
                

    

  
    

