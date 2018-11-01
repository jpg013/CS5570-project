from data_operation import OperationType
import collections
from recovery_report import RecoveryReport

class ReadFromRelationship:
    """ReadFromRelationship represents a dependency relationship of two data operations where the 
    dependent_operation either reads from, or writes to a data item that has been written to by a previous
    operation of a different transaction. The relationship class has addition properties, 
    is_recoverable, is_aca, and is_strict and their reasons which are initially set to None.
    """

    def __init__(self, dependent_operation, read_from_operation):
        if dependent_operation is None:
            raise Exception('dependent_operation must be defined.')

        if read_from_operation is None:
            raise Exception('write_op must be defined.')

        self.dependent_operation = dependent_operation
        self.read_from_operation = read_from_operation
        
        # Values 
        self.is_recoverable = None
        self.is_recoverable_reason = None
        self.is_aca = None
        self.is_aca_reason = None
        self.is_strict = None
        self.is_strict_reason = None

class RecoveryEngine:
    """RecoveryEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history

        # set of FunctionalDependency's containing a read op that reads data item written by write op from a 
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

        # Analyze the set of read from relationships
        self.analyze_functional_dependencies()

        return self.build_results()

    def build_results(self):
        recovery_result = RecoveryReport(self.tx_completed_order)

        for func_dep in self.functional_dependency_set:
            recovery_result.process_result(func_dep)
        
        return recovery_result.get_report()
        
    def analyze_functional_dependencies(self):
        """Iterates over each read set item and computes recoverable/aca/strict property of each."""
        
        for func_dep in self.functional_dependency_set:
            func_dep.is_recoverable = self.determine_recoverable(func_dep)
            func_dep.is_aca = self.determine_aca(func_dep)
            func_dep.is_strict = self.determine_strict(func_dep)
            
    def determine_recoverable(self, functional_dependency):
        """Rules for determining whether dep_op is recoverable with regards to write_tx. Returns True is recoverable else False"""

        dependent_operation = functional_dependency.dependent_operation
        read_from_operation = functional_dependency.read_from_operation

        dep_tx       = dependent_operation.transaction
        read_from_tx = read_from_operation.transaction
        
        dep_tx_complete_order = self.tx_completed_order[dep_tx.id]
        read_from_tx_complete_order = self.tx_completed_order[read_from_tx.id]

        # some ugly use cases here.
        if dep_tx.commit_type() is OperationType.COMMIT and read_from_tx.commit_type() is OperationType.COMMIT:
            # case1: dep_tx && read_from_tx both commit, since dep_tx reads from read_from_tx, read_from_tx must commit first
            return read_from_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and read_from_tx.commit_type() is OperationType.COMMIT:
            # case2: read_tx aborts while read_from_tx commits, for this to be recoverable read_tx must abort after read_from_tx commits
            return read_from_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.COMMIT and read_from_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx commits while read_from_tx aborts, for this to be recoverable read_tx must abort before read_from_tx commits
            return dep_tx_complete_order < read_from_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and read_from_tx.commit_type() is OperationType.ABORT:
            # case3: read_tx and read_from_tx both abort, then read_tx must abort before read_tx
            return dep_tx_complete_order < read_from_tx_complete_order

        # we should never reach this case?
        raise Exception('unknown operation type')

    def determine_aca(self, functional_dependency):
        """To determine aca we follow the logic that if T1 reads data item x from T2, the T2 must commit 
        before any operation in T1 reads data item x that is written by T2. Returns True is aca else false."""

        dependent_operation = functional_dependency.dependent_operation
        read_from_operation = functional_dependency.read_from_operation

        
        # The dependent operation has to be a read
        if dependent_operation.is_write():
            return

        return self.commit_exists_between_operations(read_from_operation, dependent_operation)

    def determine_strict(self, functional_dependency):
        """To determine strict, if T1 is functionally dependent on T2, T2 must commit
        before any T1 writes to a data item and T2 also writes to the same data item. Returns true for strict"""
        
        dependent_operation = functional_dependency.dependent_operation
        read_from_operation = functional_dependency.read_from_operation

        return self.commit_exists_between_operations(read_from_operation, dependent_operation)

    def determine_tx_completed_order(self):
        order = 1
        for data_op in self.history.schedule:
            if data_op.is_abort() or data_op.is_commit():
                self.tx_completed_order[data_op.transaction.id] = order
                order += 1

    def commit_exists_between_operations(self, start_op=None, end_op=None):
        start_idx = self.history.schedule.index(start_op)
        end_idx = self.history.schedule.index(end_op)
        sched_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')

        return any(op.is_commit() and op.transaction is start_op.transaction for op in sched_slice)
    
    def abort_exists_within_func_dep(self, dep_op=None, write_op=None):
        start_idx = self.history.schedule.index(write_op)
        end_idx = self.history.schedule.index(dep_op)
        schedule_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')
                
        # Check for aborts in the index slice
        return any(item.is_abort() and item.transaction is write_op.transaction for item in schedule_slice)

    def construct_functional_dependency_set(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x) 
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """
        
        # init the set
        self.functional_dependency_set = set()
        
        schedule = self.history.schedule[0:]

        for idx, dep_op in enumerate(schedule):
            # cannot read from previous data if first element
            if idx == 0:
                continue

            # pass if abort/commit
            if dep_op.is_abort() or dep_op.is_commit():
                continue

            # Create a slice of all the previous data operations in the schedule
            prev_slice = schedule[0:idx]
            read_from_op = None

            # walk backwards through the prev slice and look for operations that
            # have written to the dep_op.
            for op in reversed(prev_slice):
                # only care about same data item
                if op.data_item != dep_op.data_item:
                    continue
                
                # Filter out non-writes
                if not op.is_write():
                    continue

                # If dep_op is reading a write from the same transaction then
                # we can simply break out and continue;
                if op.transaction is dep_op.transaction:
                    break
                
                # Passed all the criteria, so op is being read from.
                read_from_op = op
                break

            # If we didnt' find a write operation keep going
            if read_from_op is None:
                continue
            
            #abort_exists = self.abort_exists_within_func_dep(first_op, write_found)
            
            # An abort exists, so read_op does not read from write_op
            #if abort_exists:
                #continue
            
            # There is a read from relation. Add functional dependency.
            self.functional_dependency_set.add(FunctionalDependency(dep_op, read_from_op))
