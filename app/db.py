import mariadb
from flask import g, abort
import os

dbconfig = {
    "host": os.environ.get("HOST") or "127.0.0.1",
    "port": 3306,
    "user": "foo",
    "password": "secret",
    "database": "bike",
}


def get_db():
    if "db" not in g:
        g.db = mariadb.connect(**dbconfig, autocommit=True)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        print("Closing database")
        db.close()


# Returns PER_PAGE length list of bike stations or journeys. Also returns total amount of rows in either table
def get_result_set_and_count(query, offset, per_page, phrase=None):
    journeys = []
    count = 0
    try:
        cur = get_db().cursor()

        if phrase == None:
            cur.execute(query, (offset, per_page))
            for i in cur:
                journeys.append(i)
            cur.execute("SELECT FOUND_ROWS()")
            for i in cur:
                count = i[0]
        else:
            cur.execute(query, (phrase, offset, per_page))
            for i in cur:
                journeys.append(i)
            cur.execute("SELECT FOUND_ROWS()")
            for i in cur:
                count = i[0]

    except mariadb.Error as e:
        print(f"Error: {e}")
        return abort(500, "Query didn't succeed. Try a little later.")

    close_db()
    return journeys, count
