import json
from unittest.case import TestCase

from datetime import datetime

from binlogexplorer.binlog_parser import Transaction, Statement, Change
from binlogexplorer.webui import binlog_parser_presenter


class WebTests(TestCase):
    def test_convert_list_of_transactions_to_dict(self):
        transactions = [
            Transaction(
                datetime(2018, 1, 1, 12, 1, 1),
                datetime(2018, 1, 1, 12, 1, 2),
                {111, 222, 333},
                [
                    Statement([
                        Change('UPDATE', actual_command='UPDATE SHU SET X = 1')
                    ])
                ]
            )
        ]

        result = json.loads(binlog_parser_presenter(transactions))
        
        self.assertEqual(1, len(result['data']))
        transaction = result['data'][0]
        self.assertEqual(transaction['identifiers'], '(333) (222) (111)')
        self.assertEqual('2018-01-01 12:01:01', transaction['start_date'])
        self.assertEqual('2018-01-01 12:01:02', transaction['end_date'])
        self.assertEqual(1, len(transaction['statements']))
        self.assertEqual(1, len(transaction['statements'][0]['changes']))
        self.assertEqual('UPDATE', transaction['statements'][0]['changes'][0]['command_type'])
        self.assertEqual('UPDATE SHU SET X = 1', transaction['statements'][0]['changes'][0]['actual_command'])
