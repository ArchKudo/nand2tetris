"""
Hardware description for logic gates
"""
from myhdl import always_comb, StopSimulation
from math import log2


def and_gate(a, out):
    """
    and gate returns 1 only if all the inputs are 1 else 0

    :param      a:    bit array of input
    :param      out:  output of gate
    :type       a:    intbv Signal
    :type       out:  intbv Signal

    :returns:   (a₀ & a₁ & a₂ & .. & aₙ)
    :rtype:     myhdl always_comb() instance
    """
    @always_comb
    def logic():
        for i in range(len(a.val)):
            if a[i] == 0:
                out.next = 0
                break
        else:
            out.next = 1

    return logic


def or_gate(a, out):
    """
    or gate returns 1 when atleast one of its input is 1, 0 otherwise

    :param      a:    bit array of input
    :param      out:  output of gate
    :type       a:    intbv Signal
    :type       out:  intbv Signal

    :returns:   (a₀ || a₁ || a₂ || .. || aₙ)
    :rtype:     myhdl always_comb() instance
    """
    @always_comb
    def logic():
        for i in range(len(a.val)):
            if a[i] == 1:
                out.next = 1
                break
            else:
                out.next = 0

    return logic


def not_gate(a, out):
    """
    not gate returns inverted value of input

    :param      a:    bit array of input
    :param      out:  output of gate
    :type       a:    intbv Signal
    :type       out:  intbv Signal

    :returns:   not applied to individual bits of a
    :rtype:     myhdl always_comb() instance
    """
    @always_comb
    def logic():
        for i in range(len(a.val)):
            if a[i] == 0:
                out.next[i] = 1
            else:
                out.next[i] = 0

    return logic


def xor_gate(a, out):
    """
    xor gate returns 1 only when exactly one of its input bit is 1

    :param      a:    bit array of input
    :param      out:  output of gate
    :type       a:    intbv Signal
    :type       out:  intbv Signal

    :returns:   a =1
    :rtype:     myhdl always_comb() instance

    Note: xor doesn't make sense for more than two input use parity instead
    See: https://electronics.stackexchange.com/a/93719
    """
    @always_comb
    def logic():
        count = 0
        for i in range(len(a.val)):
            if a[i] == 1:
                count += 1
        if count == 1:
            out.next = 1
        else:
            out.next = 0

    return logic


def odd_parity(a, out):
    """
    checks odd parity i.e returns 1 for odd number of 1 in input
    is equivalent to xor when number of input bits is two

    :param      a:    bit array of input
    :param      out:  output of gate
    :type       a:    intbv Signal
    :type       out:  intbv Signal

    :returns:   (aₒ ⊕ a₁ ⊕ a₂ ⊕ .. ⊕ aₙ)
    :rtype:     myhdl always_comb() instance
    """
    @always_comb
    def logic():
        count = 0
        for i in range(len(a.val)):
            if a[i] == 1:
                count += 1

        if count % 2 == 1:
            out.next = 1
        else:
            out.next = 0

    return logic


def mul_mux(ip, out, sel):
    """
    selects one input from `n` select lines and `2**n` inputs as output

    :param      sel:  select pin
    :param      out:  output
    :param      ip:   array of equal sized inputs
    :type       sel:  intbv Signal
    :type       out:  intbv Signal
    :type       ip:   list

    :returns:   (ip₀ ⋅ S̄₀ ⋅ S̄₁ ⋅ .. ⋅ S̄ₙ) ⋅ .. ⋅ (ipₙ . S₀ ⋅ S₁ ⋅ .. ⋅ Sₙ)
    :rtype:     myhdl always_comb instance
    """
    if len(ip) != 2 ** len(sel.val):
        raise StopSimulation(f'{log2(len(ip))} number of selectors required')

    @always_comb
    def logic():
        out.next = ip[sel.val]

    return logic


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
