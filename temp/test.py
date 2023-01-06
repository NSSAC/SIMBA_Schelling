import psycopg2
import pandas as pd
import csv
import json


def csv_to_db(path, table, drop=True):
    f = open('db.status.json', 'r')
    host = json.load(f)['host']

    ip = host.split(':')[0]
    conn = psycopg2.connect(
        database="test_db", user="testuser", password="testpass", host=ip, port="5432")

    with open(path, 'r') as file:
        data = csv.reader(file)
        headers = next(data)
        cur = conn.cursor()
        if drop:
            drop_table = '''DROP TABLE IF EXISTS {}'''.format(table)
            cur.execute(drop_table)

        create_table = '''CREATE TABLE IF NOT EXISTS {}
          (ID INT PRIMARY KEY     NOT NULL,
          "{}"           TEXT    NOT NULL,
          "{}"         REAL); '''.format(table, headers[1], headers[2])

        print(create_table)
        cur.execute(create_table)

        conn.commit()
        #print('created db')

        #cur = conn.cursor()
        cur.execute("SELECT * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='NETWORK'")
        record = cur.fetchall()
        print(record, cur.rowcount)

        for row in data:
            print(row)
            cur.execute('''INSERT INTO {} (ID,"{}","{}") \
                     VALUES ({}, {}, {})'''.format(table, headers[1], headers[2], row[0], row[1], row[2]))

        conn.commit()
    #cur = conn.cursor()
    #cur.execute("SELECT * from NETWORK")
    #record = cur.fetchall()
    #print(record, cur.rowcount)

    return conn


def conn_db():
    f = open('db.status.json', 'r')
    host = json.load(f)['host']

    ip = host.split(':')[0]
    conn = psycopg2.connect(
        database="test_db", user="testuser", password="testpass", host=ip, port="5432")
    return conn


def read_db(conn, table, df=True):
    cur = conn.cursor()
    cur.execute("SELECT * from {}".format(table))
    record = cur.fetchall()
    print(pd.DataFrame(record))


if __name__ == '__main__':
    table = "NETWORK"
    conn = csv_to_db('../temp/test.csv', table)
    conn = conn_db()
    read_db(conn, table)
