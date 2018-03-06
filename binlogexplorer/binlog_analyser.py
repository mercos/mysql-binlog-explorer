class BinlogAnalyser(object):
    def __init__(self, setup):
        self.setup = setup

    def analyse(self, transactions):
        changes_by_identifier = {}
        transactions_by_identifier = {}

        for transaction in transactions:
            for statement in transaction.statements:
                for change in statement.changes:
                    index_of_the_column_with_the_identifier = self.setup['group_identifier'].get(change.table)
                    if index_of_the_column_with_the_identifier:
                        identifier_at_where = change.where_parameters.get(index_of_the_column_with_the_identifier)
                        identifier_at_set = change.set_parameters.get(index_of_the_column_with_the_identifier)
                        identifier = identifier_at_set or identifier_at_where

                        if identifier:
                            transaction.identifiers.add(identifier)
                            changes_by_identifier[identifier] = changes_by_identifier.get(identifier, 0) + 1

        for transaction in transactions:
            for identifier in transaction.identifiers:
                transactions_by_identifier[identifier] = transactions_by_identifier.get(identifier, 0) + 1

        return transactions, {
            'changes_by_identifier': order_by_count(changes_by_identifier),
            'transactions_by_identifier': order_by_count(transactions_by_identifier)
        }


def order_by_count(itens_by_identifier):
    return sorted(itens_by_identifier.iteritems(), key=lambda x: x[1], reverse=True)
