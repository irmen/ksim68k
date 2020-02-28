from typing import List

import pytest

import ksim68k


def setup_function(function):
    ksim68k.init(ksim68k.Cpu.M68030)


@pytest.fixture
def memory():
    return MemoryForTest()


class MemoryForTest(ksim68k.Memory):
    def __init__(self):
        super().__init__()
        self.reads = []
        self.writes = []
        self.data = [0] * 0x10000

    def load(self, data: List[int]):
        self.data = data

    def read8(self, address: int) -> int:
        self.reads.append((address, 8))
        return super().data_read_8(self.data, address)

    def read16(self, address: int) -> int:
        self.reads.append((address, 16))
        return super().data_read_16(self.data, address)

    def read32(self, address: int) -> int:
        self.reads.append((address, 32))
        return super().data_read_32(self.data, address)

    def write8(self, address: int, value: int):
        self.writes.append((address, value, 8))
        super().data_write_8(self.data, address, value)

    def write16(self, address: int, value: int):
        self.writes.append((address, value, 16))
        super().data_write_16(self.data, address, value)

    def write32(self, address: int, value: int):
        self.writes.append((address, value, 32))
        super().data_write_32(self.data, address, value)


def test_basics():
    assert ksim68k.cycles_remaining() == 0
    assert ksim68k.cycles_run() == 0


def test_disassem(memory: MemoryForTest):
    ksim68k.use_memory(memory)
    memory.write32(0, 0x12345678)
    memory.write32(4, 0xaabbccdd)
    disassem, length = ksim68k.disassemble(0, ksim68k.Cpu.M68030)
    assert length == 4
    assert disassem == "move.b  ($78,A4,D5.w*8), D1"


def test_reset(memory: MemoryForTest):
    memory.data_write_32(memory.data, 0, 0x11223344)   # stack pointer
    memory.data_write_32(memory.data, 4, 0xaabbccdd)   # program counter
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    sp = ksim68k.get_reg(None, ksim68k.Register.SP)
    a7 = ksim68k.get_reg(None, ksim68k.Register.A7)
    pc = ksim68k.get_reg(None, ksim68k.Register.PC)
    assert memory.reads == [(0, 32), (4, 32)]
    assert memory.writes == []
    assert sp == 0x11223344
    assert a7 == sp
    assert pc == 0xaabbccdd


def test_execute(memory: MemoryForTest):
    memory.data_write_32(memory.data, 0, 0x00001234)   # stack pointer
    memory.data_write_32(memory.data, 4, 0x0000abcd)   # program counter
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    cycles = ksim68k.execute(20)
    assert cycles == 16
    reg_a0 = ksim68k.get_reg(None, ksim68k.Register.A0)
    reg_a7 = ksim68k.get_reg(None, ksim68k.Register.A7)
    reg_d0 = ksim68k.get_reg(None, ksim68k.Register.D0)
    reg_pc = ksim68k.get_reg(None, ksim68k.Register.PC)
    reg_sp = ksim68k.get_reg(None, ksim68k.Register.SP)
    reg_sr = ksim68k.get_reg(None, ksim68k.Register.SR)
    assert reg_a0 == 0
    assert reg_d0 == 0
    assert reg_sp == 0x00001234
    assert reg_pc == 0x0000abed
    assert reg_a7 == reg_sp
    assert reg_sr == 0b0010011100000100
