class RecoveryReport:
    """RecoveryReport produces recovery results for a given history."""
    
    def __init__(self, tx_completed_order):
        self.tx_completed_order = tx_completed_order
        # list of functional dependency recovery violations
        self.recovery_violations = []
        # list of functional dependency recovery compliances
        self.recovery_compliances = []

        # list of functional dependency aca violations
        self.aca_violations = []
        # list of functional dependency aca compliances
        self.aca_compliances = []

        #list of functional dependency strict violations
        self.strict_violations = []
        #list of functional dependency string compliances
        self.strict_compliances = []

    def generate_strict_report(self):
        is_history_strict = len(self.strict_violations) == 0

        report = 'history is{0}strict because:'.format(' ' if is_history_strict else ' not ')

        reasons = self.strict_compliances[0:] if is_history_strict else self.strict_violations[0:]

        for idx, reason in enumerate(reasons):
            report = report + '\n{0}) {1}'.format(idx+1, reason)

        return report

    def generate_aca_report(self):
        is_history_aca = len(self.aca_violations) == 0

        report = 'history is{0}aca because:'.format(' ' if is_history_aca else ' not ')

        reasons = self.aca_compliances[0:] if is_history_aca else self.aca_violations[0:]

        for idx, reason in enumerate(reasons):
            report = report + '\n{0}) {1}'.format(idx+1, reason)

        return report
    
    def generate_recoverable_report(self):
        is_history_recoverable = len(self.recovery_violations) == 0

        report = 'history is{0}recoverable because:'.format(' ' if is_history_recoverable else ' not ')

        reasons = self.recovery_compliances[0:] if is_history_recoverable else self.recovery_violations[0:]

        for idx, reason in enumerate(reasons):
            report = report + '\n{0}) {1}'.format(idx+1, reason)

        return report

    def get_report(self):
        return self.generate_recoverable_report() + '\n \n' + self.generate_aca_report() + '\n\n' + self.generate_strict_report()

    def process_result(self, func_dep=None):
        if func_dep is None:
            raise Exception('func_dep must be defined')

        self.build_recovery_result(func_dep)
        self.build_aca_result(func_dep)

    def process_strict_result(self, func_dep=None):
        if func_dep is None:
            raise Exception('func_dep must be defined')

        self.build_strict_result(func_dep)
        
    def build_recovery_result(self, func_dep):
        if func_dep is None:
            raise Exception('func_dep must be defined')
        
        dep_tx = func_dep.dep_op.transaction
        write_tx = func_dep.write_op.transaction
        
        dep_formatted_commit_type = dep_tx.commit_type().name.lower() + 's'
        write_formatted_commit_type = write_tx.commit_type().name.lower() + 's'

        formatted_order = 'before' if self.tx_completed_order[dep_tx.id] < self.tx_completed_order[write_tx.id] else 'after'
        formatted_dep_op_type = func_dep.dep_op.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(func_dep.dep_op.format_pretty(), formatted_dep_op_type, func_dep.write_op.format_pretty())

        msg = msg + 'T{0} {1} {2} '.format(dep_tx.id, dep_formatted_commit_type, formatted_order)

        msg = msg + 'T{0} {1}.'.format(write_tx.id, write_formatted_commit_type)
        
        self.recovery_compliances.append(msg) if func_dep.is_recoverable else self.recovery_violations.append(msg)
        
    def build_aca_result(self, func_dep):
        if func_dep is None:
            raise Exception('func_dep must be defined')

        write_tx = func_dep.write_op.transaction

        formatted_dep_op_type = func_dep.dep_op.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(func_dep.dep_op.format_pretty(), formatted_dep_op_type, func_dep.write_op.format_pretty())
        
        if func_dep.is_aca:
            msg = msg + 'T{0} commits before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())
        else:
            msg = msg + 'T{0} does not commit before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())

        self.aca_compliances.append(msg) if func_dep.is_aca else self.aca_violations.append(msg)

    def build_strict_result(self, func_dep):
        if func_dep is None:
            raise Exception('func_dep must be defined')
            
        write_tx = func_dep.write_op.transaction

        formatted_dep_op_type = func_dep.dep_op.operation_type.name.lower() + 's'

        msg = '{0} {1} from {2} and '.format(func_dep.dep_op.format_pretty(), formatted_dep_op_type, func_dep.write_op.format_pretty())

        if func_dep.is_strict:
            msg = msg + 'T{0} commits before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())
        else:
            msg = msg + 'T{0} does not commit before {1}.'.format(write_tx.id, func_dep.dep_op.format_pretty())

        self.strict_compliances.append(msg) if func_dep.is_strict else self.strict_violations.append(msg)
                    

        
