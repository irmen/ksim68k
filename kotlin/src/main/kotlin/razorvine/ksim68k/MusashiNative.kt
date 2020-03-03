package razorvine.ksim68k

import com.sun.jna.*
import com.sun.jna.Library
import java.nio.Buffer


interface MusashiNative: Library {

    companion object {
        init {
            if(!Platform.isWindows())
                System.setProperty("jna.library.path", "/usr/local/lib")
        }

        val INSTANCE: MusashiNative by lazy { Native.load("musashi", MusashiNative::class.java) }

//        init {
//            val library = NativeLibrary.getInstance("/usr/local/lib/libbinaryen.so")
//            Native.register(Binaryen::class.java, library)
//        }
    }

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


    // functions:
    // TODO
    fun m68k_init()
    fun m68k_set_cpu_type(cpu_type: Int)
    fun m68k_pulse_reset()
    fun m68k_execute(num_cycles: Int): Int
    fun m68k_cycles_run(): Int
    fun m68k_cycles_remaining(): Int
    fun m68k_modify_timeslice(cycles: Int)
    fun m68k_end_timeslice()
    fun m68k_set_irq(int_level: Int)
    fun m68k_set_virq(level: Int, active: Int)
    fun m68k_get_virq(level: Int): Int
    fun m68k_pulse_halt()
    fun m68k_pulse_bus_error()
    fun m68k_context_size(): Int
    fun m68k_get_reg(context: Buffer?, reg: Int): Int
    fun m68k_set_reg(reg: Int, value: Int)
    fun m68k_is_valid_instruction(instruction: Int, cpu_type: Int): Boolean
    fun m68k_get_context(ctx: Buffer): Int
    fun m68k_set_context(ctx: Buffer)
    fun m68k_disassemble(str_buff: ByteArray, pc: Int, cpu_type: Int): Int
    fun m68k_disassemble_raw(str_buff: ByteArray, pc: Int, opdata: ByteArray, argdata: ByteArray, cpu_type: Int): Int

//    fun m68k_set_int_ack_callback(int (*callback)(int int_level))
//    fun m68k_set_bkpt_ack_callback(void (*callback)(unsigned int data))
//    fun m68k_set_reset_instr_callback(void (*callback)(void))
//    fun m68k_set_pc_changed_callback(void (*callback)(unsigned int new_pc))
//    fun m68k_set_tas_instr_callback(int (*callback)(void))
//    fun m68k_set_illg_instr_callback(int (*callback)(int))
//    fun m68k_set_fc_callback(void (*callback)(unsigned int new_fc))
//    fun m68k_set_instr_hook_callback(void (*callback)(unsigned int pc))

// TODO function stubs for these that you an register a callback for:
// unsigned int m68k_read_memory_8(unsigned int address);
// unsigned int m68k_read_memory_16(unsigned int address);
// unsigned int m68k_read_memory_32(unsigned int address);
// unsigned int m68k_read_immediate_16(unsigned int address);
// unsigned int m68k_read_immediate_32(unsigned int address);
// unsigned int m68k_read_pcrelative_8(unsigned int address);
// unsigned int m68k_read_pcrelative_16(unsigned int address);
// unsigned int m68k_read_pcrelative_32(unsigned int address);
// unsigned int m68k_read_disassembler_8 (unsigned int address);
// unsigned int m68k_read_disassembler_16 (unsigned int address);
// unsigned int m68k_read_disassembler_32 (unsigned int address);
// void m68k_write_memory_8(unsigned int address, unsigned int value);
// void m68k_write_memory_16(unsigned int address, unsigned int value);
// void m68k_write_memory_32(unsigned int address, unsigned int value);
// void m68k_write_memory_32_pd(unsigned int address, unsigned int value);

    // IGNORED for now:  void m68k_state_register(const char *type, int index);
}
