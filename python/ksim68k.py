import enum
from _musashi import ffi, lib

__version__ = "0.1.dev0"


class CpuType(enum.Enum):
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
    A0 = lib.M68K_REG_A0
    A1 = lib.M68K_REG_A1
    A2 = lib.M68K_REG_A2
    A3 = lib.M68K_REG_A3
    A4 = lib.M68K_REG_A4
    A5 = lib.M68K_REG_A5
    A6 = lib.M68K_REG_A6
    A7 = lib.M68K_REG_A7
    D0 = lib.M68K_REG_D0
    D1 = lib.M68K_REG_D1
    D2 = lib.M68K_REG_D2
    D3 = lib.M68K_REG_D3
    D4 = lib.M68K_REG_D4
    D5 = lib.M68K_REG_D5
    D6 = lib.M68K_REG_D6
    D7 = lib.M68K_REG_D7
    CAAR = lib.M68K_REG_CAAR
    CACR = lib.M68K_REG_CACR
    DFC = lib.M68K_REG_DFC
    IR = lib.M68K_REG_IR
    ISP = lib.M68K_REG_ISP
    MSP = lib.M68K_REG_MSP
    PC = lib.M68K_REG_PC
    PPC = lib.M68K_REG_PPC
    SFC = lib.M68K_REG_SFC
    SP = lib.M68K_REG_SP
    SR = lib.M68K_REG_SR
    USP = lib.M68K_REG_USP
    VBR = lib.M68K_REG_VBR
    PREF_ADDR = lib.M68K_REG_PREF_ADDR
    PREF_DATA = lib.M68K_REG_PREF_DATA
    CPU_TYPE = lib.M68K_REG_CPU_TYPE
    
    
@ffi.def_extern()
def m68k_read_memory_8(address: int) -> int:
    print("read memory 8", hex(address))
    return 0

@ffi.def_extern()
def m68k_read_memory_16(address: int) -> int:
    print("read memory 16", hex(address))
    return 0

@ffi.def_extern()
def m68k_read_memory_32(address: int) -> int:
    print("read memory 32", hex(address))
    return 0

@ffi.def_extern()
def m68k_read_disassembler_8(address: int) -> int:
    print("disassembler read memory 8", hex(address))
    return 0

@ffi.def_extern()
def m68k_read_disassembler_16(address: int) -> int:
    print("disassembler read memory 16", hex(address))
    return 0

@ffi.def_extern()
def m68k_read_disassembler_32(address: int) -> int:
    print("disassembler read memory 32", hex(address))
    return 0

@ffi.def_extern()
def m68k_write_memory_8(address: int, value: int) -> None:
    print("write memory 8", hex(address), hex(value))
    return 0

@ffi.def_extern()
def m68k_write_memory_16(address: int, value: int) -> None:
    print("write memory 16", hex(address), hex(value))
    return 0

@ffi.def_extern()
def m68k_write_memory_32(address: int, value: int) -> None:
    print("write memory 32", hex(address), hex(value))
    return 0


m68k_context_size=           lib.m68k_context_size
m68k_cycles_remaining=       lib.m68k_cycles_remaining
m68k_cycles_run=             lib.m68k_cycles_run
m68k_disassemble=            lib.m68k_disassemble
m68k_disassemble_raw=        lib.m68k_disassemble_raw
m68k_end_timeslice=          lib.m68k_end_timeslice
m68k_execute=                lib.m68k_execute
m68k_get_context=            lib.m68k_get_context
m68k_get_reg=                lib.m68k_get_reg
m68k_get_virq=               lib.m68k_get_virq
m68k_init=                   lib.m68k_init
m68k_is_valid_instruction=   lib.m68k_is_valid_instruction
m68k_modify_timeslice=       lib.m68k_modify_timeslice
m68k_pulse_bus_error=        lib.m68k_pulse_bus_error
m68k_pulse_halt=             lib.m68k_pulse_halt
m68k_pulse_reset=            lib.m68k_pulse_reset

# m68k_read_disassembler_16=
# m68k_read_disassembler_16=
# m68k_read_disassembler_32=
# m68k_read_disassembler_32=
# m68k_read_disassembler_8=
# m68k_read_disassembler_8=
# m68k_read_immediate_16=
# m68k_read_immediate_32=
# m68k_read_memory_16=
# m68k_read_memory_16=
# m68k_read_memory_32=
# m68k_read_memory_32=
# m68k_read_memory_8=
# m68k_read_memory_8=
# m68k_read_pcrelative_16=
# m68k_read_pcrelative_32=
# m68k_read_pcrelative_8=
# m68k_set_bkpt_ack_callback=
# m68k_set_context=
# m68k_set_cpu_type=
# m68k_set_fc_callback=
# m68k_set_illg_instr_callback=
# m68k_set_instr_hook_callback=
# m68k_set_int_ack_callback=
# m68k_set_irq=
# m68k_set_pc_changed_callback=
# m68k_set_reg=
# m68k_set_reset_instr_callback=
# m68k_set_tas_instr_callback=
# m68k_set_virq=
# m68k_state_register=
# m68k_write_memory_16=
# m68k_write_memory_16=
# m68k_write_memory_32=
# m68k_write_memory_32=
# m68k_write_memory_32_pd=
# m68k_write_memory_8=
# m68k_write_memory_8
