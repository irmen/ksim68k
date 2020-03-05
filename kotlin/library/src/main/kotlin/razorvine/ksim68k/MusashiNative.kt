package razorvine.ksim68k

import com.sun.jna.*
import com.sun.jna.Library
import java.nio.Buffer


internal interface MusashiNative: Library {

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

    // functions:
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

    fun set_read_memory_8_callback(callback: Callback)
    fun set_read_memory_16_callback(callback: Callback)
    fun set_read_memory_32_callback(callback: Callback)
    fun set_write_memory_8_callback(callback: Callback)
    fun set_write_memory_16_callback(callback: Callback)
    fun set_write_memory_32_callback(callback: Callback)
    fun m68k_set_reset_instr_callback(callback: Callback)
    fun m68k_set_pc_changed_callback(callback: Callback)
    fun m68k_set_illg_instr_callback(callback: Callback)

// not used for now:
//    fun m68k_set_int_ack_callback(int (*callback)(int int_level))
//    fun m68k_set_bkpt_ack_callback(void (*callback)(unsigned int data))
//    fun m68k_set_tas_instr_callback(int (*callback)(void))
//    fun m68k_set_fc_callback(void (*callback)(unsigned int new_fc))
//    fun m68k_set_instr_hook_callback(void (*callback)(unsigned int pc))

    // IGNORED for now:  void m68k_state_register(const char *type, int index);
}
