from MAIN.module import environment

class enviornment(environment):
	
	def __init__(self):
		print(1)

	
	def reset(self):
		self.state = self.__get_state__()
		print(self.state)
		return self.state

	def step(self):
		return 1

	




if __name__ == '__main__':
	env = environment()
	env.reset()
