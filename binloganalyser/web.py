import decimal

import bottle
from bottle import route, run, template
import simplejson
from datetime import datetime

from django.utils import datetime_safe

from binlog_parser import BinlogParser

bottle.debug(True)

transactions = BinlogParser().parse(open('tests/examples/binlog-transaction-sample.txt'))


class DateTimeEncoder(simplejson.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if isinstance(o, datetime.datetime):
            d = datetime_safe.new_datetime(o)
            return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(o, datetime.date):
            d = datetime_safe.new_date(o)
            return d.strftime(self.DATE_FORMAT)
        elif isinstance(o, datetime.time):
            return o.strftime(self.TIME_FORMAT)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DateTimeEncoder, self).default(o)


@route('/')
def index():
    return template('main')


@route('/binlog-parser/')
def binlog_parser():
    return {
        "data": [simplejson.dumps(transactions, ensure_ascii=False, for_json=True)]
    }


run(host='localhost', port=8080)
