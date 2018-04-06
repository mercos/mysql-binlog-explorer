from unittest import TestCase

from binlogexplorer.binlog_analyser import BinlogAnalyser
from binlogexplorer.binlog_parser import Transaction, Statement, Change


class BinlogAnalyserTests(TestCase):
    def test_group_changes_by_identifier(self):
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
                           where_parameters={1: 999}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 999}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 100}, set_parameters={1: 100}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={}, set_parameters={1: 999})
                ])
            ])
        ]

        transactions, report = BinlogAnalyser(group_identifier=1).analyse(transactions)

        self.assertEqual(transactions[0].identifiers, {100, 999})
        self.assertEqual(set(report['changes_by_identifier']), set([
            (999, 4),
            (100, 6),
        ]))

    def test_group_transactions_by_identifier(self):
        transactions = [
            Transaction(statements=[
                Statement(changes=[
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 100}, set_parameters={}),
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 999}, set_parameters={}),
                ])
            ]),
            Transaction(statements=[
                Statement(changes=[
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 999}, set_parameters={}),
                ])
            ]),
            Transaction(statements=[
                Statement(changes=[
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 100}, set_parameters={}),
                ])
            ]),
            Transaction(statements=[
                Statement(changes=[
                    Change(table='`binlog_analyser`.`a_table`',
                           where_parameters={1: 999}, set_parameters={}),
                ])
            ]),
        ]

        transactions, report = BinlogAnalyser(group_identifier=1).analyse(transactions)

        self.assertEqual(report['transactions_by_identifier'], [
            (999, 3),
            (100, 2),
        ])
