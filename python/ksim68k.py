import sys
import enum
from typing import Optional, Tuple

from _musashi import ffi, lib

__version__ = "1.1"


class Cpu(enum.Enum):
    """The simulated CPU type"""
    M68000 = lib.M68K_CPU_TYPE_68000
    M68010 = lib.M68K_CPU_TYPE_68010
    M68020 = lib.M68K_CPU_TYPE_68020
    M68030 = lib.M68K_CPU_TYPE_68030
    M68040 = lib.M68K_CPU_TYPE_68040
    M680EC20 = lib.M68K_CPU_TYPE_68EC020
    M680EC30 = lib.M68K_CPU_TYPE_68EC030
    M680EC40 = lib.M68K_CPU_TYPE_68EC040
    M680LC40 = lib.M68K_CPU_TYPE_68LC040
    INVALID = lib.M68K_CPU_TYPE_INVALID
    SCC68070 = lib.M68K_CPU_TYPE_SCC68070


class Register(enum.Enum):
    """A cpu register"""
    D0 = lib.M68K_REG_D0
    D1 = lib.M68K_REG_D1
    D2 = lib.M68K_REG_D2
    D3 = lib.M68K_REG_D3
    D4 = lib.M68K_REG_D4
    D5 = lib.M68K_REG_D5
    D6 = lib.M68K_REG_D6
    D7 = lib.M68K_REG_D7
    A0 = lib.M68K_REG_A0
    A1 = lib.M68K_REG_A1
    A2 = lib.M68K_REG_A2
    A3 = lib.M68K_REG_A3
    A4 = lib.M68K_REG_A4
    A5 = lib.M68K_REG_A5
    A6 = lib.M68K_REG_A6
    A7 = lib.M68K_REG_A7
    PC = lib.M68K_REG_PC                # program counter
    SR = lib.M68K_REG_SR                # status register (CCR)
    SP = lib.M68K_REG_SP                # current stack pointer (A7)
    ISP = lib.M68K_REG_ISP              # interrupt stack pointer
    MSP = lib.M68K_REG_MSP              # master stack pointer
    USP = lib.M68K_REG_USP              # user stack pointer
    CAAR = lib.M68K_REG_CAAR            # cache address
    CACR = lib.M68K_REG_CACR            # cache control
    PPC = lib.M68K_REG_PPC              # previous program counter
    DFC = lib.M68K_REG_DFC              # destination function code
    SFC = lib.M68K_REG_SFC              # source function code
    VBR = lib.M68K_REG_VBR              # vector base register
    IR = lib.M68K_REG_IR                # pseudo register: instruction register
    CPU_TYPE = lib.M68K_REG_CPU_TYPE    # pseudo register: current CPU type


class Memory:
    def __init__(self, size: int) -> None:
        self.data = bytearray(size)

    def load(self, address, data: bytes) -> None:
        if address + len(data) > len(self.data):
            raise ValueError("size of data is too large to fit in the memory at that address")
        self.data[address:address+len(data)] = data

    def read8(self, address: int) -> int:
        return self.data[address]

    def read16(self, address: int) -> int:
        return (self.data[address] << 8) | self.data[address + 1]

    def read32(self, address: int) -> int:
        return (self.data[address] << 24) | (self.data[address + 1] << 16) \
               | (self.data[address + 2] << 8) | self.data[address + 3]

    def write8(self, address: int, value: int) -> None:
        self.data[address] = value

    def write16(self, address: int, value: int) -> None:
        self.data[address] = value >> 8
        self.data[address + 1] = value & 255

    def write32(self, address: int, value: int) -> None:
        self.data[address] = (value >> 24) & 255
        self.data[address + 1] = (value >> 16) & 255
        self.data[address + 2] = (value >> 8) & 255
        self.data[address + 3] = value & 255


memory = Memory(1024)


@ffi.def_extern()
def _ksim68k_read_memory_8(address: int) -> int:
    return memory.read8(address)


@ffi.def_extern()
def _ksim68k_read_memory_16(address: int) -> int:
    return memory.read16(address)


@ffi.def_extern()
def _ksim68k_read_memory_32(address: int) -> int:
    return memory.read32(address)


@ffi.def_extern()
def _ksim68k_read_disassembler_8(address: int) -> int:
    return memory.read8(address)


@ffi.def_extern()
def _ksim68k_read_disassembler_16(address: int) -> int:
    return memory.read16(address)


@ffi.def_extern()
def _ksim68k_read_disassembler_32(address: int) -> int:
    return memory.read32(address)


@ffi.def_extern()
def _ksim68k_write_memory_8(address: int, value: int) -> None:
    memory.write8(address, value)


@ffi.def_extern()
def _ksim68k_write_memory_16(address: int, value: int) -> None:
    memory.write16(address, value)


@ffi.def_extern()
def _ksim68k_write_memory_32(address: int, value: int) -> None:
    memory.write32(address, value)


def reset_handler() -> None:
    """The default callback for a RESET instruction. You can set this to your own function as desired."""
    pass


def illegalinstr_handler(opcode: int) -> int:
    """The default callback for an illegal instruction. You can set this to your own function as desired."""
    print("ksim68k: illegal instruction encountered: "+hex(opcode), file=sys.stderr)
    return 0


def pc_changed_handler(address: int) -> None:
    """The default callback for a large change in PC (jump/vector). You can set this to your own function as desired."""
    pass


@ffi.def_extern()
def _ksim68k_reset_handler() -> None:
    reset_handler()


@ffi.def_extern()
def _ksim68k_illegalinstr_handler(opcode: int) -> int:
    return illegalinstr_handler(opcode)


@ffi.def_extern()
def _ksim68k_pc_changed_handler(address: int) -> None:
    pc_changed_handler(address)


context_size = lib.m68k_context_size()


def get_context(ctx: Optional[bytes]) -> bytes:
    """Get a CPU context"""
    if ctx:
        if len(ctx) < context_size:
            raise ValueError("context buffer too small, need at least {} bytes".format(context_size))
    else:
        ctx = bytes(context_size)
    lib.m68k_get_context(ctx)
    return ctx


def set_context(ctx: bytes) -> None:
    """Set the current CPU context"""
    if len(ctx) < context_size:
        raise ValueError("context buffer too small, need at least {} bytes".format(context_size))
    lib.m68k_set_context(ctx)


def init(cpu: Cpu) -> None:
    """Sets the CPU type that is being simulated and initializes the CPU."""
    lib.m68k_set_cpu_type(cpu.value)
    lib.m68k_init()


def use_memory(mem: Memory) -> None:
    """Start using the provided memory to read/write values"""
    global memory
    memory = mem


def execute(num_cycles: int) -> int:
    """execute num_cycles worth of instructions.  returns number of cycles used"""
    return lib.m68k_execute(num_cycles)


def cycles_remaining() -> int:
    """Number of cycles left"""
    return lib.m68k_cycles_remaining()


def cycles_run() -> int:
    """Number of cycles run so far"""
    return lib.m68k_cycles_run()


def disassemble(pc: int, cpu: Cpu = Cpu.M68000) -> Tuple[str, int]:
    """Disassemble 1 instruction using the specified CPU type, at address pc.
    Returns disassembly, instruction size in bytes."""
    buf = bytes(100)
    length = lib.m68k_disassemble(buf, pc, cpu.value)
    buf = buf.split(b"\0", 1)[0]
    return buf.decode(), length


def disassemble_raw(pc: int, opdata: bytes, argdata: bytes, cpu: Cpu = Cpu.M68000) -> Tuple[str, int]:
    """Disassemble 1 instruction using the specified CPU type, at address pc.
    Accepts the raw opcode directly instead of reading data via the callback functions.
    Returns disassembly, instruction size in bytes."""
    buf = bytes(100)
    length = lib.m68k_disassemble_raw(buf, pc, opdata, argdata, cpu.value)
    buf = buf.split(b"\0", 1)[0]
    return buf.decode(), length


def is_valid_instruction(instr: int, cpu: Cpu = Cpu.M68000) -> bool:
    """Check if an instruction is valid for the specified CPU type"""
    return bool(lib.m68k_is_valid_instruction(instr, cpu.value))


def get_reg(register: Register, ctx: Optional[bytes] = None) -> int:
    """Peek at the internals of a CPU context.  This can either be a context
    retrieved using get_context() or None for the currently running context."""
    return lib.m68k_get_reg(ctx or ffi.NULL, register.value)


def set_reg(register: Register, value: int) -> None:
    """Poke values into the internals of the currently running CPU context"""
    lib.m68k_set_reg(register.value, value)


def pulse_reset() -> None:
    """Pulse the RESET pin on the CPU. You *MUST* reset the CPU at least once to initialize the emulation."""
    lib.m68k_pulse_reset()


def pulse_bus_error() -> None:
    """Trigger a bus error exception"""
    lib.m68k_pulse_bus_error()


def pulse_halt() -> None:
    """Halts the CPU as if you pulsed the HALT pin."""
    lib.m68k_pulse_halt()


def modify_timeslice(cycles: int) -> None:
    """Modify cycles left"""
    lib.m68k_modify_timeslice(cycles)


def end_timeslice() -> None:
    """End timeslice now"""
    lib.m68k_end_timeslice()


def set_irq(level: int) -> None:
    """Set the IPL0-IPL2 pins on the CPU (IRQ).
    A transition from < 7 to 7 will cause a non-maskable interrupt (NMI).
    Setting IRQ to 0 will clear an interrupt request."""
    lib.m68k_set_irq(level)


def set_virq(level: int, active: int) -> None:
    """Set the virtual irq lines, where the highest level active line is automatically selected.
    If you use this function, do not use set_irq."""
    lib.m68k_set_virq(level, active)


def get_virq(level: int) -> int:
    """Get the current virtual irq lines"""
    return lib.m68k_get_virq(level)


# unused callbacks:
# set_bkpt_ack_callback = lib.m68k_set_bkpt_ack_callback
# set_fc_callback = lib.m68k_set_fc_callback
# set_illg_instr_callback = lib.m68k_set_illg_instr_callback
# set_instr_hook_callback = lib.m68k_set_instr_hook_callback
# set_int_ack_callback = lib.m68k_set_int_ack_callback
# set_pc_changed_callback = lib.m68k_set_pc_changed_callback
# set_tas_instr_callback = lib.m68k_set_tas_instr_callback
# state_register = lib.m68k_state_register
