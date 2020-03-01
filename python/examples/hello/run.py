import ksim68k

CHROUT = 0x00fff002
TRAP15_ADDR = 0x000ff222        # "end program" trap


class MappedIoMemory(ksim68k.Memory):
    def write8(self, address: int, value: int):
        if address == CHROUT:
            print(chr(value), end="")


keep_running = True


def pc_jump_handler(address: int) -> None:
    if address == TRAP15_ADDR:
        global keep_running
        keep_running = False
        rt = ksim68k.get_reg(ksim68k.Register.D0)
        print("Trap15 executed (end program). Exit code=", rt)


ksim68k.pc_changed_handler = pc_jump_handler


def run(program: str) -> None:
    with open(program, "rb") as f:
        data = f.read()

    memory = MappedIoMemory(0x100000)
    memory.load(0, data)
    ksim68k.use_memory(memory)
    ksim68k.init(ksim68k.Cpu.M68000)
    ksim68k.pulse_reset()

    while keep_running:
        ksim68k.execute(16)


if __name__ == "__main__":
    run("testprog.bin")
