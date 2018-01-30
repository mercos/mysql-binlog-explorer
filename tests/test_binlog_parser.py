from datetime import datetime
from unittest.case import TestCase

from binloganalyser.binlog_parser import BinlogParser


class BinlogParserTests(TestCase):
    def setUp(self):
        self.binlog_parser = BinlogParser()
        self.binlog_file = open('examples/binlog-transaction-sample.txt')

    def test_parse_transactions(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        self.assertEqual(3, len(transactions))
        self.assertEqual(datetime(2018, 1, 29, 17, 28, 4), transactions[0].start_date)
        self.assertEqual(datetime(2018, 1, 29, 17, 28, 5), transactions[0].end_date)
        self.assertEqual(1, transactions[0].duration)
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
        self.assertIn("""UPDATE `binlog_analyser`.`test_table`
WHERE
  @1=1 /* INT meta=0 nullable=1 is_null=0 */
  @2='transaction-1' /* VARSTRING(60) meta=60 nullable=1 is_null=0 */
SET
  @1=1 /* INT meta=0 nullable=1 is_null=0 */
  @2='updated' /* VARSTRING(60) meta=60 nullable=1 is_null=0 */""", changes[0].actual_command)
        print(transactions[0])
        print(transactions[1])
        print(transactions[2])

    def test_print_transaction(self):
        transactions = self.binlog_parser.parse(self.binlog_file)

        self.assertEqual('Transaction 2018-01-29 17:28:04 (duration: 1)', str(transactions[0]))
        self.assertEqual('Transaction 2018-01-29 17:28:09 (duration: 2)', str(transactions[2]))

    def tearDown(self):
        self.binlog_file.close()
