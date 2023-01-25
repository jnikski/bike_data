import mariadb
from flask import current_app, g

dbconfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'foo',
    'password': 'secret',
    'database': 'bike'
}

def get_db():
    if 'db' not in g:
        print(g)
        g.db = mariadb.connect(**dbconfig).cursor()
    return g.db

def close_db(e=None):
    db = g.pop('db',  None)
    print(f'GGGGGGG: {g}')
    print(f'db: {db}')
    if db is not None:
        print('Closing database')
        db.close()