from recoverable_value import RecoverableValue

class RecoveryResult:
    """RecoveryResult Result"""
    
    def __init__(self, read_from_relationship):
        self.dep_op = read_from_relationship.dependent_operation
        self.read_from_op = read_from_relationship.read_from_operation
        self.recoverable_value = read_from_relationship.recoverable_value
        self.strict_value = read_from_relationship.strict_value
        self.aca_value = read_from_relationship.aca_value

    def get_recoverable_msg(self):
        if self.recoverable_value is RecoverableValue.NOT_AVAILABLE:
            return None

        is_recoverable = self.recoverable_value is RecoverableValue.IS_RECOVERABLE
        
        return '{0} {1} {2} and T{3} {4} {5} T{6} {7}.'.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty(),
            self.dep_op.transaction.id, 
            self.dep_op.transaction.commit_type().name.lower() + 's', 
            'after' if is_recoverable else 'before',
            self.read_from_op.transaction.id,
            self.read_from_op.transaction.commit_type().name.lower() + 's'
        )

    def get_strict_msg(self):
        if self.strict_value is RecoverableValue.NOT_AVAILABLE:
            return None
        
        return '{0} {1} {2} and T{3} {4} {5}.'.format(
            self.dep_op.format_pretty(), 
            'overwrites' if self.dep_op.is_write() else 'reads from',
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits before' if self.strict_value is RecoverableValue.IS_STRICT else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

    def get_aca_msg(self):
        if self.aca_value is RecoverableValue.NOT_AVAILABLE:
            return None

        return '{0} reads from {1} and T{2} {3} {4}.'.format(
            self.dep_op.format_pretty(), 
            self.read_from_op.format_pretty(),
            self.read_from_op.transaction.id, 
            'commits' if self.aca_value is RecoverableValue.IS_ACA else 'does not commit before',
            self.dep_op.format_pretty(), 
        )

class RecoveryReport:
    """RecoveryReport produces recovery results for a given history."""
    
    def __init__(self, history, read_from_relationship_set):
        # list of recovery results
        self.recovery_results = []

        # holds the given history
        self.history = history

        # List of recoverable violations for the history
        self.recoverable_violations = []
        
        # List of aca violations for the history
        self.aca_violations = []

        # List of strict violations for the history
        self.strict_violations = []

        self.process_results(read_from_relationship_set)
        
    def generate_strict_report(self):
        if len(self.recovery_results) == 0 or len(self.strict_violations) == 0:  
            return "\n\nhistory is ST"
        
        strict_report = '\n\nhistory is not strict because:'

        for idx, result in enumerate(self.strict_violations):
            strict_report += '\n{0}) {1}'.format(idx+1, result)

        return strict_report

    def generate_aca_report(self):
        if len(self.recovery_results) == 0 or len(self.aca_violations) == 0:  
            return "\n\nhistory is ACA"
        
        aca_report = '\n\nhistory is not aca because:'

        for idx, result in enumerate(self.aca_violations):
            aca_report += '\n{0}) {1}'.format(idx+1, result)

        return aca_report
    
    def generate_recoverable_report(self):
        recoverable_report = "\n"
        
        if len(self.recovery_results) == 0:
            recoverable_report += 'history recovery is not availabe because there do not exist any read-from relationships.'
        elif len(self.recoverable_violations) == 0:
            recoverable_report += 'history is recoverable.'
        else:
            recoverable_report += 'history is not recoverable because:'

            for idx, result in enumerate(self.recoverable_violations):
                recoverable_report += '\n{0}) {1}'.format(idx+1, result)

        return recoverable_report

    def build_report(self):
        hist_title = self.history.format_pretty()
        report = '\nHistory Recovery Report\n{0}\n'.format(hist_title)

        report += "=" * len(hist_title)

        report += self.generate_recoverable_report()
        report += self.generate_aca_report()
        report += self.generate_strict_report()

        report += "\n" + "=" * len(hist_title) + "\n"
        
        self.report = report

    def display_pretty(self):
        print(self.report)

    def process_results(self, read_from_relationship_set):
        for item in read_from_relationship_set:
            recovery_result = RecoveryResult(item)

            self.recovery_results.append(recovery_result)
            self.process_recoverable_result(recovery_result)
            self.process_aca_result(recovery_result) 
            self.process_strict_result(recovery_result)
        
    def process_recoverable_result(self, recovery_result):
        msg = recovery_result.get_recoverable_msg()

        if msg is None:
            return

        if recovery_result.recoverable_value is RecoverableValue.IS_NOT_RECOVERABLE:
            self.recoverable_violations.append(msg)

    def process_strict_result(self, recovery_result):
        msg = recovery_result.get_strict_msg()

        if msg is None:
            return

        if recovery_result.strict_value is RecoverableValue.IS_NOT_STRICT:
            self.strict_violations.append(msg)

    def process_aca_result(self, recovery_result):
        msg = recovery_result.get_aca_msg()

        if msg is None:
            return

        if recovery_result.aca_value is RecoverableValue.IS_NOT_ACA:
            self.aca_violations.append(msg)

    def is_recoverable(self):
        return all(item.recoverable_value is RecoverableValue.IS_RECOVERABLE for item in self.recovery_results)

    def is_aca(self):
        if not self.is_recoverable():
            return False

        available_values = list(filter(lambda x: x.aca_value is RecoverableValue.IS_ACA or x.aca_value is RecoverableValue.IS_NOT_ACA, self.recovery_results))

        if len(available_values) == 0:
            return True

        return all(item.aca_value is RecoverableValue.IS_ACA for item in available_values)

    def is_strict(self):
        return all(item.strict_value is RecoverableValue.IS_STRICT for item in self.recovery_results)

    def recovery_results_available(self):
        return len(self.recovery_results) > 0
    
        
