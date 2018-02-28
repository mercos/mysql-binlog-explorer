from unittest import TestCase

from binlogexplorer.binlog_analyser import BinlogAnalyser
from binlogexplorer.binlog_parser import Transaction, Statement, Change


class BinlogAnalyserTests(TestCase):
    def setUp(self):
        self.setup = {}
        self.binlog_analyser = BinlogAnalyser(self.setup)

    def test_group_changes_by_identifier(self):
        self.setup['group_identifier'] = {
            '`binlog_analyser`.`a_table`': 1
        }

        transactions = [
            Transaction(statements=[
                Statement(changes=[
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={}, set_parameters={1: 100}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 100}, set_parameters={}),
                    Change(table='`binlog_analyser`.`other_table`',
                           where_parameters={}, set_parameters={1: 100}),
                    Change(table='`binlog_analyser`.`other_table`',
                           where_parameters={1: 100}, set_parameters={}),
                    Change(table='`binlog_analyser`.`not_included_table`',
                           where_parameters={1: 100}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 999}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 100}, set_parameters={1: 100}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={}, set_parameters={1: 999})
                ])
            ])
        ]

        result = self.binlog_analyser.analyse(transactions)

        self.assertEqual(result, {
            100: 3,
            999: 2
        })
