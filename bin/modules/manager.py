import random
import json
import subprocess
import time
import requests

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def init():
    def start_db():
        '''
        Start and initialize postgres database module

        '''
        sbatch_output = subprocess.check_output(
            ["sbatch", "../bin/modules/POSTGRES/postgres_rundb.sh", "../data/db"])
        job_id = sbatch_output.decode("utf-8").split()[-1]

        job_node = ''
        while job_node == '':
            print('Waiting for a node to be assigned ...', flush=True)
            time.sleep(10)
            squeue_output = subprocess.check_output(
                ["squeue", "-j", job_id, "-o", "%i,%N"])
            squeue_output = squeue_output.decode("utf-8")
            # print(squeue_output)
            assert squeue_output.split('\n')[1].split(',')[0] == job_id
            job_node = squeue_output.split('\n')[1].split(',')[-1]
            print('Database Job Node: {}'.format(job_node), flush=True)

        # Wait until service is ready
        print('Waiting for db to be ready ...', flush=True)
        service_ready_start_time = time.time()

        return job_id, job_node

    def start_service():
        '''
        Start and initailize flask api

        '''
        sbatch_output = subprocess.check_output(
            ["sbatch", "../bin/server.slurm"])
        job_id = sbatch_output.decode("utf-8").split()[-1]

        job_node = ''
        while job_node == '':
            print('Waiting for a node to be assigned ...', flush=True)
            time.sleep(10)
            squeue_output = subprocess.check_output(
                ["squeue", "-j", job_id, "-o", "%i,%N"])
            squeue_output = squeue_output.decode("utf-8")
            # print(squeue_output)
            assert squeue_output.split('\n')[1].split(',')[0] == job_id
            job_node = squeue_output.split('\n')[1].split(',')[-1]
            print('Simulation Service Job Node: {}'.format(job_node), flush=True)

        # Wait until service is ready
        print('Waiting for simulation service to be ready ...', flush=True)
        service_ready_start_time = time.time()
        service_ready_url = "http://{}:5000/".format(job_node)

        return job_id, service_ready_url

        #out = requests.get(service_ready_url+'reset')

        # print(out.json())

    db = start_db()
    service = start_service()

    return db, service


if __name__ == '__main__':
    import json
    import psycopg2
    import db_service as dbs

    db_add, service = init()

    #host = json.load(open('db.status.json','r'))['host']

    #ip = host.split(':')[0]
    # connection = psycopg2.connect(
    #    database="network", user="user", password="pass", host=ip, port="5432")

    db = dbs.db()
    db.create_table('NETWORK', '../data/test.json', from_csv=True, drop=True)

    print(db.read_db('NETWORK'))

    time.sleep(40)

    subprocess.check_output(["scancel", "-b", "-s", "SIGINT", db_add[0]])
    subprocess.check_output(["scancel", service[0]])
