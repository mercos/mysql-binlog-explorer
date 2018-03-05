import json
import os
import sys

import bottle
from bottle import route, run, template, static_file

from binlog_analyser import BinlogAnalyser
from binlog_parser import BinlogParser

CURRENT_DIRECTORY = os.path.join(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIRECTORY, 'template')
STATIC_DIR = os.path.join(CURRENT_DIRECTORY, 'static')

bottle.debug(True)
bottle.TEMPLATE_PATH = [TEMPLATE_DIR]


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=STATIC_DIR)


@route('/images/<filename>')
def server_images(filename):
    return server_static(filename)


@route('/')
def index():
    return template('main')


@route('/binlog-parser/')
def binlog_parser():
    return binlog_parser_presenter(transactions)


def binlog_parser_presenter(list_of_transactions):
    response = {
        'data': [{
            'start_date': transaction.start_date.strftime("%Y-%m-%d %H:%M:%S") if transaction.start_date else '',
            'end_date': transaction.end_date.strftime("%Y-%m-%d %H:%M:%S") if transaction.end_date else '',
            'duration': transaction.duration,
            'identifiers': ' '.join(map(lambda identifier: '({})'.format(identifier), transaction.identifiers)),
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


def main():
    if len(sys.argv) <= 1:
        print("Usage: mysql-binlog-explorer <binlog.file1> <binlog.file2> <binlog.file...N>")
        exit(1)

    global transactions
    transactions = []
    files = sys.argv[1:]

    for binlog_file in files:
        print('Parsing {}...'.format(binlog_file))
        with open(binlog_file) as content:
            transactions += BinlogParser().parse(content)
            transactions = identify_transactions(transactions)

    run(host='localhost', port=8080)


def identify_transactions(transactions):
    if not os.path.exists('schema_mapping.json'):
        return transactions

    with open('schema_mapping.json') as mapping:
        setup = json.load(mapping)
        transactions_with_identifier, result = BinlogAnalyser(setup).analyse(transactions)
        itens = sorted(result.iteritems(), key=lambda x: x[1], reverse=True)
        for key, value in itens:
            print(key, value)

        return transactions_with_identifier


if __name__ == '__main__':
    main()
