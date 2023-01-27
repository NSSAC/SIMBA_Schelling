import psycopg2
import pandas as pd
import csv
import json


class db:
    def __init__(self):
        '''
        ESTABLISH db connection
        '''
        f = open('db.status.json', 'r')
        host = json.load(open('db.status.json', 'r'))['host']
        ip = json.load(open('db.status.json', 'r'))['host'].split(':')[0]

        self.CONNECTION = psycopg2.connect(
            database="test_db",
            user="testuser",
            password="testpass",
            port="5432",
            host=json.load(open('db.status.json', 'r'))['host'].split(':')[0])

        self.CURSOR = self.CONNECTION.cursor()

        try:
            with open('db_schema.json', 'r') as f:
                data = json.load(f)
                self.HEADERS = data['headers']
                self.IDX = data['idx']

                print(self.HEADERS, self.IDX, flush=True)
        except:
            self.HEADERS = {}
            self.IDX = {}

    def create_table(self, name, schema, from_csv=False, drop=False):
        '''
        CREATE table from schema
        param:name     -   name of table
        param:schema   -   schema path
        param:from_csv -   create table from existing csv file
        param:drop     -   drop table if exists
        '''

        if drop:
            self.CURSOR.execute('''DROP TABLE IF EXISTS {}'''.format(name))

        #name = "TEST"
        schema = json.load(open(schema, 'r'))
        headers = schema['modules']
        columns = []

        for header in headers:
            columns.append(headers[header]['columns'])

        query = '''CREATE TABLE IF NOT EXISTS {}
            (ID INT PRIMARY KEY     NOT NULL,
            {}
            );
           '''
        body = ''
        columns = []
        for header in headers:
            # print(headers[header])
            for column in headers[header]['columns'].items():
                # print(column)
                body += '{}     {}    NOT NULL,'.format(column[0], column[1])
                columns.append(column[0])
        self.CURSOR.execute(query.format(name, body[:-1]))

        self.IDX[name] = 0
        self.HEADERS[name] = columns
        print(self.HEADERS[name], "header", flush=True)

        with open("db_schema.json", "w") as f:
            write = {"headers":self.HEADERS, "idx":self.IDX}
            out = json.dumps(write, indent=4)
            f.write(out)

        if from_csv:
            data = csv.reader(open(schema['path'], 'r'))
            self.HEADERS[name] = next(data)

            for idx, row in enumerate(data):
                self.CURSOR.execute(
                    '''INSERT INTO {} (ID,{})
        	       VALUES {}'''.format(
                        name,
                        str(tuple(headers.keys()))[1:-1].replace("'", ""),
                        str(tuple(row)).replace("'", "")))

            self.IDX[name] = idx

        self.CONNECTION.commit()

    def add(self, name, data):
        '''
        METHOD for adding data to table
        param:name  -  table to add to
        param:data  -  data to add
        '''
        if isinstance(data, pd.DataFrame):
            for idx, row in data.iterrows():
                print(self.IDX, "idx", flush=True)
                self.IDX[name] += 1

                self.CURSOR.execute('''
                    INSERT INTO {} (ID, {})
                    VALUES ({}, {})'''.format(
                    name,
                    str(tuple(data.columns))[1:-1].replace("'", ""),
                    str(self.IDX[name] + 1),
                    str(tuple(row))[1:-1]))

    def read_db(self, name, df=True):
        '''
        METHOD for selecting data from table
        param:name  -  table to select from
        param:pd    -  return as pd dataframe
        '''

        self.CURSOR.execute('SELECT * FROM {}'.format(name))
        if df:
            #print(self.HEADERS, "header2", flush=True)
            data = self.CURSOR.fetchall()
            print(data, flush=True)
            return(pd.DataFrame(data, index=None, columns=self.HEADERS[name]).set_index(""))
        return self.CURSOR.fetchall()


if __name__ == '__main__':
    dbs = db()
    dbs.create_table('NETWORK', 'data/config.json', from_csv=True, drop=True)
    # print(dbs.read_db('INFORMATION_SCHEMA.COLUMNS where TABLE_NAME="NETWORK"')
    print(dbs.read_db("INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='NETWORK'", df=False))
    dbs.add('NETWORK', pd.DataFrame({'a': [0, 2, 3], 'b': [3, 2, 1]}))
    print(dbs.read_db('NETWORK'))
