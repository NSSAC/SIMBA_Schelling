import random
import json
import subprocess
import time
import requests

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def init(modules):
    def start_db():
        '''
        Start and initialize postgres database module
	Returns: slurm address, id

        '''
        sbatch_output = subprocess.check_output(
            ["sbatch", "../simba/modules/POSTGRES/postgres_rundb.sh", "../data/db"])
        job_id = sbatch_output.decode("utf-8").split()[-1]

        job_node = ''
        while job_node == '':
            print('Waiting for a node to be assigned ...', flush=True)
            time.sleep(10)
            squeue_output = subprocess.check_output(
                ["squeue", "-j", job_id, "-o", "%i,%N"]) 		#check queue and await run
            squeue_output = squeue_output.decode("utf-8")
            # print(squeue_output)
            assert squeue_output.split('\n')[1].split(',')[0] == job_id
            job_node = squeue_output.split('\n')[1].split(',')[-1]
            print('Database Job Node: {}'.format(job_node), flush=True)

        # Wait until service is ready
        print('Waiting for db to be ready ...', flush=True)
        service_ready_start_time = time.time()

        return job_id, job_node

    def start_service(module):
        '''
        Start and initailize flask api
	Returns: slurm address, id

        '''
        sbatch_output = subprocess.check_output(
            ["sbatch", "../simba/server.slurm", str(module)])

        job_id = sbatch_output.decode("utf-8").split()[-1]

        job_node = ''
        while job_node == '':
            print('Waiting for a node to be assigned for {} ...'.format(
                module), flush=True)
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

        print("HTTP endpoint:", service_ready_url, flush=True)

        f = open("modules.txt", "a")
        f.write("{},{}".format(module, service_ready_url))
        f.close()

        return job_id, service_ready_url

        #out = requests.get(service_ready_url+'reset')

        # print(out.json())

    f = open("modules.txt", "w")
    f.write("")
    f.close()

    services = []
    db = start_db()
    #modules = ["example_module"]
    for module in modules:
        try:
            services.append(start_service(module['path']))
        except AssertionError as msg:
            print(msg)
            subprocess.check_output(["scancel", "-b", "-s", "SIGINT", db[0]])
            exit()
    return db, services


if __name__ == '__main__':
    import json
    import psycopg2
    import sys
    #import db_service as dbs

    #print(sys.argv)
    #init(sys.argv[1])
    #modules = ['/home/sms8fr/simba_schelling/schelling/enviroment']
    
    #modules = [sys.argv[1]]
    #{'modules': {'schelling': {'path': 'schelling/enviornment.py', 'priority': 0}}}
    #print(sys.argv)
    modules = json.load(open(sys.argv[1],'r'))['modules'].values()
    #path = sys.argv[1]
    db_add, services = init(modules)

    #host = json.load(open('db.status.json','r'))['host']

    #ip = host.split(':')[0]
    # connection = psycopg2.connect(
    #    database="network", user="user", password="pass", host=ip, port="5432")

    #db = dbs.db()
    #db.create_table('NETWORK', '../schema/test.json', from_csv=True, drop=True)

    # print(db.read_db('NETWORK'))

    time.sleep(500)

    subprocess.check_output(["scancel", "-b", "-s", "SIGINT", db_add[0]])
    for service in services:
        subprocess.check_output(["scancel", service[0]])
