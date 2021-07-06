package ksimtests

import razorvine.ksim68k.Cpu
import razorvine.ksim68k.Ksim68k
import razorvine.ksim68k.Memory
import razorvine.ksim68k.Register
import kotlin.test.BeforeTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class TestKsim68k {

    private lateinit var memory: MemoryForTest

    private open class MemoryForTest(size: Int) : Memory(size) {

        val reads = mutableListOf<Pair<Int, Int>>()
        val writes = mutableListOf<Triple<Int, Long, Int>>()

        override fun read8(address: Int): Short {
            reads.add(Pair(address, 8))
            return super.read8(address)
        }

        override fun read16(address: Int): Int {
            reads.add(Pair(address, 16))
            return super.read16(address)
        }

        override fun read32(address: Int): Long {
            reads.add(Pair(address, 32))
            return super.read32(address)
        }

        override fun read8s(address: Int): Byte {
            reads.add(Pair(address, 8))
            return super.read8s(address)
        }

        override fun read16s(address: Int): Short {
            reads.add(Pair(address, 16))
            return super.read16s(address)
        }

        override fun read32s(address: Int): Int {
            reads.add(Pair(address, 32))
            return super.read32s(address)
        }

        override fun write8(address: Int, value: Short) {
            writes.add(Triple(address, value.toLong() and 0xffffffff, 8))
            super.write8(address, value)
        }

        override fun write8s(address: Int, value: Byte) {
            writes.add(Triple(address, value.toLong() and 0xffffffff, 8))
            super.write8s(address, value)
        }

        override fun write16(address: Int, value: Int) {
            writes.add(Triple(address, value.toLong() and 0xffffffff, 16))
            super.write16(address, value)
        }

        override fun write16s(address: Int, value: Short) {
            writes.add(Triple(address, value.toLong() and 0xffffffff, 16))
            super.write16s(address, value)
        }

        override fun write32(address: Int, value: Long) {
            writes.add(Triple(address, value, 32))
            super.write32(address, value)
        }

        override fun write32s(address: Int, value: Int) {
            writes.add(Triple(address, value.toLong() and 0xffffffff, 32))
            super.write32s(address, value)
        }
    }

    @BeforeTest
    fun setup() {
        memory = MemoryForTest(0x10000)
        Ksim68k.useMemory(memory)
        Ksim68k.init(Cpu.M68030)
    }

    @Test
    fun testDisassem() {
        memory.write32(0, 0x12345678)
        memory.write32(4, 0xaabbccdd)
        val (disassem, length) = Ksim68k.disassemble(0, Cpu.M68030)
        assertEquals("move.b  ($78,A4,D5.w*8), D1", disassem)
        assertEquals(4, length)
    }

    @Test
    fun testResetPulse() {
        memory.write32(0, 0x11223344)  // stack pointer
        memory.write32(4, 0xaabbccdd)  // program counter
        memory.writes.clear()
        memory.reads.clear()
        Ksim68k.pulseReset()
        val sp = Ksim68k.getReg(Register.SP)
        val a7 = Ksim68k.getReg(Register.A7)
        val pc = Ksim68k.getReg(Register.PC)
        assertEquals(0x11223344, sp)
        assertEquals(sp, a7)
        assertEquals(0xaabbccdd, pc)
        assertEquals(listOf(Pair(0,32), Pair(4,32)), memory.reads)
        assertTrue(memory.writes.isEmpty())
    }

    @Test
    fun testResetCallback() {
        var handlerCalled = false
        fun handler() {
            handlerCalled = true
        }
        memory.write32(0, 0x5000)   // stack pointer
        memory.write32(4, 0x2000)   // program counter
        memory.write16(0x2000, 0x4e70)       // reset instruction
        val oldHandler = Ksim68k.handlerForResetInstruction
        Ksim68k.handlerForResetInstruction = ::handler
        try {
            Ksim68k.pulseReset()
            Ksim68k.execute(5)
            assertTrue(handlerCalled)
        } finally {
            Ksim68k.handlerForResetInstruction = oldHandler
        }
    }

    @Test
    fun testExecute() {
        memory.write32(0, 0x00001234)   // stack pointer
        memory.write32(4, 0x0000abc0)   // program counter
        memory.write16(0x0000abc0, 0x4e71)       // NOP instruction
        memory.write16(0x0000abc2, 0x4e71)       // NOP instruction
        memory.write16(0x0000abc4, 0x4e71)       // NOP instruction
        memory.write16(0x0000abc6, 0x4e71)       // NOP instruction
        memory.write16(0x0000abc8, 0x4e71)       // NOP instruction
        memory.write16(0x0000abca, 0x4e71)       // NOP instruction
        memory.write16(0x0000abcc, 0x4e71)       // NOP instruction
        memory.write16(0x0000abce, 0x4e71)       // NOP instruction
        Ksim68k.pulseReset()
        var reg_pc = Ksim68k.getReg(Register.PC)
        var reg_sp = Ksim68k.getReg(Register.SP)
        assertEquals(0x1234, reg_sp)
        assertEquals(0xabc0, reg_pc)
        var cycles = Ksim68k.execute(8)
        assertEquals(4, cycles)
        cycles = Ksim68k.execute(8)
        assertEquals(8, cycles)
        val reg_a0 = Ksim68k.getReg(Register.A0)
        val reg_a7 = Ksim68k.getReg(Register.A7)
        val reg_d0 = Ksim68k.getReg(Register.D0)
        reg_pc = Ksim68k.getReg(Register.PC)
        reg_sp = Ksim68k.getReg(Register.SP)
        val reg_sr = Ksim68k.getReg(Register.SR)
        assertEquals(0, reg_a0)
        assertEquals(0, reg_d0)
        assertEquals(0x00001234, reg_sp)
        assertEquals(0x0000abcc, reg_pc)
        assertEquals(reg_sp, reg_a7)
        assertEquals(0b0010011100000100, reg_sr)
    }

    @Test
    fun testIllegalInstrHandler() {
        var illegalFound = false
        fun handler(opcode: Int): Int {
            illegalFound = opcode == 0x4afc
            return 0
        }
        val oldHandler = Ksim68k.handlerForIllegalInstruction
        Ksim68k.handlerForIllegalInstruction = ::handler
        try {
            memory.write32(0, 0x00002000)    // stack pointer
            memory.write32(4, 0x00001000)    // program counter
            memory.write32(16, 0x0022334455)    // illegal instruction vector
            memory.write16(0x1000, 0x4afc)   // ILLEGAL instruction
            Ksim68k.pulseReset()
            Ksim68k.execute(6)
            val ir = Ksim68k.getReg(Register.IR)
            val pc = Ksim68k.getReg(Register.PC)
            assertTrue(illegalFound)
            assertEquals(0x4afc, ir)
            assertEquals(0x0022334455, pc)
        } finally {
            Ksim68k.handlerForIllegalInstruction = oldHandler
        }
    }

    @Test
    fun testPcChangedHandler() {
        val jumps = mutableListOf<Int>()
        fun handler(address: Int) {
            jumps.add(address)
        }
        val oldHandler = Ksim68k.handlerForPcChanged
        Ksim68k.handlerForPcChanged = ::handler
        try {
            memory.write32(0, 0x00002000)    // stack pointer
            memory.write32(4, 0x00001000)    // program counter
            memory.write16(0x1000, 0x4e71)   // NOP instruction
            memory.write16(0x1002, 0x4e71)   // NOP instruction
            memory.write16(0x1004, 0x4e71)   // NOP instruction
            Ksim68k.pulseReset()
            Ksim68k.execute(6)
            val pc = Ksim68k.getReg(Register.PC)
            assertEquals(0x1002, pc)
            assertEquals(listOf(0, 0x1000), jumps)
        } finally {
            Ksim68k.handlerForPcChanged = oldHandler
        }
    }

    @Test
    fun testStopInstructionBehavior() {
        memory.write32(0, 0x00002000)    // stack pointer
        memory.write32(4, 0x00001000)    // program counter
        memory.write16(0x1000, 0x4e72)   // STOP instruction
        memory.write16(0x1002, 0x2700)   // sr argument
        Ksim68k.pulseReset()
        Ksim68k.execute(20)
        var ir = Ksim68k.getReg(Register.IR)
        var pc = Ksim68k.getReg(Register.PC)
        assertEquals(0x4e72, ir)
        assertEquals(0x1004, pc)
        Ksim68k.execute(40)
        ir = Ksim68k.getReg(Register.IR)
        pc = Ksim68k.getReg(Register.PC)
        assertEquals(0x4e72, ir)
        assertEquals(0x1004, pc)
    }

    @Test
    fun testExecuteExampleProgram() {
        var output = ""

        class MappedIoMemory(size: Int) : MemoryForTest(size) {
            override fun write8(address: Int, value: Short) {
                if (address == 0x00fff002) {
                    // memory mapped chrout register
                    output += value.toInt().toChar()
                }
            }
        }

        val testprog = javaClass.classLoader.getResourceAsStream("testprog.bin")?.readBytes()!!
        memory = MappedIoMemory(0x8000)
        memory.load(0, testprog)
        Ksim68k.useMemory(memory)
        Ksim68k.pulseReset()
        Ksim68k.execute(2000)
        assertEquals("Hello, world! From the 68000 assembly program.\n", output)
    }
}
