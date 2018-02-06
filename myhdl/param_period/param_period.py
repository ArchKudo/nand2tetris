from myhdl import Signal, delay, instance, always, now, Simulation

def clk_driver(clk, period=20):

	low = period // 2
	high = period - low

	@instance
	def drive_clk():
		while True:
			yield delay(low)
			clk.next = 1
			yield delay(high)
			clk.next = 0

	return drive_clk

def hello(clk, msg='Hello'):
	@always(clk.negedge)
	def say_hello():
		print(f'{now()}: {msg}')

	return say_hello

clk = Signal(0)
cdr1 = clk_driver(clk, period=5)
cdr2 = clk_driver(clk, period=13)
hello_inst = hello(clk)
hola_inst = hello(clk, msg='Hola')
sim = Simulation(cdr1, hello_inst, cdr2, hola_inst)
sim.run(100)
