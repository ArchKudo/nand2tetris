import myhdl

def hello_world():
	interval = myhdl.delay(10)

	@myhdl.always(interval)
	def say_hello():
		print(f'{myhdl.now()}: Hello!')

	return say_hello

instance = hello_world()
sim = myhdl.Simulation(instance)
sim.run(50)
