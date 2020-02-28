"""
Python interface to the Musashi m68k cpu emulation library (https://github.com/kstenerud/Musashi)

This module Use CFFI to create the glue code but also to actually compile the library in one go!

Author: Irmen de Jong (irmen@razorvine.net)
Software license: "MIT software license". See http://opensource.org/licenses/MIT
"""

import os
from cffi import FFI

# the stripped header file, generated with: cpp -nostdinc -E -P Musashi/m68k.h
m68k_h = """
enum
{
 M68K_CPU_TYPE_INVALID,
 M68K_CPU_TYPE_68000,
 M68K_CPU_TYPE_68010,
 M68K_CPU_TYPE_68EC020,
 M68K_CPU_TYPE_68020,
 M68K_CPU_TYPE_68EC030,
 M68K_CPU_TYPE_68030,
 M68K_CPU_TYPE_68EC040,
 M68K_CPU_TYPE_68LC040,
 M68K_CPU_TYPE_68040,
 M68K_CPU_TYPE_SCC68070
};
typedef enum
{
 M68K_REG_D0,
 M68K_REG_D1,
 M68K_REG_D2,
 M68K_REG_D3,
 M68K_REG_D4,
 M68K_REG_D5,
 M68K_REG_D6,
 M68K_REG_D7,
 M68K_REG_A0,
 M68K_REG_A1,
 M68K_REG_A2,
 M68K_REG_A3,
 M68K_REG_A4,
 M68K_REG_A5,
 M68K_REG_A6,
 M68K_REG_A7,
 M68K_REG_PC,
 M68K_REG_SR,
 M68K_REG_SP,
 M68K_REG_USP,
 M68K_REG_ISP,
 M68K_REG_MSP,
 M68K_REG_SFC,
 M68K_REG_DFC,
 M68K_REG_VBR,
 M68K_REG_CACR,
 M68K_REG_CAAR,
 M68K_REG_PREF_ADDR,
 M68K_REG_PREF_DATA,
 M68K_REG_PPC,
 M68K_REG_IR,
 M68K_REG_CPU_TYPE
} m68k_register_t;
unsigned int m68k_read_memory_8(unsigned int address);
unsigned int m68k_read_memory_16(unsigned int address);
unsigned int m68k_read_memory_32(unsigned int address);
unsigned int m68k_read_immediate_16(unsigned int address);
unsigned int m68k_read_immediate_32(unsigned int address);
unsigned int m68k_read_pcrelative_8(unsigned int address);
unsigned int m68k_read_pcrelative_16(unsigned int address);
unsigned int m68k_read_pcrelative_32(unsigned int address);
unsigned int m68k_read_disassembler_8 (unsigned int address);
unsigned int m68k_read_disassembler_16 (unsigned int address);
unsigned int m68k_read_disassembler_32 (unsigned int address);
void m68k_write_memory_8(unsigned int address, unsigned int value);
void m68k_write_memory_16(unsigned int address, unsigned int value);
void m68k_write_memory_32(unsigned int address, unsigned int value);
void m68k_write_memory_32_pd(unsigned int address, unsigned int value);
void m68k_set_int_ack_callback(int (*callback)(int int_level));
void m68k_set_bkpt_ack_callback(void (*callback)(unsigned int data));
void m68k_set_reset_instr_callback(void (*callback)(void));
void m68k_set_pc_changed_callback(void (*callback)(unsigned int new_pc));
void m68k_set_tas_instr_callback(int (*callback)(void));
void m68k_set_illg_instr_callback(int (*callback)(int));
void m68k_set_fc_callback(void (*callback)(unsigned int new_fc));
void m68k_set_instr_hook_callback(void (*callback)(unsigned int pc));
void m68k_set_cpu_type(unsigned int cpu_type);
void m68k_init(void);
void m68k_pulse_reset(void);
int m68k_execute(int num_cycles);
int m68k_cycles_run(void);
int m68k_cycles_remaining(void);
void m68k_modify_timeslice(int cycles);
void m68k_end_timeslice(void);
void m68k_set_irq(unsigned int int_level);
void m68k_set_virq(unsigned int level, unsigned int active);
unsigned int m68k_get_virq(unsigned int level);
void m68k_pulse_halt(void);
void m68k_pulse_bus_error(void);
unsigned int m68k_context_size(void);
unsigned int m68k_get_context(void* dst);
void m68k_set_context(void* dst);
void m68k_state_register(const char *type, int index);
unsigned int m68k_get_reg(void* context, m68k_register_t reg);
void m68k_set_reg(m68k_register_t reg, unsigned int value);
unsigned int m68k_is_valid_instruction(unsigned int instruction, unsigned int cpu_type);
unsigned int m68k_disassemble(char* str_buff, unsigned int pc, unsigned int cpu_type);
unsigned int m68k_disassemble_raw(char* str_buff, unsigned int pc, const unsigned char* opdata, const unsigned char* argdata, unsigned int cpu_type);
"""

extern_python = """

extern "Python" unsigned int _ksim68k_read_memory_8(unsigned int address);
extern "Python" unsigned int _ksim68k_read_memory_16(unsigned int address);
extern "Python" unsigned int _ksim68k_read_memory_32(unsigned int address);
extern "Python" unsigned int _ksim68k_read_disassembler_8  (unsigned int address);
extern "Python" unsigned int _ksim68k_read_disassembler_16 (unsigned int address);
extern "Python" unsigned int _ksim68k_read_disassembler_32 (unsigned int address);
extern "Python" void _ksim68k_write_memory_8(unsigned int address, unsigned int value);
extern "Python" void _ksim68k_write_memory_16(unsigned int address, unsigned int value);
extern "Python" void _ksim68k_write_memory_32(unsigned int address, unsigned int value);
"""

ffibuilder = FFI()
ffibuilder.cdef(m68k_h + extern_python)

libraries = []
compiler_args = ["-g1"]
if os.name == "posix":
    libraries = ["m"]

ffibuilder.set_source("_musashi", """
                      #include "m68k.h"

static unsigned int _ksim68k_read_memory_8(unsigned int address);
static unsigned int _ksim68k_read_memory_16(unsigned int address);
static unsigned int _ksim68k_read_memory_32(unsigned int address);
static unsigned int _ksim68k_read_disassembler_8  (unsigned int address);
static unsigned int _ksim68k_read_disassembler_16 (unsigned int address);
static unsigned int _ksim68k_read_disassembler_32 (unsigned int address);
static void _ksim68k_write_memory_8(unsigned int address, unsigned int value);
static void _ksim68k_write_memory_16(unsigned int address, unsigned int value);
static void _ksim68k_write_memory_32(unsigned int address, unsigned int value);

unsigned int  m68k_read_memory_8(unsigned int address) {
    return _ksim68k_read_memory_8(address);
}
unsigned int  m68k_read_memory_16(unsigned int address){
    return _ksim68k_read_memory_16(address);
}
unsigned int  m68k_read_memory_32(unsigned int address){
    return _ksim68k_read_memory_32(address);
}
unsigned int m68k_read_disassembler_8  (unsigned int address){
    return _ksim68k_read_disassembler_8(address);
}
unsigned int m68k_read_disassembler_16 (unsigned int address){
    return _ksim68k_read_disassembler_16(address);
}
unsigned int m68k_read_disassembler_32 (unsigned int address){
    return _ksim68k_read_disassembler_32(address);
}
void m68k_write_memory_8(unsigned int address, unsigned int value) {
    _ksim68k_write_memory_8(address, value);
}
void m68k_write_memory_16(unsigned int address, unsigned int value) {
    _ksim68k_write_memory_16(address, value);
}
void m68k_write_memory_32(unsigned int address, unsigned int value) {
    _ksim68k_write_memory_32(address, value);
}

unsigned int  m68k_read_immediate_16(unsigned int address) {
    return m68k_read_memory_16(address);
}
unsigned int  m68k_read_immediate_32(unsigned int address) {
    return m68k_read_memory_32(address);
}
unsigned int  m68k_read_pcrelative_8(unsigned int address) {
    return m68k_read_memory_8(address);
}
unsigned int  m68k_read_pcrelative_16(unsigned int address){
    return m68k_read_memory_16(address);
}
unsigned int  m68k_read_pcrelative_32(unsigned int address){
    return m68k_read_memory_32(address);
}

void m68k_state_register(const char *type, int index)
{ /* dummy */ }

void m68k_write_memory_32_pd(unsigned int address, unsigned int value) {
    m68k_write_memory_32(address, value);
}


""",
                      sources=[
                          "Musashi/m68kcpu.c",
                          "Musashi/m68kdasm.c",
                          "Musashi/m68kops.c",
                          "Musashi/softfloat/softfloat.c"
                      ],
                      include_dirs=["Musashi", "."],
                      libraries=libraries,
                      define_macros=[("MUSASHI_CNF", '"m68kconf_custom.h"')],
                      extra_compile_args=compiler_args)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
