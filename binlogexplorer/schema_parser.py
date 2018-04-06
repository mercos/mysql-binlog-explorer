import re
from string import strip


def parse_schema_to_column_mapping(schema_file):
    contents = schema_file.read()
    raw_tables = re.findall('create table(.*?);', contents, re.DOTALL)
    tables = {}
    for raw_table in raw_tables:
        columns_start = raw_table.index('(')
        table_name = raw_table[:columns_start].strip()
        columns = __remove_commas_from_column_type_declaration(columns_start, raw_table)
        columns = map(strip, columns.split(','))
        columns = map(lambda column_raw: column_raw.split(' ')[0], columns)
        tables[table_name] = dict(zip(range(1, len(columns) + 1), columns))

    return tables


def __remove_commas_from_column_type_declaration(columns_start, raw_table):
    return re.sub(',\d', '', raw_table[columns_start + 1:])
