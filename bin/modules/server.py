import random 
import flask
import json

from module import environment

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

app = flask.Flask(__name__)
global env

def init():
	global env
	env = environment()


@app.route('/', methods=['GET'])
def main():
    return "OK" 

@app.route('/reset', methods=['GET'])
def reset():
	global env
	return(env.reset())

@app.route('/step', methods=['GET'])
def step():
	global env
	return(env.step())


if __name__ == '__main__':
	init()
	app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


