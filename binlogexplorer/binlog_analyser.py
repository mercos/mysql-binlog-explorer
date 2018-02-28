class BinlogAnalyser(object):
    def __init__(self, setup):
        self.setup = setup

    def analyse(self, transactions):
        total_changes_by_id = {}

        for transaction in transactions:
            for statement in transaction.statements:
                for change in statement.changes:
                    index_of_the_column_with_the_identifier = self.setup['group_identifier'].get(change.table)
                    if index_of_the_column_with_the_identifier:
                        identifier_at_where = change.where_parameters.get(index_of_the_column_with_the_identifier)
                        identifier_at_set = change.set_parameters.get(index_of_the_column_with_the_identifier)
                        identifier = identifier_at_set or identifier_at_where

                        if identifier:
                            total_changes_by_id[identifier] = total_changes_by_id.get(identifier, 0) + 1

        return total_changes_by_id
