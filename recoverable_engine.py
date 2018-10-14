from data_operation import OperationType

class RecoverableNode:
    """RecoverableGraphNode"""
  
    def __init__(self, id=None, commit_type=None):
        if id is None:
            raise ValueError("RecoverableGraphNode requires a valid id")
        
        if commit_type is None:
            raise ValueError("RecoverableGraphNode requires a commit_type")
        
        self.id = id
        self.commit_type = commit_type
        self.formatted_commit_type = str(self.commit_type.name.lower() + 's')

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
        self.read_set = set()

        self.transaction_terminate_order = []
        self.not_recoverable_set = set()
  
    def run(self):
        #self.build_graph_nodes()
        #self.build_node_edges()
        self.construct_read_set()
        self.determine_transaction_terminate_order()
        self.determine_recoverability()

    def get_transaction_by_id(self, tx_id):
        return next(x for x in self.history.transactions if x.transaction_id is tx_id)

    def determine_recoverability(self):
        """To determine recoverability, for each graph node edge T1 -> T2, where T1 read from T2,
        c2 < c1 or a1 < a2."""
        
        for item in self.read_set:
            op_a = item[0]
            op_b = item[1]

            tx_a = self.get_transaction_by_id(op_a.transaction_id)
            tx_b = self.get_transaction_by_id(op_b.transaction_id)

            is_recoverable = self.is_transaction_recoverable(tx_a, tx_b)

            # Add unrecoverable node tuples to a set
            if not is_recoverable:
                self.display_recoverable_error_message(tx_a, tx_b)
                #self.not_recoverable_set.add((n, key)) 

    def display_recoverable_error_message(self, tx_a, tx_b):
        a_formatted_commit_type = tx_a.commit_type().name.lower() + 's'
        b_formatted_commit_type = tx_b.commit_type().name.lower() + 's'

        print('history is not recoverable because T{0} reads from T{1} and T{0} {2} before T{1} {3}.'
            .format(tx_a.transaction_id, tx_b.transaction_id, a_formatted_commit_type, b_formatted_commit_type))

    def is_transaction_recoverable(self, tx_a, tx_b):
        """tx_a is dependent on / reads from tx_b"""
        a_terminate_order = self.transaction_terminate_order.index(tx_a.transaction_id)
        b_terminate_order = self.transaction_terminate_order.index(tx_b.transaction_id)

        # some ugly use cases here.
        if tx_a.commit_type() is OperationType.COMMIT and tx_b.commit_type() is OperationType.COMMIT:
            # case1: a && b both commit, since a reads from b, b must commit first
            return b_terminate_order < a_terminate_order

        if tx_a.commit_type() is OperationType.ABORT and tx_b.commit_type() is OperationType.COMMIT:
            # case2: a aborts while b commits, for this to be recoverable tx_a must abort after tx_b commits
            return b_terminate_order < a_terminate_order

        if tx_a.commit_type() is OperationType.COMMIT and tx_b.commit_type() is OperationType.ABORT:
            # case3: a commits while b aborts, for this to be recoverable tx_a must abort before tx_b commits
            return a_terminate_order < b_terminate_order

        if tx_a.commit_type() is OperationType.ABORT and tx_b.commit_type() is OperationType.ABORT:
            # case3: a and b both abort, then a must abort before b 
            return a_terminate_order < b_terminate_order

        # we should never reach this case?
        raise Exception('what the hell?')

    def determine_transaction_terminate_order(self):
        for item in self.history.schedule:
            if item.is_abort() or item.is_commit():
                self.transaction_terminate_order.append(item.transaction_id)
    
    def build_graph_nodes(self):
        for tx in self.history.transactions:
            self.graph_nodes.append(RecoverableNode(tx.transaction_id, tx.get_commit_type()))

    def get_node(self, id): 
        return next(x for x in self.graph_nodes if x.id is id)

    def create_node_edge(self, read_op, write_op):
        read_node = self.get_node(read_op.transaction_id)
        write_node = self.get_node(write_op.transaction_id)

        if read_node is None or write_node is None:
            raise Exception("Undefined graph_node for data operation")

        data_op_set = set([read_op, write_op])
        read_node.add_edge(write_node, data_op_set)       

    def construct_read_set(self):
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
            if not read_op.is_read():
                continue
            
            # look for an write to the same data item
            p_slice = schedule[0:idx]
            write_found = None

            for idx, write_op in enumerate(reversed(p_slice)):
                # only care about same data item write op
                if write_op.data_item != read_op.data_item:
                    continue
                
                # Filter out non-writes
                if not write_op.is_write():
                    continue

                # break if same transaction
                if write_op.transaction_id != read_op.transaction_id:
                    write_found = write_op
                
                break
            
            if write_found is not None:
                # There is a read from relation. Add a tuple to the read set
                self.read_set.add((read_op, write_op))


                

                      
        


        
                

    

  
    

