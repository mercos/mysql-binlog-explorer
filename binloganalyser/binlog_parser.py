from datetime import datetime


class Transaction(object):
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.statements = []

    def __repr__(self):
        return 'Transaction {} (duration: {})'.format(self.start_date.strftime("%Y-%m-%d %H:%M:%S"), self.duration)

    @property
    def duration(self):
        return (self.end_date - self.start_date).seconds


class Statement(object):
    def __init__(self):
        self.changes = []


class Change(object):
    def __init__(self, type, actual_command):
        self.type = type
        self.actual_command = actual_command


class BinlogParser(object):
    def parse(self, binlog_file):
        transactions = []
        change_buffer = ''
        last_line = None
        for line in binlog_file:
            if line.startswith("BEGIN"):
                transaction = Transaction()
            elif "Table_map:" in line:
                statement = Statement()
                if not transaction.start_date:
                    transaction.start_date = datetime.strptime(line[1:16], '%y%m%d %H:%M:%S')
                transaction.statements.append(statement)
            elif line.startswith("### UPDATE") or line.startswith("### INSERT") or line.startswith("### DELETE"):
                if change_buffer:
                    statement.changes.append(self._create_change(change_buffer))
                    change_buffer = ''
                else:
                    change_buffer = line[4:]
            elif line.startswith("###"):
                change_buffer += line[4:]
            elif line.startswith("# at") and change_buffer:
                statement.changes.append(self._create_change(change_buffer))
                change_buffer = ''
            elif line.startswith("COMMIT"):
                transaction.end_date = datetime.strptime(last_line[1:16], '%y%m%d %H:%M:%S')
                transactions.append(transaction)
            last_line = line
        return transactions

    def _create_change(self, change_buffer):
        type = change_buffer.split(' ')[0]
        return Change(type, change_buffer)
