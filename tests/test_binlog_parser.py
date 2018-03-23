import os
from StringIO import StringIO
from datetime import datetime
from unittest.case import TestCase

from binlogexplorer.binlog_parser import BinlogParser
from binlogexplorer.schema_parser import parse_schema_to_column_mapping

EXAMPLES_FOLDER = os.path.join(os.path.dirname(__file__), 'examples')


class BinlogParserTests(TestCase):
    def setUp(self):
        self.binlog_parser = BinlogParser()
        self.binlog_file = open(os.path.join(EXAMPLES_FOLDER, 'binlog-transaction-sample.txt'))

    def test_parse_transactions(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        self.assertEqual(3, len(transactions))
        self.assertEqual(datetime(2018, 1, 29, 17, 28, 4), transactions[0].start_date)
        self.assertEqual(datetime(2018, 1, 29, 17, 28, 5), transactions[0].end_date)
        self.assertEqual(1, transactions[0].duration)

        self.assertEqual(1, transactions[0].total_changes)
        self.assertEqual(1, transactions[1].total_changes)
        self.assertEqual(4, transactions[2].total_changes)

        self.assertEqual(1, len(transactions[0].statements))
        self.assertEqual(1, len(transactions[0].statements[0].changes))

        self.assertEqual(1, len(transactions[1].statements))
        self.assertEqual(1, len(transactions[1].statements[0].changes))

        self.assertEqual(3, len(transactions[2].statements))
        self.assertEqual(2, len(transactions[2].statements[2].changes))

    def test_parse_changes(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        changes = transactions[2].statements[2].changes

        self.assertEqual(2, len(changes))
        self.assertIn('UPDATE', changes[0].command_type)
        self.assertEqual('`binlog_analyser`.`test_table`', changes[0].table)
        self.assertIn('UPDATE', changes[1].command_type)
        self.assertEqual('`binlog_analyser`.`test_table`', changes[1].table)
        self.assertEqual(clean_string(
            'UPDATE `binlog_analyser`.`test_table` WHERE @1=1 @2=\'transaction-1\' SET @1=1 @2=\'updated\''),
            clean_string(changes[0].actual_command))
        self.assertEqual(clean_string(
            'UPDATE `binlog_analyser`.`test_table` WHERE @1=2 @2=\'transaction-2\' SET @1=2 @2=\'updated\''),
            clean_string(changes[1].actual_command))

    def test_parse_parameters_of_a_insert_statement(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        insert_change = transactions[0].statements[0].changes[0]
        self.assertIn('INSERT', insert_change.command_type)
        self.assertEqual({1: 1, 2: 'delete-me-1'}, insert_change.set_parameters)
        self.assertEqual({}, insert_change.where_parameters)

    def test_parse_parameters_of_a_delete_statement(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        delete_change = transactions[1].statements[0].changes[0]
        self.assertIn('DELETE', delete_change.command_type)
        self.assertEqual({}, delete_change.set_parameters)
        self.assertEqual({1: 1, 2: 'delete-me-1'}, delete_change.where_parameters)

    def test_parse_parameters_of_a_update_statement(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        update_change = transactions[2].statements[2].changes[0]
        self.assertIn('UPDATE', update_change.command_type)
        self.assertEqual({1: 1, 2: 'updated'}, update_change.set_parameters)
        self.assertEqual({1: 1, 2: 'transaction-1'}, update_change.where_parameters)

    def test_parse_parameters_with_actual_name(self):
        schema = StringIO("""
        create table test_table
        (
            nice_column int null,
            beautiful_column varchar(20) null
        );         
        """)
        binlog_parser = BinlogParser(column_mapping=parse_schema_to_column_mapping(schema))
        transactions = binlog_parser.parse(self.binlog_file)

        update_change = transactions[2].statements[2].changes[0]
        self.assertIn('UPDATE', update_change.command_type)
        self.assertEqual({'nice_column': 1, 'beautiful_column': 'updated'}, update_change.set_parameters)
        self.assertEqual({'nice_column': 1, 'beautiful_column': 'transaction-1'}, update_change.where_parameters)

    def tearDown(self):
        self.binlog_file.close()


def clean_string(string):
    return string.replace('\n', '').replace(' ', '')
