import re
from datetime import datetime


class Transaction(object):
    def __init__(self, start_date=None, end_date=None, statements=None):
        self.start_date = start_date
        self.end_date = end_date
        self.statements = statements or []

    @property
    def duration(self):
        return (self.end_date - self.start_date).seconds if self.end_date and self.start_date else 0

    @property
    def total_changes(self):
        return sum([len(statement.changes) for statement in self.statements])


class Statement(object):
    def __init__(self, changes=None):
        self.changes = changes or []


class Change(object):
    def __init__(self, command_type, actual_command):
        self.command_type = command_type
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
        command_type = change_buffer.split(' ')[0]
        change_instruction_without_comments = re.sub("/\*.*\*/", "", change_buffer)
        return Change(command_type, change_instruction_without_comments)
