from StringIO import StringIO
from unittest.case import TestCase

from binlogexplorer.schema_parser import parse_schema_to_column_mapping


class SchamParserTests(TestCase):
    def setUp(self):
        self.schema_file = StringIO("""create table test_table1
                                    (
                                        table1_column_1 int null,
                                        table1_column_2 varchar(20) null
                                    ); 
                                    
                                    create table test_table2
                                    (
                                        table2_column_1 int null, table2_column_2 varchar(20) null, table2_column_3 int null 
                                    );""")

    def test_parse_tables_with_it_columns_indexed_by_order(self):
        result = parse_schema_to_column_mapping(self.schema_file)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result['test_table1']), 2)
        self.assertEqual(result['test_table1'][1], 'table1_column_1')
        self.assertEqual(result['test_table1'][2], 'table1_column_2')
        self.assertEqual(len(result['test_table2']), 3)
        self.assertEqual(result['test_table2'][1], 'table2_column_1')
        self.assertEqual(result['test_table2'][2], 'table2_column_2')
        self.assertEqual(result['test_table2'][3], 'table2_column_3')
