from myhdl import (Signal, intbv, delay, instance,
                   Simulation, bin, StopSimulation)
from itertools import product
import logic_gates as lg
import pytest


@pytest.mark.parametrize('width', [2, 3, 4])
def test_bench_and_gate(width):
    a = Signal(intbv(0)[width:])
    out = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    got = list()
    expected = ['0' for x in range(2 ** width - 1)]
    expected.append('1')
    gate_inst = lg.and_gate(a, out)

    @instance
    def stimulus():
        for num in bin_product:
            a.next = intbv(num)
            yield delay(10)
            got.append(bin(out, 1))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


@pytest.mark.parametrize('width', [2, 3, 4])
def test_bench_or_gate(width):
    a = Signal(intbv(0)[width:])
    out = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = ['1' for x in range(2 ** width - 1)]
    expected.insert(0, '0')
    got = list()

    gate_inst = lg.or_gate(a, out)

    @instance
    def stimulus():
        for num in bin_product:
            a.next = intbv(num)
            yield delay(10)
            got.append(bin(out, 1))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


@pytest.mark.parametrize('width', [2, 3, 4])
def test_bench_not_gate(width):
    a = Signal(intbv(0)[width:])
    out = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = [''.join(x) for x in list(product('10', repeat=width))]
    got = list()

    gate_inst = lg.not_gate(a, out)

    @instance
    def stimulus():
        for num in bin_product:
            a.next = intbv(num)
            yield delay(10)
            got.append(bin(out, width))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


@pytest.mark.parametrize('width', [2, 3, 4])
def test_bench_xor_gate(width):
    a = Signal(intbv(0)[width:])
    out = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = ['1' if x.count('1') == 1 else '0' for x in bin_product]
    got = list()

    gate_inst = lg.xor_gate(a, out)

    @instance
    def stimulus():
        for num in bin_product:
            a.next = intbv(num)
            yield delay(10)
            got.append(bin(out, 1))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


@pytest.mark.parametrize('width', [2, 3, 4])
def test_odd_parity(width):
    a = Signal(intbv(0)[width:])
    out = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = ['1' if x.count('1') % 2 != 0 else '0' for x in bin_product]
    got = list()

    gate_inst = lg.odd_parity(a, out)

    @instance
    def stimulus():
        for num in bin_product:
            a.next = intbv(num)
            yield delay(10)
            got.append(bin(out, 1))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


def test_mul_mux_raises_StopSimulation_on_bad_ip():
    a = [Signal(intbv(0)[3:]) for x in range(8)]
    sel = Signal(intbv(0)[2:])
    out = Signal(intbv(0)[3:])

    with pytest.raises(StopSimulation) as execinfo:
        lg.mul_mux(a, out, sel)

    assert 'number of selectors required' in str(execinfo.value)


@pytest.mark.parametrize('width', [2, 3, 4])
def test_mul_mux(width):
    a = [Signal(intbv(x)[width:]) for x in range(2 ** width)]
    out = Signal(intbv(0)[width:])
    sel = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = bin_product
    got = list()

    gate_inst = lg.mul_mux(a, out, sel)

    @instance
    def stimulus():
        for num in bin_product:
            sel.next = intbv(num)
            yield delay(10)
            got.append(bin(out, width))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected


def test_mul_demux_raises_StopSimulation_on_bad_ip():
    a = [Signal(intbv(0)[3:]) for x in range(8)]
    sel = Signal(intbv(0)[2:])
    out = Signal(intbv(0)[3:])

    with pytest.raises(StopSimulation) as execinfo:
        lg.mul_mux(a, out, sel)

    assert 'number of selectors required' in str(execinfo.value)

@pytest.mark.parametrize('width', [2, 3, 4])
def test_mul_demux(width):
    ip = Signal(intbv('101')[3:])
    op = [Signal(intbv(0)[3:]) for x in range(2**width)]
    sel = Signal(intbv(0)[width:])

    bin_product = [''.join(x) for x in list(product('01', repeat=width))]
    expected = ['101' for x in range(2**width)]
    got = list()
    gate_inst = lg.mul_demux(sel, ip, op)


    @instance
    def stimulus():
        for num in bin_product:
            sel.next = intbv(num)
            yield delay(10)
            got.append(bin(op[sel], 3))

    sim = Simulation(gate_inst, stimulus)
    sim.run()

    assert got == expected

