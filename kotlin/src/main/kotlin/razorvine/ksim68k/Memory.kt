package razorvine.ksim68k

import com.sun.jna.Callback

open class Memory(val mem: ByteArray) {
    internal fun registerCallbacks(musashi: MusashiNative) {
        musashi.set_read_memory_8_callback(Read8(this))
        musashi.set_read_memory_16_callback(Read16(this))
        musashi.set_read_memory_32_callback(Read32(this))
        musashi.set_write_memory_8_callback(Write8(this))
        musashi.set_write_memory_16_callback(Write16(this))
        musashi.set_write_memory_32_callback(Write32(this))
    }

    open fun read8(address: Int): Short {
        return (mem[address].toInt() and 255).toShort()
    }

    open fun read16(address: Int): Int {
        val b0 = mem[address].toInt() and 255
        val b1 = mem[address+1].toInt() and 255
        return (b0 shl 8) or b1
    }

    open fun read32(address: Int): Long {
        val b0 = mem[address].toLong() and 255
        val b1 = mem[address+1].toLong() and 255
        val b2 = mem[address+2].toLong() and 255
        val b3 = mem[address+3].toLong() and 255
        return (b0 shl 24) or (b1 shl 16) or (b2 shl 8) or b3
    }

    open fun read8s(address: Int): Byte  = mem[address]
    open fun read16s(address: Int): Short = read16(address).toShort()
    open fun read32s(address: Int): Int = read32(address).toInt()

    open fun write8(address: Int, value: Short) {
        mem[address] = value.toByte()
    }

    open fun write8s(address: Int, value: Byte) {
        mem[address] = value
    }

    open fun write16(address: Int, value: Int) {
        mem[address] = (value ushr 8).toByte()
        mem[address+1] = value.toByte()
    }

    open fun write16s(address: Int, value: Short) {
        mem[address] = (value.toInt() ushr 8).toByte()
        mem[address+1] = value.toByte()
    }

    open fun write32(address: Int, value: Long) {
        mem[address] = (value ushr 24).toByte()
        mem[address+1] = (value ushr 16).toByte()
        mem[address+2] = (value ushr 8).toByte()
        mem[address+3] = value.toByte()
    }

    open fun write32s(address: Int, value: Int) {
        mem[address] = (value ushr 24).toByte()
        mem[address+1] = (value ushr 16).toByte()
        mem[address+2] = (value ushr 8).toByte()
        mem[address+3] = value.toByte()
    }

    // callbacks, auto wired by JNA:

    private class Read8(private val mem: Memory) : Callback {
        fun callback(address: Int): Short = mem.read8(address)
    }

    private class Read16(private val mem: Memory) : Callback {
        fun callback(address: Int): Int  = mem.read16(address)
    }

    private class Read32(private val mem: Memory) : Callback {
        fun callback(address: Int): Long  = mem.read32(address)
    }

    private class Write8(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Short) = mem.write8(address, value)
    }

    private class Write16(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Int) = mem.write16(address, value)
    }

    private class Write32(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Long) = mem.write32(address, value)
    }
}
