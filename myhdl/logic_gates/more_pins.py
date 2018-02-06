from myhdl import (Signal, intbv, delay, instance,
                   Simulation, bin, StopSimulation, always_comb)
from itertools import product
from math import log2


def mul_demux(sel, ip, op):
    """
    forwards single input to one of `2**n` output through `n` select lines

    :param      sel:  select pin
    :param      out:  output
    :param      ip:   array of equal sized inputs
    :type       sel:  intbv Signal
    :type       out:  intbv Signal
    :type       ip:   list

    :returns:   (ip₁ ⋅ S̄₁ ⋅ .. ⋅ S̄ₙ) ⋅ .. ⋅ (ipₙ ⋅ S₁ ⋅ .. ⋅ Sₙ)
    :rtype:     myhdl always_comb instance
    """
    if len(op) != 2 ** len(sel.val):
        raise StopSimulation(f'{log2(len(op))}number of selectors required')

    @always_comb
    def logic():
        for i in range(len(op)):
                op[i].next = ip if i == sel else 0

    return logic


ip = Signal(intbv('101')[3:])
op = [Signal(intbv(0)[3:]) for x in range(8)]
sel = Signal(intbv(0)[3:])

bin_product = [''.join(x) for x in list(product('01', repeat=3))]
gate_inst = mul_demux(sel, ip, op)


@instance
def stimulus():
    for num in bin_product:
        sel.next = intbv(num)
        yield delay(10)
        print(
            f'ip: {bin(ip, 3)} | sel: {bin(sel, 3)} | \
            \nout:{[bin(out, 3) for out in op]}')


sim = Simulation(gate_inst, stimulus)
sim.run()
