import ksim68k


def disassemble(data):
    memory = ksim68k.Memory(0x1000)
    memory.load(0, data)
    ksim68k.use_memory(memory)
    pc = 0
    while pc < len(data):
        asm, size = ksim68k.disassemble(pc)
        print("{:08x}  {}".format(pc, asm))
        pc += size


if __name__ == "__main__":
    with open("program.bin", "rb") as f:
        disassemble(f.read())
