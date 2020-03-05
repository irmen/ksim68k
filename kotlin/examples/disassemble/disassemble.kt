package disassemble

import razorvine.ksim68k.Ksim68k
import java.io.File
import razorvine.ksim68k.Memory


fun disassemble(data: ByteArray) {
    val memory = Memory(0x1000)
    memory.load(0, data)
    Ksim68k.useMemory(memory)
    var pc = 0
    while(pc < data.size) {
        val (asm, size) = Ksim68k.disassemble(pc)
        println("${pc.toString(16).padStart(8, '0')}   $asm")
        pc += size
    }
}


fun main() {
    val data = File("program.bin").readBytes()
    disassemble(data)
}
