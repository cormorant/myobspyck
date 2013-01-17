# -*- coding: utf-8 -*-
"""
some code about path, database, connestions, ...
"""
#import sys
try:
    import psycopg2
except ImportError:
    print("Database connection will not work. No psycopg2 package installed! Aborting.")
    #sys.exit(1)


DATA_DIR = "seisobr"

DB_OPTIONS = {
    'host': '172.16.200.1',
    'database': 'seisobr',
    'user': 'pguser',
    'password': 'my_password',
}

SELECT_CODES = """\
SELECT "prnbase01_prns"."idPrn", "prnbase01_prnsdir"."Path", "prnbase01_prns"."seisFile"
FROM "prnbase01_prns"
INNER JOIN "prnbase01_prnsdir"
ON "prnbase01_prnsdir"."idDir" = "prnbase01_prns"."idDir"
WHERE "prnbase01_prns"."idDir" = %s
ORDER BY 1;\
"""

SELECT_WAVES = """\
SELECT "prnbase01_prnswaves"."NameWave", "prnbase01_prnswaves"."TimeWave",
    "prnbase01_prnswaves"."idWave"
FROM "prnbase01_prnswaves"
INNER JOIN "prnbase01_prns"
ON "prnbase01_prns"."idPrn" = "prnbase01_prnswaves"."idPrn"
WHERE "prnbase01_prnswaves"."idPrn" = %s
AND "prnbase01_prnswaves"."NameWave" NOT LIKE '__m'
;\
"""
#--AND "seisobr_prnswaves"."NameWave" NOT LIKE '%m'
#--where letter "m" is not in NameWave

UPDATE_WAVES = 'UPDATE "prnbase01_prnswaves" SET "TimeWave"=%s WHERE "idWave"=%s;'


def execute_query(cursor, query, params):
    """ ищем записи """
    try:
        cursor.execute(query, tuple(params,))
    except psycopg2.Error, msg:
        print("An error ocured while executing query:", msg)
        #return []
    else:
        return cursor.fetchall()


def setup_db_connection():
    conn_string = "host='%(host)s' dbname='%(database)s' user='%(user)s' password='%(password)s'" % DB_OPTIONS
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError, msg:
        print("Error connecting to database with problem:", msg)
        #sys.exit(1)
    cursor = conn.cursor()
    return (conn, cursor)
