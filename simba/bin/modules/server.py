import random 
import flask
import json
import sys
import db_service as dbs
import importlib

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

app = flask.Flask(__name__)

def init(path):
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

	#module = ".....schelling.enviroment"
	#module = __import__(module, fromlist=["environment"])
	#environment = getattr(module, "environment")
	
	#../simba/bin/modules/
	import importlib.util
	import sys
	spec = importlib.util.spec_from_file_location("environment", "{}.py".format(path))
	
	foo = importlib.util.module_from_spec(spec)
	sys.modules["environment"] = foo
	spec.loader.exec_module(foo)
	env = foo.environment()

	#environment = importlib.import_module("..modules..bin..simba..simba_schelling." + module, "environment")
	#env = environment()
	
	db = dbs.db()
	tick = 0
	status = "INIT"

def write_state(data):
	'''
	param::data - data to write to state
	'''
	global db
	db.write_db("STATE", data)

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
	staus = "RUNNING"
	#state = env.reset()
	write_state(env.reset())
	return(output())

@app.route('/step', methods=['GET'])
def step():
	global env
	state = get_state()
	write_state(env.step(state))

	return(output())


if __name__ == '__main__':
	print(sys.argv)	
	init(sys.argv[1])
	app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


