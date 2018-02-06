import myhdl

def clk_driver(clk):
	half_period = myhdl.delay(10)

	@myhdl.always(half_period)
	def drive_clk():
		clk.next = not clk

	return drive_clk

def hello_concurrency(clk):
	@myhdl.always(clk.posedge)
	def say_hello():
		print(f'{myhdl.now()}: Hello!')

	return say_hello

clk = myhdl.Signal(0)
clk_drv_inst = clk_driver(clk)
hello_conc_inst = hello_concurrency(clk)
sim = myhdl.Simulation(clk_drv_inst, hello_conc_inst)
sim.run(100)
