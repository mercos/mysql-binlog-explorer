import json

import bottle
from bottle import route, run, template

from binlog_parser import BinlogParser


@route('/')
def index():
    return template('main')


@route('/binlog-parser/')
def binlog_parser():
    transactions = BinlogParser().parse(open('tests/examples/binarylog_01_31_1145.log'))
    return binlog_parser_presenter(transactions)


def binlog_parser_presenter(list_of_transactions):
    response = {
        'data': [{
            'start_date': transaction.start_date.strftime("%Y-%m-%d %H:%M:%S") if transaction.start_date else '',
            'end_date': transaction.end_date.strftime("%Y-%m-%d %H:%M:%S") if transaction.end_date else '',
            'duration': transaction.duration,
            'total_changes': transaction.total_changes,
            'statements': [{
                'changes': [{
                    'actual_command': change.actual_command,
                    'command_type': change.command_type
                } for change in statement.changes]
            } for statement in transaction.statements]
        } for transaction in list_of_transactions]
    }
    
    return json.dumps(response, ensure_ascii=False)

if __name__ == '__main__':
    bottle.debug(True)

    run(host='localhost', port=8080)
