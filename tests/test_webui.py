from unittest.case import TestCase

from datetime import datetime

from binlogexplorer.binlog_parser import Transaction, Statement, Change
from binlogexplorer.webui import binlog_parser_presenter


class WebTests(TestCase):
    def test_convert_list_of_transaction_to_dict(self):
        transactions = [
            Transaction(
                datetime(2018, 1, 1, 12, 1, 1),
                datetime(2018, 1, 1, 12, 1, 2),
                [
                    Statement([
                        Change('UPDATE', 'UPDATE SHU SET X = 1')
                    ])
                ]
            )
        ]

        result = binlog_parser_presenter(transactions)
        
        self.assertEqual(1, len(result['data']))
        self.assertEqual(datetime(2018, 1, 1, 12, 1, 1), result['data'][0]['start_date'])
        self.assertEqual(datetime(2018, 1, 1, 12, 1, 2), result['data'][0]['end_date'])
        self.assertEqual(1, len(result['data'][0]['statements']))
        self.assertEqual(1, len(result['data'][0]['statements'][0]['changes']))
        self.assertEqual('UPDATE', result['data'][0]['statements'][0]['changes'][0]['command_type'])
        self.assertEqual('UPDATE SHU SET X = 1', result['data'][0]['statements'][0]['changes'][0]['actual_command'])
