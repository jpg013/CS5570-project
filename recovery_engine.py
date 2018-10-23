from data_operation import OperationType
import collections
from recovery_report import RecoveryReport

class FunctionalDependency:
    """FunctionalDependency represents a dependency relationship of two data operations where the 
    dep_op either reads from, or writes to a data item that has been wrtten to by the independent 
    write operation.
    """

    def __init__(self, dep_op, write_op):
        if dep_op is None:
            raise Exception('dep_op must be defined.')

        if write_op is None:
            raise Exception('write_op must be defined.')

        self.dep_op = dep_op
        self.write_op = write_op
        self.is_recoverable = None
        self.is_aca = None
        self.is_strict = None

class RecoveryEngine:
    """RecoveryEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history
        # set of ReadRecoveryResults containing a read op that reads data item written by write op from a 
        # different transaction
        
        self.functional_dependency_set = set()

        # a dict containing the order that each transaction in the history either commits/aborts. The keys are 
        # transaction ids, and the value is the order of completion, starting at index 1.
        #
        self.tx_completed_order = {}

        
    def analyze(self):
        """Main method to be called to analyze the history. Returns a RecoveryResult"""
        
        # Determine the order in which the transactions completed. This is needed for recoverability
        self.determine_tx_completed_order()
        
        # Construct the set of read from relationships
        self.construct_functional_dependency_set()

        # Construct the set of read from relationships
        self.analyze_functional_dependencies()

        return self.build_results()

    def build_results(self):
        recovery_result = RecoveryReport(self.tx_completed_order)

        for func_dep in self.functional_dependency_set:
            recovery_result.process_result(func_dep)
        
        # for item in self.read_from_set:
        return recovery_result
        
    def analyze_functional_dependencies(self):
        """Iterates over each read set item and computes recoverable/aca properties."""
        for func_dep in self.functional_dependency_set:
            func_dep.is_recoverable = self.determine_recoverable(func_dep.dep_op, func_dep.write_op)            
            func_dep.is_aca = self.determine_aca(func_dep.dep_op, func_dep.write_op)
            func_dep.is_strict = self.determine_strict(func_dep.dep_op, func_dep.write_op)
            
    def determine_recoverable(self, dep_op, write_op):
        """Rules for determining whether dep_op is recoverable with regards to write_tx. Returns True is recoverable else False"""
        
        dep_tx = dep_op.transaction
        write_tx = write_op.transaction
        
        dep_tx_complete_order = self.tx_completed_order[dep_tx.id]
        write_tx_complete_order = self.tx_completed_order[write_tx.id]

        # some ugly use cases here.
        if dep_tx.commit_type() is OperationType.COMMIT and write_tx.commit_type() is OperationType.COMMIT:
            # case1: dep_tx && write_tx both commit, since dep_tx reads from write_tx, write_tx must commit first
            return write_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and write_tx.commit_type() is OperationType.COMMIT:
            # case2: read_tx aborts while write_tx commits, for this to be recoverable read_tx must abort after write_tx commits
            return write_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.COMMIT and write_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx commits while write_tx aborts, for this to be recoverable read_tx must abort before write_tx commits
            return dep_tx_complete_order < write_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and write_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx and write_tx both abort, then read_tx must abort before read_tx
            return dep_tx_complete_order < write_tx_complete_order

        # we should never reach this case?
        raise Exception('what the hell!')

    def determine_aca(self, dep_op, write_op):
        """To determine aca we follow the logic that if T1 reads from T2, the T2 must commit 
        before any operation in T1 reads data that is written by T2. Returns True is aca else false."""

        return self.commit_exists_within_func_dep(dep_op, write_op)

    def determine_strict(self, dep_op, write_op):
        """To determine strict, if T1 is functionally dependent on T2, T2 must commit
        before any T1 writes to a data item and T2 also writes to the same data item. Returns true for strict"""

        return self.commit_exists_within_func_dep(dep_op, write_op) and dep_op.is_write()

    def determine_tx_completed_order(self):
        order = 1
        for data_op in self.history.schedule:
            if data_op.is_abort() or data_op.is_commit():
                self.tx_completed_order[data_op.transaction.id] = order
                order += 1

    def commit_exists_within_func_dep(self, dep_op=None, write_op=None):
        start_idx = self.history.schedule.index(write_op)
        end_idx = self.history.schedule.index(dep_op)
        sched_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')

        return any(op.is_commit() and op.transaction is write_op.transaction for op in sched_slice)
    
    def abort_exists_within_func_dep(self, dep_op=None, write_op=None):
        start_idx = self.history.schedule.index(write_op)
        end_idx = self.history.schedule.index(dep_op)
        schedule_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')
                
        # Check for aborts in the index slice
        return any(item.is_abort() and item.transaction is write_op.transaction for item in schedule_slice)

    def add_functional_dependency(self, dep_op, write_op):
        self.functional_dependency_set.add(FunctionalDependency(dep_op, write_op))
        
    def construct_functional_dependency_set(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x)
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """
        
        # init the set
        self.functional_dependency_set = set()
        
        schedule = self.history.schedule[0:]

        for idx, read_op in enumerate(schedule):
            # cannot read from previous data if first element
            if idx == 0:
                continue

            # must be a read operation
            if not read_op.is_read():
                continue
            
            # look for an write to the same data item
            r_slice = schedule[0:idx]
            write_found = None

            for write_op in reversed(r_slice):
                # only care about same data item write op
                if write_op.data_item != read_op.data_item:
                    continue
                
                # Filter out non-writes
                if not write_op.is_write():
                    continue

                # break if same transaction
                if write_op.transaction is read_op.transaction:
                    break
                
                write_found = write_op
                break

            if write_found is None:
                continue
            
            abort_exists = self.abort_exists_within_func_dep(read_op, write_found)
            
            # An abort exists, so read_op does not read from write_op
            if abort_exists:
                continue
            
            # There is a read from relation. Add a tuple to the read set
            self.add_functional_dependency(read_op, write_op)
            

                

                      
        


        
                

    

  
    

