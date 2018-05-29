import os
import os.path
import hashlib
import sqlite3
import itertools
from binascii import hexlify
from collections import namedtuple
from urllib.parse import unquote

from spiderman.normalize import normalize_url

# store hashes hex-encoded out of lazyiness
create_table = '''
    create table if not exists urls (
        url varchar primary key,
        location varchar,
        status_code integer,
        content_type varchar,
        hash char(64)
    )
    '''

class Row(object):

    def __init__(self, url,
            location=None,
            status_code=None,
            content_type=None,
            hash=None,
            ):
        self.url = normalize_url(url)
        self.location = location
        self.status_code = status_code
        self.content_type = content_type
        self.hash = hash

    def __iter__(self):
        yield self.url
        yield self.location
        yield self.status_code
        yield self.content_type
        yield self.hash

    _fields = ('url', 'location', 'status_code', 'content_type', 'hash')

class Storage():

    def __init__(self, db, blob_dir):
        self.blob_dir = blob_dir
        os.makedirs(self.blob_dir, exist_ok=True)
        self.conn = sqlite3.connect(db)
        self.conn.execute(create_table)

    def close(self):
        self.conn.close()

    # assumes no loops
    def resolve_url(self, _url):
        url = normalize_url(_url)
        while True:
            row = self.get_row_by_url(url)
            if row is None or row.location is None:
                return row
            url = row.location

    # assumes no loops
    def unresolve_url(self, url):
        def go(u):
            for row in self.get_rows_by_location(u):
                yield row.url
                yield from go(row.url)
        return frozenset(go(normalize_url(url)))

    def put_row(self, row):
        q = 'insert or replace into urls ({}) values ({})'.format(','.join(Row._fields), ','.join('?' for _ in Row._fields))
        cur = self.conn.cursor()
        cur.execute(q, tuple(row))
        self.conn.commit()

    def get_row_by_url(self, url):
        cur = self.conn.cursor()
        it = cur.execute('select * from urls where url = ?', (normalize_url(url),))
        try:
            return Row(*next(it))
        except StopIteration:
            return None

    def get_rows_by_url_pred(self, pred):
        for row in self.get_all_rows():
            if pred(row.url):
                yield row

    def get_all_rows(self):
        cur = self.conn.cursor()
        it = cur.execute('select * from urls')
        return itertools.starmap(Row, it)

    def blob_path(self, hash):
        return os.path.join(self.blob_dir, hash)

    def put_blob(self, blob):
        h = hashlib.new('sha256')
        h.update(blob)
        hash = hexlify(h.digest()).decode('ascii')
        path = self.blob_path(hash)
        if not os.path.isfile(path):
            with open(path, 'wb') as f:
                f.write(blob)
        return hash

    def get_blob(self, hash, binary=True):
        path = self.blob_path(hash)
        if os.path.isfile(path):
            mode = 'rb' if binary else 'r'
            with open(path, mode) as f:
                return f.read()
        else:
            return None
