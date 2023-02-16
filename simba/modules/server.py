import random
import flask
import json
import sys
import db_service as dbs
import importlib
import pandas as pd
import time

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

app = flask.Flask(__name__)


def init(path, data_path):
    '''
    param::module - python based enviornment to import


    establish database connection
    set environment status to initialized
    initialize environment
    '''

    global status
    global db
    global tick
    global env
    global state
    global lastTime

    #module = ".....schelling.enviroment"
    #module = __import__(module, fromlist=["environment"])
    #environment = getattr(module, "environment")

    # ../simba/bin/modules/
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location(
        "environment", "{}".format(path))

    foo = importlib.util.module_from_spec(spec)
    sys.modules["environment"] = foo
    spec.loader.exec_module(foo)
    env = foo.environment(data_path)

    #environment = importlib.import_module("..modules..bin..simba..simba_schelling." + module, "environment")
    #env = environment()

    db = dbs.db()
    tick = 0
    state = pd.DataFrame
    status = "INIT"
    lastTime = time.time()

def write_state(data):
    '''
    param::data - data to write to state
    '''
    global db
    db.add("STATE", data)


def get_state():
    '''
    get current state from database module
    '''

    global db
    return db.read_db("STATE")


def output():
    '''
    return status and tick number 
    error check
    '''
    global tick
    global status

    tick += 1
    return({'status': status, 'output': [str(tick)]})


@app.route('/', methods=['GET'])
def main():
    return "OK"


@app.route('/reset', methods=['GET'])
def reset():
    global env
    global status
    global state
    global lastTime
   
    staus = "RUNNING"
    lastTime = time.time() 
    state = env.reset()
    #print(state,"state", flush=True)
    #write_state(state)
    state.to_csv('reset.csv',mode='a')
    print("time to reset:", time.time() - lastTime, flush=True)
    return(output())


@app.route('/step', methods=['GET'])
def step():
    global env
    global state
    global lastTime
    #print(state,"this is the state", flush=True)#state = get_state()
    #write_state(env.step(state))
    lastTime = time.time()
    state = env.step(state)
    print("Time to step:",time.time() - lastTime,flush=True)
    state.to_csv('step.csv', mode='a')
    pd.DataFrame([]).to_csv('step.csv',mode='a')
    return(output())


if __name__ == '__main__':
    print(sys.argv[1])
    init(sys.argv[1], sys.argv[2])
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
