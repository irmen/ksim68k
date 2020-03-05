package razorvine.ksim68k

import com.sun.jna.Callback
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

    fun init(cpu: Cpu) {
        musashi.m68k_set_cpu_type(cpu.ordinal)
        musashi.m68k_init()
        musashi.m68k_set_reset_instr_callback(ResetHandler)
        musashi.m68k_set_illg_instr_callback(IllegalInstrHandler)
        musashi.m68k_set_pc_changed_callback(PcChangedHandler)
    }

    fun setCpuType(cpu: Cpu) = musashi.m68k_set_cpu_type(cpu.ordinal)
    fun pulseReset() = musashi.m68k_pulse_reset()
    fun execute(num_cycles: Int) = musashi.m68k_execute(num_cycles)
    fun cyclesRun() = musashi.m68k_cycles_run()
    fun cyclesRemaining() = musashi.m68k_cycles_remaining()
    fun modifyTimeslice(cycles: Int) = musashi.m68k_modify_timeslice(cycles)
    fun endTimeslice() = musashi.m68k_end_timeslice()
    fun setIrq(int_level: Int) = musashi.m68k_set_irq(int_level)
    fun setVirq(level: Int, active: Int) = musashi.m68k_set_virq(level, active)
    fun getVirq(level: Int): Int = musashi.m68k_get_virq(level)
    fun pulseHalt() = musashi.m68k_pulse_halt()
    fun pulseBusError() = musashi.m68k_pulse_bus_error()
    fun contextSize(): Int = musashi.m68k_context_size()
    fun getReg(reg: Register, context: Buffer? = null): Long = musashi.m68k_get_reg(context, reg.ordinal).toLong() and 0xffffffff
    fun getRegSgn(reg: Register, context: Buffer? = null): Int = musashi.m68k_get_reg(context, reg.ordinal)
    fun setReg(reg: Register, value: Long) = musashi.m68k_set_reg(reg.ordinal, value.toInt())
    fun setRegSgn(reg: Register, value: Int) = musashi.m68k_set_reg(reg.ordinal, value)
    fun isValidInstruction(instruction: Int, cpu: Cpu = Cpu.M68000): Boolean = musashi.m68k_is_valid_instruction(instruction, cpu.ordinal)
    fun getContext(ctx: Buffer): Int = musashi.m68k_get_context(ctx)
    fun setContext(ctx: Buffer) = musashi.m68k_set_context(ctx)
    fun disassemble(pc: Int, cpu: Cpu = Cpu.M68000): Pair<String, Int> {
        val buff = ByteArray(100)
        val instrSize = musashi.m68k_disassemble(buff, pc, cpu.ordinal)
        return Pair(String(buff, 0, buff.indexOf(0)), instrSize)
    }

    fun disassembleRaw(pc: Int, opdata: ByteArray, argdata: ByteArray, cpu: Cpu = Cpu.M68000): Pair<String, Int> {
        val buff = ByteArray(100)
        val instrSize = musashi.m68k_disassemble_raw(buff, pc, opdata, argdata, cpu.ordinal)
        return Pair(String(buff, 0, buff.indexOf(0)), instrSize)
    }

    fun useMemory(memory: Memory) {
        memory.registerCallbacks(musashi)
    }

    object ResetHandler : Callback {
        var callbackFunction: () -> Unit = { }
        fun callback() = callbackFunction()
    }

    object IllegalInstrHandler : Callback {
        var callbackFunction: (Int) -> Int = { opcode ->
            println("Ksim68k: illegal instruction encountered: ${opcode.toString(16)}")
            0 }
        fun callback(opcode: Int): Int = callbackFunction(opcode)
    }

    object PcChangedHandler : Callback {
        var callbackFunction: (Int) -> Int = { address -> 0 }
        fun callback(address: Int): Int = callbackFunction(address)
    }

    var handlerForResetInstruction: () -> Unit
        get() = ResetHandler.callbackFunction
        set(value) {
            ResetHandler.callbackFunction = value
        }

    var handlerForIllegalInstruction: (Int) -> Int
        get() = IllegalInstrHandler.callbackFunction
        set(value) {
            IllegalInstrHandler.callbackFunction = value
        }

    var handlerForPcChanged: (Int) -> Int
        get() = PcChangedHandler.callbackFunction
        set(value) {
            PcChangedHandler.callbackFunction = value
        }


    // not implemented for now:
//    fun m68k_set_int_ack_callback(int (*callback)(int int_level))
//    fun m68k_set_bkpt_ack_callback(void (*callback)(unsigned int data))
//    fun m68k_set_tas_instr_callback(int (*callback)(void))
//    fun m68k_set_fc_callback(void (*callback)(unsigned int new_fc))
//    fun m68k_set_instr_hook_callback(void (*callback)(unsigned int pc))

    // IGNORED for now:  void m68k_state_register(const char *type, int index);
}
