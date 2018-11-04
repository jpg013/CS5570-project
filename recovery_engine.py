from data_operation import OperationType
import collections
from recovery_report import RecoveryReport
from recoverable_value import RecoverableValue

class ReadFromRelationship:
    """ReadFromRelationship represents a dependency relationship of two data operations where the 
    dependent_operation either reads from, or writes to a data item that has been written to by a previous
    operation of a different transaction. The relationship class has the properties, 
    recoverable_value, aca_value, and strict_value which indicate whether or not the relationship holds to 
    recoverable, aca and strict properties.
    """

    def __init__(self, dependent_operation, read_from_operation, dep_tx_complete_order, read_from_tx_complete_order):
        if dependent_operation is None:
            raise Exception('dependent_operation must be defined.')

        if read_from_operation is None:
            raise Exception('write_op must be defined.')

        self.dependent_operation = dependent_operation
        self.read_from_operation = read_from_operation
        self.dep_tx_complete_order = dep_tx_complete_order
        self.read_from_tx_complete_order = read_from_tx_complete_order
        
        # Values 
        self.recoverable_value = RecoverableValue.NOT_AVAILABLE
        self.aca_value = RecoverableValue.NOT_AVAILABLE
        self.strict_value = RecoverableValue.NOT_AVAILABLE

class RecoveryEngine:
    """RecoveryEngine class. Given a history will determine whether or not
    the history is recoverable, avoids cascading aborts (aca), and is strict."""

    def __init__(self, history):
        if history is None:
            raise ValueError("History must be defined.")
      
        self.history = history

        # set of ReadFromRelationships for the given history schedule
        self.read_from_relationship_set = set()

        # a dict containing the order that each transaction in the history either commits/aborts. The keys are 
        # transaction ids, and the value is the order of completion, starting at index 1.
        self.tx_completed_order = {}

        # Determine the order in which the transactions completed. This is needed for recoverability
        self.determine_tx_completed_order()
        
        # Construct the set of read from relationships
        self.construct_read_from_relationship_set()

        # Analyze the ReadFromRelationships for recoverable, aca, and strict properties
        self.analyze()
        
    def analyze(self):
        """Iterates over each read from relationship computes recoverable/aca/strict property of each."""
        
        for item in self.read_from_relationship_set:
            item.recoverable_value = self.determine_recoverable(item)
            item.aca_value = self.determine_aca(item)
            item.strict_value = self.determine_strict(item)

    def get_report(self):
        """Helper method for generating a recovery report after the history has been analyzed. Analyze() should be 
        called first before a report can be generated"""
        recovery_report = RecoveryReport()

        for read_from_op in self.read_from_relationship_set:
            recovery_report.process_result(read_from_op)
        
        return recovery_report.build_report(self.history)
            
    def determine_recoverable(self, read_from_relationship):
        """Rules for determining whether dep_op is recoverable with regards to write_tx. Returns True is recoverable else False"""

        dep_tx       = read_from_relationship.dependent_operation.transaction
        read_from_tx = read_from_relationship.read_from_operation.transaction
        
        dep_tx_complete_order = self.tx_completed_order[dep_tx.id]
        read_from_tx_complete_order = self.tx_completed_order[read_from_tx.id]

        # Recoverable Rules
        is_recoverable = None
        if dep_tx.commit_type() is OperationType.COMMIT and read_from_tx.commit_type() is OperationType.COMMIT:
            # case1: dep_tx && read_from_tx both commit, since dep_tx reads from read_from_tx, read_from_tx must commit first
            is_recoverable = read_from_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and read_from_tx.commit_type() is OperationType.COMMIT:
            # case2: dep_tx aborts while read_from_tx commits, for this to be recoverable dep_tx must abort after read_from_tx commits
            is_recoverable = read_from_tx_complete_order < dep_tx_complete_order

        if dep_tx.commit_type() is OperationType.COMMIT and read_from_tx.commit_type() is OperationType.ABORT:
            # case3: dep_tx commits while read_from_tx aborts, for this to be recoverable dep_tx must abort before read_from_tx commits
            is_recoverable = dep_tx_complete_order < read_from_tx_complete_order

        if dep_tx.commit_type() is OperationType.ABORT and read_from_tx.commit_type() is OperationType.ABORT:
            # case4: dep_tx and read_from_tx both abort, then dep_tx must abort before read_from_tx
            is_recoverable = dep_tx_complete_order < read_from_tx_complete_order

        # we should never reach this case?
        if is_recoverable is None:
            raise Exception('invalid recoverability')

        return RecoverableValue.IS_RECOVERABLE if is_recoverable else RecoverableValue.IS_NOT_RECOVERABLE


    def determine_aca(self, read_from_relationship):
        """To determine aca we follow the logic that if T1 explicitly reads data item x from T2, then T2 must commit 
        before any operation in T1 reads data item x that is written by T2. Returns True is aca else false."""

        dep_op = read_from_relationship.dependent_operation
        read_from_op = read_from_relationship.read_from_operation
        
        # The dependent operation has to be an explicit read
        if dep_op.is_write():
            return RecoverableValue.NOT_AVAILABLE

        return RecoverableValue.IS_ACA if self.commit_exists_between_operations(read_from_op, dep_op, read_from_op.transaction) else RecoverableValue.IS_NOT_ACA

    def determine_strict(self, read_from_relationship):
        """To determine strict, if T1 is functionally dependent on T2, T2 must commit
        before any T1 writes to a data item and T2 also writes to the same data item. Returns true for strict"""
        
        dep_op = read_from_relationship.dependent_operation
        read_from_op = read_from_relationship.read_from_operation

        return RecoverableValue.IS_STRICT if self.commit_exists_between_operations(read_from_op, dep_op, read_from_op.transaction) else RecoverableValue.IS_NOT_STRICT

    def determine_tx_completed_order(self):
        """Iterate over each data_operation, discarding all non commits/aborts, and populate the tx_completed_order dict"""
        order = 1
        for data_op in self.history.schedule:
            if data_op.is_abort() or data_op.is_commit():
                self.tx_completed_order[data_op.transaction.id] = order
                order += 1

    def commit_exists_between_operations(self, start_op=None, end_op=None, ref_tx=None):
        """Finds whether or not a commit operation exists for a given transaction in the schedule between two given operations."""
        start_idx = self.history.schedule.index(start_op)
        end_idx = self.history.schedule.index(end_op)
        sched_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')

        return any(op.is_commit() and op.transaction is ref_tx for op in sched_slice)
    
    def abort_exists_between_operations(self, start_op=None, end_op=None, ref_tx=None):
        """Finds whether or not an abort operation exists for a given transaction in the schedule between two given operations."""
        start_idx = self.history.schedule.index(start_op)
        end_idx = self.history.schedule.index(end_op)
        schedule_slice = self.history.schedule[start_idx:end_idx]

        if start_idx >= end_idx:
            raise Exception('invalid index bounds')
                
        # Check for aborts in the index slice
        return any(item.is_abort() and item.transaction is ref_tx for item in schedule_slice)

    def construct_read_from_relationship_set(self):
        """Find edge relationships between nodes. We say a node Ti, reads x from Tj in history H if:
        1) wj(x) < ri(x) 
        2) aj !< ri(x)
        3) if there is some wk(x) such that wj(x) < wk(x) < ri(x), then ak < ri(x)
        """
        
        # init the set
        self.read_from_relationship_set = set()
        
        # Schedule slice
        schedule = self.history.schedule[0:]

        # Iterate through each item in the schedule
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
                
                # If dep_op is reading a write from the same transaction then we can simply break out and continue;
                if op.transaction is dep_op.transaction:
                    break

                abort_exists = self.abort_exists_between_operations(op, dep_op, op.transaction)

                if abort_exists:
                    continue
                
                # Passed all the criteria, so op is being read from.
                read_from_op = op
                break

            # If we didnt' find a write operation keep going
            if read_from_op is None:
                continue
            
            # There exists a read from relation. Add to the set.
            self.read_from_relationship_set.add(ReadFromRelationship(
                dep_op, 
                read_from_op,
                self.tx_completed_order[dep_op.transaction.id],
                self.tx_completed_order[read_from_op.transaction.id]
            ))
