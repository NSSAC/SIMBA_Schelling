import requests
import pandas as pd
import numpy as np


def init():

	urls = []
	with open("../logs/modules.txt", "r") as f:
		for url in f:
			dat = url.split(",")
			urls.append(dat[1]+"{}")
	#url = #"http://udc-aj38-1c0:5000/{}"
	return urls

if __name__ == '__main__':
	urls = init()
	print(urls,flush=True)
	for url in urls:
		print("reset")
		data = requests.get(url.format("reset"))
		print(data,flush=True)
		print("starting ticks")
		tic = 0
		for i in range(100):
			print(tic)	
			tic += 1
			tick = requests.get(url.format("step"))
			print(tick,flush=True)
	#print('Simulating tick %s ...' % str(tick))
	#simulate_one_tick_start_time = time.time()
#    req = requests.get(simulate_one_tick_url, params=payload)
