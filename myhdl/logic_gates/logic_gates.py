from myhdl import always_comb, Signal, intbv, delay, instance, Simulation, bin
from itertools import product


def not_gate(ip, out):
    """
    @brief      not gate returns inverted value of input

    @param      ip    input intbv signal
    @param      out   output intbv signal

    @return     not logic myhdl instance

    | ip | out |
    |----|-----|
    |  0 |   1 |
    |  1 |   0 |

    """

    @always_comb
    def logic():
        if ip == 0:
            out.next = 1
        else:
            out.next = 0

    return logic


def and_gate(a, b, out):
    """
    @brief      and gate returns 1 only if both inputs are 1 else 0

    @param      a     first input intbv signal
    @param      b     second input intbv signal
    @param      out   output intbv signal

    @return     and logic myhdl instance

    | a | b | out |
    |---|---|-----|
    | 0 | 0 |   0 |
    | 0 | 1 |   0 |
    | 1 | 0 |   0 |
    | 1 | 1 |   1 |

    """

    @always_comb
    def logic():
        if a == b == 1:
            out.next = 1
        else:
            out.next = 0

    return logic


def or_gate(a, b, out):
    """
    @brief      or gate returns 1 when atleast one of its input is 1,
                0 otherwise

    @param      a     first input intbv signal
    @param      b     second input intbv signal
    @param      out   output intbv signal

    @return     or logic myhdl instance

    | a | b | out |
    |---|---|-----|
    | 0 | 0 |   0 |
    | 0 | 1 |   1 |
    | 1 | 0 |   1 |
    | 1 | 1 |   1 |

    """

    @always_comb
    def logic():
        if a == b == 0:
            out.next = 0
        else:
            out.next = 1

    return logic


def xor_gate(a, b, out):
    """
    @brief      Exclusive or, returns 1 only if both the inputs are different

    @param      a     first input intbv signal
    @param      b     second input intbv signal
    @param      out   output intbv signal

    @return     xor gate myhdl instance

    | a | b | out |
    |---|---|-----|
    | 0 | 0 |   0 |
    | 0 | 1 |   1 |
    | 1 | 0 |   1 |
    | 1 | 1 |   0 |

    """

    @always_comb
    def logic():
        if a != b:
            out.next = 1
        else:
            out.next = 0

    return logic


def mux_gate(a, b , sel, out):
    """
    @brief      mux selects input as output depending on sel pin

    @param      a     first input intbv signal
    @param      b     second input intbv signal
    @param      sel   selector pin
    @param      out   output intbv signal

    @return     not logic myhdl instance

    | a | b | sel | out |
    |---|---|-----|-----|
    | 0 | 0 |   0 |   0 |
    | 0 | 1 |   0 |   0 |
    | 1 | 0 |   0 |   1 |
    | 1 | 1 |   0 |   1 |
    | 0 | 0 |   1 |   0 |
    | 0 | 1 |   1 |   1 |
    | 1 | 0 |   1 |   0 |
    | 1 | 1 |   1 |   1 |

    """

    @always_comb
    def logic():
        if sel == 0:
            out.next = a
        else:
            out.next = b

    return logic


def dmux_gate(ip, sel, a, b):
    """
    @brief      demux returns a, b depending on value of sel

    @param      ip    input intbv signal
    @param      sel   selector pin signal
    @param      a     output a selected when sel=0
    @param      b     output b selected when sel=1

    @return     dmux myhdl instance

    | sel | a  | b  |
    |-----|----|----|
    |   0 | in | 0  |
    |   1 | 0  | in |

    """

    @always_comb
    def logic():
        if sel == 0:
            a.next = ip
            b.next = 0
        else:
            a.next = 0
            b.next = ip

    return logic
