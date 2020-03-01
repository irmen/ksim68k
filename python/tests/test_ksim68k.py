import os
import pytest
import ksim68k


def setup_function(function):
    ksim68k.init(ksim68k.Cpu.M68030)


@pytest.fixture
def memory():
    return MemoryForTest(0x10000)


def read_test_data(filename):
    if os.path.exists(filename):
        return open(filename, "rb").read()
    else:
        return open("tests/"+filename, "rb").read()


class MemoryForTest(ksim68k.Memory):
    def __init__(self, size: int):
        super().__init__(size)
        self.reads = []
        self.writes = []

    def read8(self, address: int) -> int:
        self.reads.append((address, 8))
        return super().read8(address)

    def read16(self, address: int) -> int:
        self.reads.append((address, 16))
        return super().read16(address)

    def read32(self, address: int) -> int:
        self.reads.append((address, 32))
        return super().read32(address)

    def write8(self, address: int, value: int):
        self.writes.append((address, value, 8))
        super().write8(address, value)

    def write16(self, address: int, value: int):
        self.writes.append((address, value, 16))
        super().write16(address, value)

    def write32(self, address: int, value: int):
        self.writes.append((address, value, 32))
        super().write32(address, value)


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


def test_reset_pulse(memory: MemoryForTest):
    memory.data[0:4] = [0x11, 0x22, 0x33, 0x44]     # stack pointer
    memory.data[4:8] = [0xaa, 0xbb, 0xcc, 0xdd]     # program counter
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    sp = ksim68k.get_reg(ksim68k.Register.SP)
    a7 = ksim68k.get_reg(ksim68k.Register.A7)
    pc = ksim68k.get_reg(ksim68k.Register.PC)
    assert memory.reads == [(0, 32), (4, 32)]
    assert memory.writes == []
    assert sp == 0x11223344
    assert a7 == sp
    assert pc == 0xaabbccdd


def test_reset_callback(memory: MemoryForTest):
    handler_called = False
    def handler():
        nonlocal handler_called
        handler_called = True
    memory.write32(0, 0x5000)   # stack pointer
    memory.write32(4, 0x2000)   # program counter
    memory.write16(0x2000, 0x4e70)       # reset instruction
    ksim68k.use_memory(memory)
    ksim68k.use_reset_handler(handler)
    ksim68k.pulse_reset()
    ksim68k.execute(5)
    assert handler_called


def test_execute(memory: MemoryForTest):
    memory.write32(0, 0x00001234)   # stack pointer
    memory.write32(4, 0x0000abcd)   # program counter
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    cycles = ksim68k.execute(20)
    assert cycles == 16
    reg_a0 = ksim68k.get_reg(ksim68k.Register.A0)
    reg_a7 = ksim68k.get_reg(ksim68k.Register.A7)
    reg_d0 = ksim68k.get_reg(ksim68k.Register.D0)
    reg_pc = ksim68k.get_reg(ksim68k.Register.PC)
    reg_sp = ksim68k.get_reg(ksim68k.Register.SP)
    reg_sr = ksim68k.get_reg(ksim68k.Register.SR)
    assert reg_a0 == 0
    assert reg_d0 == 0
    assert reg_sp == 0x00001234
    assert reg_pc == 0x0000abed
    assert reg_a7 == reg_sp
    assert reg_sr == 0b0010011100000100


def test_illegalinstr_handler(memory: MemoryForTest):
    old_handler = ksim68k.illegalinstr_handler
    illegal_found = False
    def handler(opcode):
        nonlocal illegal_found
        illegal_found = opcode == 0x4afc
    ksim68k.illegalinstr_handler = handler
    try:
        memory.write32(0, 0x00002000)    # stack pointer
        memory.write32(4, 0x00001000)    # program counter
        memory.write32(16, 0x0022334455)    # illegal instruction vector
        memory.write16(0x1000, 0x4afc)   # ILLEGAL instruction
        ksim68k.use_memory(memory)
        ksim68k.pulse_reset()
        ksim68k.execute(6)
        ir = ksim68k.get_reg(ksim68k.Register.IR)
        pc = ksim68k.get_reg(ksim68k.Register.PC)
        assert illegal_found
        assert ir == 0x4afc
        assert pc == 0x0022334455
    finally:
        ksim68k.illegalinstr_handler = old_handler


def test_stopinstruction_behavior(memory: MemoryForTest):
    memory.write32(0, 0x00002000)    # stack pointer
    memory.write32(4, 0x00001000)    # program counter
    memory.write16(0x1000, 0x4e72)   # STOP instruction
    memory.write16(0x1002, 0x2700)   # sr argument
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    ksim68k.execute(20)
    ir = ksim68k.get_reg(ksim68k.Register.IR)
    pc = ksim68k.get_reg(ksim68k.Register.PC)
    assert ir == 0x4e72
    assert pc == 0x1004
    ksim68k.execute(40)
    ir = ksim68k.get_reg(ksim68k.Register.IR)
    pc = ksim68k.get_reg(ksim68k.Register.PC)
    assert ir == 0x4e72
    assert pc == 0x1004


def test_execute_example_program():
    output = ""

    class MappedIoMemory(ksim68k.Memory):
        def write8(self, address: int, value: int) -> None:
            if address == 0x00fff002:       # memory mapped chrout register
                nonlocal output
                output += chr(value)

    memory = MappedIoMemory(0x8000)
    memory.load(0, read_test_data("testprog.bin"))
    ksim68k.use_memory(memory)
    ksim68k.pulse_reset()
    ksim68k.execute(2000)
    assert output == "Hello, world! From the 68000 assembly program.\n"
