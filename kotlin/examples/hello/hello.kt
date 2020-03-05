package hello

import razorvine.ksim68k.Cpu
import razorvine.ksim68k.Ksim68k
import razorvine.ksim68k.Memory
import razorvine.ksim68k.Register
import java.io.File

const val CHROUT = 0x00fff002
const val TRAP15_ADDR = 0x000ff222        // "end program" trap


class MappedIoMemory(size: Int) : Memory(size) {
    override fun write8(address: Int, value: Short) {
        if(address== CHROUT)
            print(value.toChar())
    }
}


var keep_running = true


fun pc_jump_handler(address: Int) {
    if(address == TRAP15_ADDR) {
        keep_running = false
        val rt = Ksim68k.getReg(Register.D0)
        println("Trap15 executed (end program). Exit code=$rt")
    }
}


fun run(program: String) {
    val data = File(program).readBytes()
    val memory = MappedIoMemory(0x100000)
    memory.load(0, data)
    Ksim68k.useMemory(memory)
    Ksim68k.init(Cpu.M68000)
    Ksim68k.pulseReset()

    while(keep_running) {
        Ksim68k.execute(16)
    }
}


fun main() {
    Ksim68k.handlerForPcChanged = ::pc_jump_handler
    run("testprog.bin")
}
