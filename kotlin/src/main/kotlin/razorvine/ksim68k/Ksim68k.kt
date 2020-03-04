package razorvine.ksim68k

import java.nio.Buffer


enum class Cpu {
    INVALID,
    M68000,
    M68010,
    M68EC020,
    M68020,
    M68EC030,
    M68030,
    M68EC040,
    M68LC040,
    M68040,
    SCC68070
}


enum class Register {
    D0,
    D1,
    D2,
    D3,
    D4,
    D5,
    D6,
    D7,
    A0,
    A1,
    A2,
    A3,
    A4,
    A5,
    A6,
    A7,
    PC,
    SR,
    SP,
    USP,
    ISP,
    MSP,
    SFC,
    DFC,
    VBR,
    CACR,
    CAAR,
    PREF_ADDR,
    PREF_DATA,
    PPC,
    IR,
    CPU_TYPE
}


object Ksim68k {

    private val musashi = MusashiNative.INSTANCE

    // functions:
    fun init() = musashi.m68k_init()
    fun set_cpu_type(cpu: Cpu) = musashi.m68k_set_cpu_type(cpu.ordinal)
    fun pulse_reset() = musashi.m68k_pulse_reset()
    fun execute(num_cycles: Int) = musashi.m68k_execute(num_cycles)
    fun cycles_run() = musashi.m68k_cycles_run()
    fun cycles_remaining() = musashi.m68k_cycles_remaining()
    fun modify_timeslice(cycles: Int) = musashi.m68k_modify_timeslice(cycles)
    fun end_timeslice() = musashi.m68k_end_timeslice()
    fun set_irq(int_level: Int) = musashi.m68k_set_irq(int_level)
    fun set_virq(level: Int, active: Int) = musashi.m68k_set_virq(level, active)
    fun get_virq(level: Int): Int = musashi.m68k_get_virq(level)
    fun pulse_halt() = musashi.m68k_pulse_halt()
    fun pulse_bus_error() = musashi.m68k_pulse_bus_error()
    fun context_size(): Int = musashi.m68k_context_size()
    fun get_reg(context: Buffer?, reg: Register): Int = musashi.m68k_get_reg(context, reg.ordinal)
    fun set_reg(reg: Register, value: Int) = musashi.m68k_set_reg(reg.ordinal, value)
    fun is_valid_instruction(instruction: Int, cpu: Cpu = Cpu.M68000): Boolean = musashi.m68k_is_valid_instruction(instruction, cpu.ordinal)
    fun get_context(ctx: Buffer): Int = musashi.m68k_get_context(ctx)
    fun set_context(ctx: Buffer) = musashi.m68k_set_context(ctx)
    fun disassemble(str_buff: ByteArray, pc: Int, cpu: Cpu = Cpu.M68000): Int {
        val instruction_size = musashi.m68k_disassemble(str_buff, pc, cpu.ordinal)
        return instruction_size
    }
    fun disassemble_raw(str_buff: ByteArray, pc: Int, opdata: ByteArray, argdata: ByteArray, cpu: Cpu = Cpu.M68000): Int {
        val instruction_size = musashi.m68k_disassemble_raw(str_buff, pc, opdata, argdata, cpu.ordinal)
        return instruction_size
    }

    fun use_memory(memory: Memory) {
        memory.registerCallbacks(musashi)
    }

    // TODO:
//    fun m68k_set_int_ack_callback(int (*callback)(int int_level))
//    fun m68k_set_bkpt_ack_callback(void (*callback)(unsigned int data))
//    fun m68k_set_reset_instr_callback(void (*callback)(void))
//    fun m68k_set_pc_changed_callback(void (*callback)(unsigned int new_pc))
//    fun m68k_set_tas_instr_callback(int (*callback)(void))
//    fun m68k_set_illg_instr_callback(int (*callback)(int))
//    fun m68k_set_fc_callback(void (*callback)(unsigned int new_fc))
//    fun m68k_set_instr_hook_callback(void (*callback)(unsigned int pc))

    // IGNORED for now:  void m68k_state_register(const char *type, int index);
}
