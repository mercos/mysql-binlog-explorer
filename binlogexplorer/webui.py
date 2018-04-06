import argparse
import json
import os

import bottle
import simplejson
from bottle import route, run, template, static_file

from binlog_analyser import BinlogAnalyser
from binlog_parser import BinlogParser
from schema_parser import parse_schema_to_column_mapping

CURRENT_DIRECTORY = os.path.join(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIRECTORY, 'template')
STATIC_DIR = os.path.join(CURRENT_DIRECTORY, 'static')
VERSION_FILE = os.path.join(CURRENT_DIRECTORY, 'version')

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


@route('/binlog-parser/analysis')
def binlog_analysis():
    return simplejson.dumps(analysis)


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


def parse_cli_arguments():
    cli = argparse.ArgumentParser(description='Parses MySQL binlogs')
    cli.add_argument('files', type=file, nargs='+', help='binlog files to proccess')
    cli.add_argument('--schema-ddl', type=file, dest='schema_ddl', help='.ddl file with the \'create\' statements to '
                                                                        'figure out the name of the columns.')
    cli.add_argument('--tenant-identifier', dest='group_identifier', help='name of the column that identify tenant')
    cli.add_argument('-v', '--version', action='version', version=get_version())

    cli = cli.parse_args()
    return cli


def get_version():
    with open(VERSION_FILE) as version:
        return version.read().strip()


def main():
    global transactions
    global analysis

    cli = parse_cli_arguments()

    column_mapping = parse_schema_to_column_mapping(cli.schema_ddl) if cli.schema_ddl else {}
    parser = BinlogParser(column_mapping)
    analyser = BinlogAnalyser(cli.group_identifier)

    transactions = []
    for binlog_file in cli.files:
        print('Parsing {}...'.format(binlog_file.name))
        with binlog_file as content:
            transactions += parser.parse(content)
            _, analysis = analyser.analyse(transactions)

    run(host='localhost', port=8080)


if __name__ == '__main__':
    main()
