import json

import bottle
from bottle import route, run, template

from binlog_parser import BinlogParser


@route('/')
def index():
    return template('main')


@route('/binlog-parser/')
def binlog_parser():
    return {
        "data": [simplejson.dumps(transactions, ensure_ascii=False, for_json=True)]
    }


run(host='localhost', port=8080)
