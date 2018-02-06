from myhdl import always_comb, Signal, intbv, delay, instance, Simulation, bin
from itertools import product


def nand_gate(a, b, out):
    """
    @brief      nand gate implementation

    @param      a     first input intbv signal
    @param      b     second input intbv signal
    @param      out   output intbv signal

    @return     myhdl nand instance

    Chip Name: nand
    Inputs: a, b
    Output: out
    Function: if a=b=1 then out=0 else out=1
    Representation: NOT(a AND b)
    Truth Table:
        | a | b | out |
        |---|---|-----|
        | 0 | 0 |   1 |
        | 0 | 1 |   1 |
        | 1 | 0 |   1 |
        | 1 | 1 |   0 |
    """

    @always_comb  # Required decorator for combinatorial logic
    def logic():
        if a == b == 1:
            out.next = 0
        else:
            out.next = 1

    return logic


def test_nand():

    a, b, out = [Signal(intbv(0)) for i in range(3)]  # Unpacking to intbv(0)

    bin_tups = list(product((0, 1), repeat=2))  # [(0,0), (0,1), (1,0), (1,1)]

    nand_inst = nand_gate(a, b, out)  # Create a nand gate instance

    @instance
    def stimulus():
        for tup in bin_tups:
            a.next, b.next = tup[0], tup[1]
            yield delay(10)  # ?
            print(f'a: {bin(a)} | b:{bin(b)} | out:{bin(out)}')

    return nand_inst, stimulus


tb = Simulation(test_nand())  # Create simulations from myhdl instances
tb.run()  # Run simulation
