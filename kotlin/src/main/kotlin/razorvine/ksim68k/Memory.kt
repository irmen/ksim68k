package razorvine.ksim68k

import com.sun.jna.Callback

open class Memory(val mem: ShortArray) {
    internal fun registerCallbacks(musashi: MusashiNative) {
        musashi.set_read_memory_8_callback(Read8(this))
        musashi.set_read_memory_16_callback(Read16(this))
        musashi.set_read_memory_32_callback(Read32(this))
        musashi.set_write_memory_8_callback(Write8(this))
        musashi.set_write_memory_16_callback(Write16(this))
        musashi.set_write_memory_32_callback(Write32(this))
    }

    open fun read8(address: Int): Short {
        return mem[address]
    }

    open fun read16(address: Int): Int {
        return mem[address].toInt() shl 8 or mem[address].toInt()
    }

    open fun read32(address: Int): Int {
        return mem[address].toInt() shl 24 or
                mem[address+1].toInt() shl 16 or
                mem[address+2].toInt() shl 8 or
                mem[address+1].toInt()
    }

    open fun write8(address: Int, value: Short) {
        mem[address] = value
    }

    open fun write16(address: Int, value: Int) {
        mem[address] = (value ushr 8 and 0xff).toShort()
        mem[address+1] = (value and 0xff).toShort()
    }

    open fun write32(address: Int, value: Int) {
        mem[address] = (value ushr 24 and 0xff).toShort()
        mem[address+1] = (value ushr 16 and 0xff).toShort()
        mem[address+2] = (value ushr 8 and 0xff).toShort()
        mem[address+3] = (value and 0xff).toShort()
    }


    // callbacks, auto wired by JNA:

    private class Read8(private val mem: Memory) : Callback {
        fun callback(address: Int): Short = mem.read8(address)
    }

    private class Read16(private val mem: Memory) : Callback {
        fun callback(address: Int): Int  = mem.read16(address)
    }

    private class Read32(private val mem: Memory) : Callback {
        fun callback(address: Int): Int  = mem.read32(address)
    }

    private class Write8(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Short) = mem.write8(address, value)
    }

    private class Write16(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Int) = mem.write16(address, value)
    }

    private class Write32(private val mem: Memory) : Callback {
        fun callback(address: Int, value: Int) = mem.write32(address, value)
    }
}
