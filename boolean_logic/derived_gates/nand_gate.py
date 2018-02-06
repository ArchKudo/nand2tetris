"""
MyHdl description for nand gate
"""

from myhdl import always_comb, Signal


def nand_gate(a: Signal, b: Signal, out: Signal) -> always_comb:
    """
    nand gate implementation

    :param      a:    Input intbv signal
    :param      b:    Input intbv Signal
    :param      out:  Output intbv Signal
    :type       a:    Signal
    :type       b:    Signal
    :type       out:  Signal

    :returns:   Combinatorial logic for nand gate
    :rtype:     always_comb
    """
    @always_comb
    def logic():
        if a == b == 1:
            out.next = 0
        else:
            out.next = 1

    return logic
